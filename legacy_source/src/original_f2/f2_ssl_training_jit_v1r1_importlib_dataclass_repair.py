from __future__ import annotations
import argparse,csv,hashlib,importlib.util,inspect,io,json,math,os,re,sqlite3,time,urllib.request,sys
from collections import OrderedDict
from pathlib import Path
import h5py,numpy as np,torch

BR={
 "low_mid":{"fs":4096,"band":(20.,1600.),"nperseg":1048,"hop":524,"nfft":1048,"temporal":16384,"tf":(404,30)},
 "high":{"fs":16384,"band":(1600.,5000.),"nperseg":4192,"hop":2096,"nfft":4192,"temporal":65536,"tf":(870,30)}}
B=32; CONTEXT=64.; TARGET=4.; SEEDS=(20260919,20260920,20260921)
ANCHORS=("TRAIN|O4a::H1|low_mid|E000|S193","TRAIN|O4b::L1|high|E000|S111")

def loadpy(p,n):
 s=importlib.util.spec_from_file_location(n,p)
 if s is None or s.loader is None: raise RuntimeError(f'cannot import {p}')
 m=importlib.util.module_from_spec(s)
 sys.modules[n]=m
 try:
  s.loader.exec_module(m)
 except Exception:
  sys.modules.pop(n,None)
  raise
 return m

def asha(x):
 a=np.ascontiguousarray(x); h=hashlib.sha256(); h.update(str(a.dtype).encode()); h.update(repr(tuple(a.shape)).encode()); h.update(a.tobytes()); return h.hexdigest().upper()
def safe(s): return re.sub(r"[^A-Za-z0-9_.-]+","_",s)
def sid(cell,branch,epoch): return f"TRAIN|{cell}|{branch}|E{int(epoch):03d}"
def bkey(r): return f"{r['_part']}|{r['cell_key']}|{r['branch']}|E{int(r.get('epoch',0)):03d}|R{int(r['round_index']):02d}|Q{int(r.get('sequence',-1)):06d}"
def seed64(*p): return int.from_bytes(hashlib.sha256("|".join(map(str,p)).encode()).digest()[:8],"little")

class RangeFile(io.RawIOBase):
 def __init__(self,url,bs=8<<20,maxb=6):
  self.url=url; self.bs=bs; self.maxb=maxb; self.pos=0; self.cache=OrderedDict()
  q=urllib.request.Request(url,method="HEAD",headers={"User-Agent":"GW-Tech-F2-JIT/1.0"})
  with urllib.request.urlopen(q,timeout=120) as r:
   x=r.headers.get("Content-Length");
   if not x: raise RuntimeError("missing Content-Length")
   self.size=int(x)
 def readable(self): return True
 def seekable(self): return True
 def tell(self): return self.pos
 def seek(self,o,w=0):
  self.pos=int(o if w==0 else self.pos+o if w==1 else self.size+o); return self.pos
 def block(self,i):
  if i in self.cache:
   z=self.cache.pop(i); self.cache[i]=z; return z
  a=i*self.bs; b=min(self.size,a+self.bs)-1; last=None
  for k in range(6):
   try:
    q=urllib.request.Request(self.url,headers={"Range":f"bytes={a}-{b}","Accept-Encoding":"identity","User-Agent":"GW-Tech-F2-JIT/1.0"})
    with urllib.request.urlopen(q,timeout=120) as r:
     if getattr(r,"status",None)!=206 or not r.headers.get("Content-Range"): raise RuntimeError("HTTP Range not honored")
     z=r.read()
    if len(z)!=b-a+1: raise RuntimeError("short range")
    self.cache[i]=z
    while len(self.cache)>self.maxb: self.cache.popitem(last=False)
    return z
   except Exception as e: last=e; time.sleep(2*(k+1))
  raise RuntimeError(f"range fetch failed: {last}")
 def read(self,n=-1):
  if n<0: n=self.size-self.pos
  n=min(n,self.size-self.pos); out=bytearray()
  while n>0:
   i=self.pos//self.bs; off=self.pos%self.bs; z=self.block(i); take=min(n,len(z)-off)
   out+=z[off:off+take]; self.pos+=take; n-=take
  return bytes(out)
 def readinto(self,b):
  z=self.read(len(b)); b[:len(z)]=z; return len(z)

