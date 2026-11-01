from __future__ import annotations
import argparse, hashlib, importlib.util, json, math, os, re, sqlite3, sys, time
from pathlib import Path
import numpy as np
import torch

SEEDS=(20260919,20260920,20260921)
TRAIN_N=64
DEV_N=32
MIN_SEP=68.0
MAX_EPOCHS=6

def loadpy(path,name):
    s=importlib.util.spec_from_file_location(name,path)
    if s is None or s.loader is None:
        raise RuntimeError(f"cannot import {path}")
    m=importlib.util.module_from_spec(s)
    sys.modules[name]=m
    try:
        s.loader.exec_module(m)
    except Exception:
        sys.modules.pop(name,None)
        raise
    return m

def safe(s): return re.sub(r"[^A-Za-z0-9_.-]+","_",s)

def asha(x):
    a=np.ascontiguousarray(x)
    h=hashlib.sha256()
    h.update(str(a.dtype).encode())
    h.update(repr(tuple(a.shape)).encode())
    h.update(a.tobytes())
    return h.hexdigest().upper()

def fsha(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest().upper()

def group(cell,branch): return f"{cell}|{branch}"

def pick_forward(rows,n,upper=None):
    out=[]; last=None
    for r in rows:
        g=float(r["gps"])
        if upper is not None and g>upper:
            continue
        if last is None or g-last>=MIN_SEP:
            out.append(r); last=g
            if len(out)==n:
                break
    return out

def pick_backward(rows,n):
    out=[]; last=None
    for r in reversed(rows):
        g=float(r["gps"])
        if last is None or last-g>=MIN_SEP:
            out.append(r); last=g
            if len(out)==n:
                break
    out.reverse()
    return out

def build_schedule(db,outpath):
    con=sqlite3.connect(f"file:{Path(db).as_posix()}?mode=ro",uri=True)
    rows=con.execute(
        "SELECT slot_key,shard_id,slot,cell_key,branch,target_gps_start,temporal_sha256,tf_sha256 "
        "FROM slots WHERE status='cache_verified' "
        "ORDER BY cell_key,branch,target_gps_start,slot_key"
    ).fetchall()
    con.close()

    gs={}
    for r in rows:
        d={"slot_key":r[0],"shard_id":r[1],"slot":int(r[2]),"cell_key":r[3],
           "branch":r[4],"gps":float(r[5]),"temporal_sha256":r[6],"tf_sha256":r[7]}
        gs.setdefault(group(r[3],r[4]),[]).append(d)

    expected={
        "O4a::H1|high","O4a::H1|low_mid","O4a::L1|high","O4a::L1|low_mid",
        "O4b::H1|high","O4b::H1|low_mid","O4b::L1|high","O4b::L1|low_mid",
        "O4b::V1|high","O4b::V1|low_mid"
    }
    if set(gs)!=expected:
        raise RuntimeError(f"group mismatch missing={sorted(expected-set(gs))} extra={sorted(set(gs)-expected)}")

    out={"status":"FROZEN_COMPUTE_BOUNDED_SCHEDULE_V1",
         "train_per_group":TRAIN_N,"dev_per_group":DEV_N,
         "minimum_separation_s":MIN_SEP,"groups":{}}

    for gn in sorted(gs):
        rr=gs[gn]
        dev=pick_backward(rr,DEV_N)
        if len(dev)!=DEV_N:
            raise RuntimeError(f"{gn}: only {len(dev)} spaced DEV windows")
        dev_min=min(x["gps"] for x in dev)
        train=pick_forward(rr,TRAIN_N,upper=dev_min-MIN_SEP)
        if len(train)!=TRAIN_N:
            raise RuntimeError(f"{gn}: only {len(train)} spaced TRAIN windows before development split")
        train_max=max(x["gps"] for x in train)
        gap=dev_min-train_max
        if gap<MIN_SEP:
            raise RuntimeError(f"{gn}: TRAIN/DEV gap {gap} < {MIN_SEP}")
        out["groups"][gn]={
            "cell_key":train[0]["cell_key"],"branch":train[0]["branch"],
            "available_verified":len(rr),"train":train,"dev":dev,
            "train_max_gps":train_max,"dev_min_gps":dev_min,"train_dev_gap_s":gap
        }

    Path(outpath).write_text(json.dumps(out,indent=2,sort_keys=True),encoding="utf-8")
    return out

def read_slot(root,r):
    d=Path(root)/safe(r["shard_id"])
    slot=int(r["slot"])
    t=np.load(d/"temporal.npy",mmap_mode="r")
    f=np.load(d/"tf.npy",mmap_mode="r")
    b=np.load(d/"fill.npy",mmap_mode="r")
    if int(b[slot])!=1:
        raise RuntimeError(f"cache fill missing {r['slot_key']}")
    ta=np.asarray(t[slot]).copy()
    fa=np.asarray(f[slot]).copy()
    del t,f,b
    if asha(ta)!=r["temporal_sha256"] or asha(fa)!=r["tf_sha256"]:
        raise RuntimeError(f"cache hash mismatch {r['slot_key']}")
    return ta,fa

def compact_group(prod,compact,gn,info):
    gd=Path(compact)/safe(gn)
    gd.mkdir(parents=True,exist_ok=True)
    ans={}
    for part in ("train","dev"):
        p=gd/f"{part}.npz"
        if p.exists():
            z=np.load(p,allow_pickle=False)
            exp=TRAIN_N if part=="train" else DEV_N
            if z["t"].shape[0]!=exp or z["f"].shape[0]!=exp:
                raise RuntimeError(f"existing compact cache shape mismatch {p}")
            ans[part]={"windows":exp,"sha256":fsha(p)}
            continue
        ts=[];fs=[]
        for i,r in enumerate(info[part]):
            t,f=read_slot(prod,r);ts.append(t);fs.append(f)
            if (i+1)%32==0:
                print(f"COMPACT {gn} {part} {i+1}/{len(info[part])}",flush=True)
        t=np.stack(ts).astype(np.float32)
        f=np.stack(fs).astype(np.float32)
        tmp=p.with_suffix(".tmp")
        with tmp.open("wb") as h:
            np.savez(h,t=t,f=f)
        os.replace(tmp,p)
        ans[part]={"windows":len(t),"sha256":fsha(p)}
    return ans

def loadc(root,gn,part):
    z=np.load(Path(root)/safe(gn)/f"{part}.npz",allow_pickle=False)
    return z["t"],z["f"]

def saveck(path,obj):
    p=Path(path);tmp=p.with_suffix(".tmp")
    torch.save(obj,tmp)
    os.replace(tmp,p)

def main():
    ap=argparse.ArgumentParser()
    for n in ("model","base_trainer","ledger","prod_cache","state","compact","schedule","out"):
        ap.add_argument("--"+n.replace("_","-"),dest=n,type=Path,required=True)
    a=ap.parse_args()

    for p in (a.state,a.compact,a.out):
        p.mkdir(parents=True,exist_ok=True)

    torch.set_num_threads(4)
    torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True)

    mm=loadpy(a.model,"cb_r2a")
    base=loadpy(a.base_trainer,"cb_base")
    lrf=base.lrfn(mm)

    if a.schedule.exists():
        sched=json.loads(a.schedule.read_text(encoding="utf-8"))
        if sched.get("status")!="FROZEN_COMPUTE_BOUNDED_SCHEDULE_V1":
            raise RuntimeError("schedule status mismatch")
    else:
        sched=build_schedule(a.ledger,a.schedule)

    gaps=[float(x["train_dev_gap_s"]) for x in sched["groups"].values()]
    print("SCHEDULE_PASS",json.dumps({
        "groups":len(sched["groups"]),
        "train_windows":sum(len(x["train"]) for x in sched["groups"].values()),
        "dev_windows":sum(len(x["dev"]) for x in sched["groups"].values()),
        "minimum_train_dev_gap_s":min(gaps),
        "network_access":False
    },sort_keys=True),flush=True)

    compact_meta={}
    for gn,info in sched["groups"].items():
        compact_meta[gn]=compact_group(a.prod_cache,a.compact,gn,info)
    print("COMPACT_LOCAL_CACHE_PASS",json.dumps(compact_meta,sort_keys=True),flush=True)

    groups=sorted(sched["groups"])
    train_batches=[]
    for gi,gn in enumerate(groups):
        br=sched["groups"][gn]["branch"]
        for bi in range(TRAIN_N//32):
            train_batches.append({"gn":gn,"branch":br,"lo":bi*32,"hi":(bi+1)*32,
                                  "seq":100000+gi*10+bi})
    dev_batches=[{"gn":gn,"branch":sched["groups"][gn]["branch"],"seq":200000+i}
                 for i,gn in enumerate(groups)]

    summary={
        "seeds":{},"schedule_sha256":fsha(a.schedule),
        "train_windows":TRAIN_N*len(groups),
        "dev_windows":DEV_N*len(groups),
        "train_batches_per_epoch":len(train_batches),
        "dev_batches_per_epoch":len(dev_batches),
        "max_epochs":MAX_EPOCHS,
        "network_access":False,
        "external_frozen_validation_touched":False,
        "zero_lag":False
    }

    for seed in SEEDS:
        sd=a.state/f"SEED_{seed}"
        sd.mkdir(exist_ok=True)
        ck=sd/"latest.pt";bestp=sd/"best.pt";hist=sd/"history.jsonl"

        torch.manual_seed(seed)
        np.random.seed(seed & 0xffffffff)
        model=mm.F2RepresentationModel().float()
        opt=torch.optim.AdamW(model.parameters(),lr=3e-4,betas=(.9,.999),eps=1e-8,weight_decay=1e-4)
        st={"epoch":0,"order_index":0,"best":float("inf"),"best_epoch":None,"complete":False}

        if ck.exists():
            x=torch.load(ck,map_location="cpu",weights_only=False)
            model.load_state_dict(x["model"]);opt.load_state_dict(x["opt"]);st.update(x["state"])
            print(f"RESUME seed={seed} state={st}",flush=True)

        while not st["complete"]:
            e=int(st["epoch"])
            if e>=MAX_EPOCHS:
                st["complete"]=True
                break

            lr=float(lrf(e))
            for pg in opt.param_groups:
                pg["lr"]=lr

            rng=np.random.default_rng(base.seed64("CBV1",seed,e))
            order=list(rng.permutation(len(train_batches)))
            oi=int(st["order_index"])
            losses=[]
            t0=time.time()

            while oi<len(order):
                bd=train_batches[int(order[oi])]
                t,f=loadc(a.compact,bd["gn"],"train")
                loss,gnorm=base.trainbatch(
                    model,mm,opt,
                    t[bd["lo"]:bd["hi"]],
                    f[bd["lo"]:bd["hi"]],
                    bd["branch"],seed,e,bd["seq"]
                )
                losses.append(float(loss))
                oi+=1
                st["order_index"]=oi
                if oi%5==0 or oi==len(order):
                    saveck(ck,{"model":model.state_dict(),"opt":opt.state_dict(),"state":st})
                    print(f"TRAIN seed={seed} epoch={e} batch={oi}/{len(order)} loss={loss:.8g} grad={gnorm:.6g}",flush=True)

            vals=[]
            for dd in dev_batches:
                t,f=loadc(a.compact,dd["gn"],"dev")
                vals.append(base.valbatch(model,mm,t,f,dd["branch"],seed,dd["seq"]))

            v=float(np.mean(vals))
            tr=float(np.mean(losses))
            if v<float(st["best"]):
                st["best"]=v
                st["best_epoch"]=e
                saveck(bestp,{"model":model.state_dict(),"opt":opt.state_dict(),"state":st})

            rec={
                "seed":seed,"epoch":e,"train_loss":tr,"dev_loss":v,"lr":lr,
                "best":st["best"],"best_epoch":st["best_epoch"],
                "epoch_seconds":time.time()-t0
            }
            with hist.open("a",encoding="utf-8") as h:
                h.write(json.dumps(rec,sort_keys=True)+"\n")
            print("EPOCH_RESULT",json.dumps(rec,sort_keys=True),flush=True)

            st["epoch"]=e+1
            st["order_index"]=0
            if st["epoch"]>=MAX_EPOCHS:
                st["complete"]=True
            saveck(ck,{"model":model.state_dict(),"opt":opt.state_dict(),"state":st})

        summary["seeds"][str(seed)]={
            "complete":bool(st["complete"]),
            "best":float(st["best"]),
            "best_epoch":st["best_epoch"]
        }
        print(f"SEED_COMPLETE seed={seed} best_epoch={st['best_epoch']} best_dev={st['best']}",flush=True)

    summary["all_complete"]=all(v["complete"] for v in summary["seeds"].values())
    (a.out/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True),encoding="utf-8")
    print("COMPUTE_BOUNDED_TRAINING_PASS",json.dumps(summary,sort_keys=True),flush=True)

if __name__=="__main__":
    main()