def strain(h):
 if "strain" in h and "Strain" in h["strain"]: return h["strain"]["Strain"]
 c=[]
 def v(n,o):
  if isinstance(o,h5py.Dataset) and o.ndim==1: c.append((n,o))
 h.visititems(v)
 for n,o in c:
  if n.lower().endswith("strain"): return o
 if len(c)==1:return c[0][1]
 raise RuntimeError("strain dataset not found")

def piece(src,lo,hi,fs):
 rf=RangeFile(src["hdf5_url"])
 try:
  with h5py.File(rf,"r") as h:
   d=strain(h); dur=float(src["duration_s"])
   if abs(d.shape[0]/dur-fs)>1e-6: raise RuntimeError("sample rate mismatch")
   g=float(src["gps_start"]); i0=round((lo-g)*fs); i1=round((hi-g)*fs)
   return np.asarray(d[int(i0):int(i1)],dtype=np.float64)
 finally: rf.close()

def transform(ref,man,helper):
 s=BR[ref["branch"]]; fs=s["fs"]; a=ref["gps"]-CONTEXT; z=ref["gps"]+TARGET; xs=[]; last=None
 for base in ref["sources"]:
  q=man[base]; g=float(q["gps_start"]); e=g+float(q["duration_s"]); lo=max(a,g); hi=min(z,e)
  if hi<=lo: continue
  if last is not None and abs(lo-last)>0.5/fs: raise RuntimeError("noncontiguous cross-file window")
  xs.append(piece(q,lo,hi,fs)); last=hi
 raw=np.concatenate(xs) if len(xs)>1 else xs[0]
 exp=round((CONTEXT+TARGET)*fs)
 if len(raw)!=exp or not np.isfinite(raw).all(): raise RuntimeError("raw assembly gate failed")
 morph,meta=helper.deterministic_whiten(raw[:round(CONTEXT*fs)],raw[round(CONTEXT*fs):],fs,s["band"])
 tf,_,_=helper.r1t_stft(morph,fs,s["band"],s["nperseg"],s["hop"],s["nfft"])
 return morph.astype(np.float32),tf.astype(np.float32),float(meta.get("amplitude_log10_rms",np.nan))

def refs(row,man):
 e=int(row.get("epoch",0)); rix=int(row["round_index"]); out=[]
 for i,(g,ss) in enumerate(zip(row["target_gps_starts"],row["required_hdf5_basenames_per_window"])):
  out.append({"branch":row["branch"],"cell":row["cell_key"],"epoch":e,"slot":rix*32+i,"gps":float(g),"sources":sorted(ss,key=lambda x:int(man[x]["gps_start"]))})
 if len(out)!=32: raise RuntimeError("non-B32 row")
 return out

def cachepath(root,row):
 d=Path(root)/row["_part"]/row["branch"]/f"E{int(row.get('epoch',0)):03d}"; d.mkdir(parents=True,exist_ok=True)
 return d/(safe(bkey(row))+".npz")
def materialize(row,man,helper,root,qstate):
 k=bkey(row)
 if k in qstate:return None,"quality_excluded"
 p=cachepath(root,row)
 if p.exists():
  try:
   z=np.load(p); t=z["t"]; f=z["f"]; a=z["a"]
   if len(t)==32 and len(f)==32:return (t,f,a),"cache"
  except Exception: p.unlink(missing_ok=True)
 ts=[]; fs=[]; aa=[]
 try:
  for j,r in enumerate(refs(row,man)):
   t,f,a=transform(r,man,helper); ts.append(t);fs.append(f);aa.append(a)
   if (j+1)%8==0: print(f"MATERIALIZE {k} {j+1}/32",flush=True)
 except Exception as e:
  if "NO_POSITIVE_PSD" in str(e): qstate[k]={"reason":"NO_POSITIVE_PSD","no_replacement":True}; return None,"quality_excluded_new"
  raise
 t=np.stack(ts); f=np.stack(fs); a=np.asarray(aa,np.float32); tmp=p.with_suffix(".tmp")
 with tmp.open("wb") as h: np.savez(h,t=t,f=f,a=a)
 os.replace(tmp,p); return (t,f,a),"remote_range"

def translate(x,sh):
 y=np.zeros_like(x)
 if sh==0:y[:]=x
 elif sh>0:y[sh:]=x[:-sh]
 else:y[:sh]=x[-sh:]
 return y

def views(t,f,branch,seed,epoch,seq,i,valid=False):
 ans=[]; fs=BR[branch]["fs"]; s0=20260919 if valid else seed; ep=0 if valid else epoch
 for v in (1,2):
  r=np.random.default_rng(seed64("F2",s0,ep,seq,i,v,branch)); sh=int(r.integers(-round(.125*fs),round(.125*fs)+1))
  y=translate(t,sh); y*=(-1. if r.random()<.5 else 1.); y*=float(np.exp(r.uniform(np.log(.9),np.log(1.1))))
  rms=float(np.sqrt(np.mean(y*y))); y=y+r.standard_normal(len(y))*(.005*max(rms,np.finfo(float).tiny)); target=y.astype(np.float32)
  tm=np.zeros(len(y),bool); ml=max(1,int(math.floor(.02*len(y)))); m0=int(r.integers(0,len(y)-ml+1)); tm[m0:m0+ml]=1; ti=target.copy();ti[tm]=0
  ft=f.astype(np.float32,copy=True); fi=ft.copy(); fm=np.zeros(f.shape,bool); col=int(r.integers(0,f.shape[1])); fm[:,col]=1; fi[:,col]=0
  ans.append((ti,fi,target,tm,ft,fm))
 return ans

def fw(model,v): return model(torch.from_numpy(v[0]).float().unsqueeze(0),torch.from_numpy(v[1]).float().unsqueeze(0))
def vic(mm,z1,z2):
 c=mm.vicreg_components(z1,z2); return 25*c["invariance"]+25*c["variance"]+c["covariance"],c

def rec(mm,o1,o2,v1,v2):
 def T(x,dtype=None): return torch.from_numpy(x).to(dtype=dtype) if dtype else torch.from_numpy(x)
 rt=.5*(mm.masked_huber(o1["temporal_reconstruction"],T(v1[2],torch.float32).unsqueeze(0),T(v1[3]).bool().unsqueeze(0))+mm.masked_huber(o2["temporal_reconstruction"],T(v2[2],torch.float32).unsqueeze(0),T(v2[3]).bool().unsqueeze(0)))
 rf=.5*(mm.masked_huber(o1["tf_reconstruction"],T(v1[4],torch.float32).unsqueeze(0),T(v1[5]).bool().unsqueeze(0))+mm.masked_huber(o2["tf_reconstruction"],T(v2[4],torch.float32).unsqueeze(0),T(v2[5]).bool().unsqueeze(0)))
 return .5*(rt+rf)

def trainbatch(model,mm,opt,t,f,branch,seed,epoch,seq):
 model.train(); vv=[]; z1=[];z2=[]
 with torch.no_grad():
  for i in range(32):
   a,b=views(t[i],f[i],branch,seed,epoch,seq,i,False);vv.append((a,b));z1.append(fw(model,a)["projected"].squeeze(0));z2.append(fw(model,b)["projected"].squeeze(0))
 Z1=torch.stack(z1).requires_grad_(True);Z2=torch.stack(z2).requires_grad_(True);vl,c=vic(mm,Z1,Z2);g1,g2=torch.autograd.grad(vl,(Z1,Z2)); opt.zero_grad(set_to_none=True);rv=0.
 for i,(a,b) in enumerate(vv):
  o1=fw(model,a);o2=fw(model,b); rr=rec(mm,o1,o2,a,b); ((o1["projected"].squeeze(0)*g1[i]).sum()+(o2["projected"].squeeze(0)*g2[i]).sum()+rr/32.).backward();rv+=float(rr)/32
 gn=float(torch.nn.utils.clip_grad_norm_(model.parameters(),1.0));opt.step();return float(vl)+rv,gn

@torch.no_grad()
def valbatch(model,mm,t,f,branch,seed,seq):
 model.eval();z1=[];z2=[];rv=0.
 for i in range(32):
  a,b=views(t[i],f[i],branch,seed,0,seq,i,True);o1=fw(model,a);o2=fw(model,b);z1.append(o1["projected"].squeeze(0));z2.append(o2["projected"].squeeze(0));rv+=float(rec(mm,o1,o2,a,b))/32
 v,_=vic(mm,torch.stack(z1),torch.stack(z2));return float(v)+rv

def lrfn(mm):
 c=[]
 for n,o in vars(mm).items():
  if inspect.isfunction(o):
   try:s=inspect.getsource(o)
   except:continue
   if "minimum_lr" in s and "warmup_start_factor" in s and "cosine" in s.lower():c.append((n,o))
 if len(c)!=1:raise RuntimeError(f"LR function ambiguity {[x[0] for x in c]}")
 print("LR_FUNCTION",c[0][0],flush=True);return c[0][1]

def loadrows(p,part):
 out=[]
 with Path(p).open("r",encoding="utf-8") as h:
  for l in h:
   if l.strip():r=json.loads(l);r["_part"]=part;out.append(r)
 return out

def anchor_ref(rows,man,key):
 m=re.match(r"TRAIN\|(.+)\|(low_mid|high)\|E(\d+)\|S(\d+)$",key);cell,branch,e,slot=m.group(1),m.group(2),int(m.group(3)),int(m.group(4));rix=slot//32;i=slot%32
 for r in rows:
  if r["cell_key"]==cell and r["branch"]==branch and int(r.get("epoch",0))==e and int(r["round_index"])==rix:return refs(r,man)[i]
 raise RuntimeError("anchor ref missing")
def prodread(root,key,ref):
 d=Path(root)/safe(key.rsplit("|S",1)[0]);slot=int(key.rsplit("S",1)[1]);t=np.load(d/"temporal.npy",mmap_mode="r");f=np.load(d/"tf.npy",mmap_mode="r");b=np.load(d/"fill.npy",mmap_mode="r");
 if int(b[slot])!=1:raise RuntimeError("anchor cache missing")
 return np.asarray(t[slot]).copy(),np.asarray(f[slot]).copy()

def accessgate(state,rows,man,helper,pc):
 p=Path(state)/"REMOTE_RANGE_ACCESS_EQUIVALENCE_PASS.json"
 if p.exists():print("REMOTE_RANGE_ACCESS_EQUIVALENCE_REUSE",flush=True);return
 rr=[]
 for k in ANCHORS:
  r=anchor_ref(rows,man,k);pt,pf=prodread(pc,k,r);jt,jf,_=transform(r,man,helper);ok=np.array_equal(pt,jt) and np.array_equal(pf,jf);x={"slot":k,"temporal_exact":bool(np.array_equal(pt,jt)),"tf_exact":bool(np.array_equal(pf,jf)),"t_sha":asha(jt),"f_sha":asha(jf)};print("RANGE_ANCHOR",json.dumps(x,sort_keys=True),flush=True)
  if not ok:raise RuntimeError("range access equivalence failed")
  rr.append(x)
 p.write_text(json.dumps({"status":"PASS_REMOTE_RANGE_ACCESS_EQUIVALENCE","anchors":rr},indent=2),encoding="utf-8");print("PASS_REMOTE_RANGE_ACCESS_EQUIVALENCE",flush=True)

def main():
 ap=argparse.ArgumentParser()
 for n in ("model","train","valid","sources","helper","ledger","prod_cache","state","dense","out"):ap.add_argument("--"+n.replace("_","-"),dest=n,type=Path,required=True)
 ap.add_argument("--max-batches",type=int,default=240);a=ap.parse_args();a.state.mkdir(parents=True,exist_ok=True);a.dense.mkdir(parents=True,exist_ok=True);a.out.mkdir(parents=True,exist_ok=True)
 torch.set_num_threads(4);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)
 man={r["basename"]:r for r in csv.DictReader(a.sources.open("r",newline="",encoding="utf-8-sig"))};train=loadrows(a.train,"TRAIN");valid=loadrows(a.valid,"VALID");
 if len(man)!=32226 or len(train)!=24000:raise RuntimeError(f"binding count mismatch sources={len(man)} train={len(train)}")
 helper=loadpy(a.helper,"prep");mm=loadpy(a.model,"r2a");lrf=lrfn(mm);accessgate(a.state,train,man,helper,a.prod_cache)
 con=sqlite3.connect(f"file:{a.ledger.as_posix()}?mode=ro",uri=True);frozen=set()
 for s,slot in con.execute("SELECT shard_id,slot FROM slots WHERE status='quality_excluded'"):frozen.add(f"{s}|R{int(slot)//32:02d}")
 con.close();qp=a.state/"JIT_QUALITY_EXCLUSIONS.json";q=json.loads(qp.read_text()) if qp.exists() else {}
 summary={"seeds":{},"optimizer_authorized_after_range_gate":True,"zero_lag":False}
 for seed in SEEDS:
  sd=a.state/f"SEED_{seed}";sd.mkdir(exist_ok=True);ck=sd/"latest.pt";bestp=sd/"best.pt";hist=sd/"history.jsonl";torch.manual_seed(seed);np.random.seed(seed&0xffffffff);model=mm.F2RepresentationModel().float();opt=torch.optim.AdamW(model.parameters(),lr=3e-4,betas=(.9,.999),eps=1e-8,weight_decay=1e-4);st={"epoch":0,"batch":0,"best":float("inf"),"best_epoch":None,"pref":float("inf"),"pat":0,"complete":False}
  if ck.exists():x=torch.load(ck,map_location="cpu",weights_only=False);model.load_state_dict(x["model"]);opt.load_state_dict(x["opt"]);st.update(x["state"]);print("RESUME",seed,st,flush=True)
  used=0
  while not st["complete"] and used<a.max_batches:
   e=int(st["epoch"]);rows=[r for r in train if int(r.get("epoch",0))==e]
   if len(rows)!=240:raise RuntimeError(f"epoch rows {len(rows)}")
   lr=float(lrf(e));[pg.update(lr=lr) for pg in opt.param_groups]
   while st["batch"]<240 and used<a.max_batches:
    bi=int(st["batch"]);r=rows[bi];fk=f"{sid(r['cell_key'],r['branch'],e)}|R{int(r['round_index']):02d}"
    if fk in frozen or bkey(r) in q:st["batch"]+=1;continue
    data,mode=materialize(r,man,helper,a.dense,q)
    if data is None:qp.write_text(json.dumps(q,indent=2),encoding="utf-8");st["batch"]+=1;continue
    loss,gn=trainbatch(model,mm,opt,data[0],data[1],r["branch"],seed,e,int(r.get("sequence",-1)));st["batch"]+=1;used+=1
    if st["batch"]%5==0 or used>=a.max_batches:torch.save({"model":model.state_dict(),"opt":opt.state_dict(),"state":st},ck);print(f"TRAIN seed={seed} epoch={e} batch={st['batch']}/240 mode={mode} loss={loss:.8g} grad={gn:.6g}",flush=True)
   if st["batch"]<240:break
   vals=[]
   for r in valid:
    data,mode=materialize(r,man,helper,a.dense,q)
    if data is not None:vals.append(valbatch(model,mm,data[0],data[1],r["branch"],seed,int(r.get("sequence",-1))))
   if not vals:raise RuntimeError("no validation batches")
   v=float(np.mean(vals));rec={"seed":seed,"epoch":e,"validation_loss":v,"lr":lr,"time":time.time()};
   if v<st["best"]:st["best"]=v;st["best_epoch"]=e;torch.save({"model":model.state_dict(),"opt":opt.state_dict(),"state":st},bestp)
   if not math.isfinite(st["pref"]) or v<st["pref"]*(1-.001):st["pref"]=v;st["pat"]=0
   else:st["pat"]+=1
   with hist.open("a",encoding="utf-8") as h:h.write(json.dumps(rec,sort_keys=True)+"\n")
   print("EPOCH_RESULT",json.dumps({**rec,"best":st["best"],"best_epoch":st["best_epoch"],"patience":st["pat"]},sort_keys=True),flush=True);st["epoch"]+=1;st["batch"]=0
   if st["pat"]>=10 or st["epoch"]>=100:st["complete"]=True
   torch.save({"model":model.state_dict(),"opt":opt.state_dict(),"state":st},ck)
  ss={**st,"batches_advanced_this_invocation":used}
  if not math.isfinite(float(ss["best"])): ss["best"]=None
  if not math.isfinite(float(ss["pref"])): ss["pref"]=None
  summary["seeds"][str(seed)]=ss
 qp.write_text(json.dumps(q,indent=2,sort_keys=True),encoding="utf-8");summary["all_complete"]=all(x["complete"] for x in summary["seeds"].values());(a.out/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True),encoding="utf-8");print("F2_SSL_TRAINING_JIT_INVOCATION_PASS",json.dumps(summary,sort_keys=True),flush=True)
if __name__=="__main__":main()