from __future__ import annotations
import argparse,csv,hashlib,importlib.util,json,math,os,re,shutil,subprocess,sys,time
from pathlib import Path
import h5py,numpy as np,torch
from scipy.stats import rankdata

SEEDS=(20260919,20260920,20260921)
BR={"low_mid":{"fs":4096,"band":(20.,1600.),"nperseg":1048,"hop":524,"nfft":1048,"temporal":16384},
    "high":{"fs":16384,"band":(1600.,5000.),"nperseg":4192,"hop":2096,"nfft":4192,"temporal":65536}}
CONTEXT=64.;TARGET=4.;EVAL_SEED=20260926

def loadpy(p,n):
 s=importlib.util.spec_from_file_location(n,p)
 if s is None or s.loader is None:raise RuntimeError(f"cannot import {p}")
 m=importlib.util.module_from_spec(s);sys.modules[n]=m
 try:s.loader.exec_module(m)
 except Exception:sys.modules.pop(n,None);raise
 return m
def safe(s):return re.sub(r"[^A-Za-z0-9_.-]+","_",s)
def asint(v,default):
 if v is None or v=="":return int(default)
 return int(v)
def md5(p):
 h=hashlib.md5()
 with Path(p).open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b)
 return h.hexdigest().upper()
def fsha(p):
 h=hashlib.sha256()
 with Path(p).open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b)
 return h.hexdigest().upper()
def rows(path):
 out=[]
 with Path(path).open("r",encoding="utf-8") as f:
  for l in f:
   if l.strip():out.append(json.loads(l))
 return out
def man(path):
 with Path(path).open("r",newline="",encoding="utf-8-sig") as f:return {r["basename"]:r for r in csv.DictReader(f)}
def select_panel(rr):
 g={}
 for r in rr:g.setdefault(f"{r['cell_key']}|{r['branch']}",[]).append(r)
 exp={"O4a::H1|high","O4a::H1|low_mid","O4a::L1|high","O4a::L1|low_mid","O4b::H1|high","O4b::H1|low_mid","O4b::L1|high","O4b::L1|low_mid","O4b::V1|high","O4b::V1|low_mid"}
 if set(g)!=exp:raise RuntimeError(f"VALID groups mismatch {set(g)^exp}")
 out={}
 for k,v in g.items():
  v=sorted(v,key=lambda r:(asint(r.get("sequence"),10**9),asint(r.get("epoch"),0),asint(r.get("round_index"),0)))
  if len(v[0]["target_gps_starts"])!=32:raise RuntimeError("non-B32 VALID")
  out[k]=v[0]
 return out
def find_local(root,base,expected):
 if not Path(root).exists():return None
 for p in Path(root).rglob("*"):
  if p.is_file() and p.name in {base,base+".partial",base+".curl.partial"}:
   try:
    if md5(p)==expected:return p
   except OSError:pass
 return None
def acquire(src,work,rawroot):
 base=src["basename"];expected=src["md5"].upper();dst=Path(work)/base
 if dst.exists() and md5(dst)==expected:return dst
 if dst.exists():dst.unlink()
 q=find_local(rawroot,base,expected)
 if q is not None:
  shutil.copyfile(q,dst)
  if md5(dst)!=expected:raise RuntimeError("local copy MD5 mismatch")
  print("VALID_SOURCE_LOCAL_REUSE",base,flush=True);return dst
 part=dst.with_suffix(dst.suffix+".partial");curl=shutil.which("curl.exe") or shutil.which("curl")
 if not curl:raise RuntimeError("curl not found")
 for k in range(1,41):
  off=part.stat().st_size if part.exists() else 0
  print(f"VALID_DOWNLOAD_BEGIN {base} pass={k}/40 offset={off}",flush=True)
  cp=subprocess.run([curl,"--location","--fail","--http1.1","--connect-timeout","30","--speed-limit","1024","--speed-time","120","--max-time","900","--continue-at","-","--output",str(part),src["hdf5_url"]])
  now=part.stat().st_size if part.exists() else 0
  print(f"VALID_DOWNLOAD_END {base} pass={k}/40 exit={cp.returncode} bytes={now}",flush=True)
  if cp.returncode==0:
   if md5(part)==expected:os.replace(part,dst);print("VALID_DOWNLOAD_VERIFY_PASS",base,flush=True);return dst
   part.unlink(missing_ok=True);continue
  if cp.returncode in (2,3,4,23,26,27,33):raise RuntimeError(f"fatal curl {cp.returncode}")
  time.sleep(5)
 raise RuntimeError(f"download retries exhausted {base}")
def strain(h):
 if "strain" in h and "Strain" in h["strain"]:return h["strain"]["Strain"]
 c=[]
 def v(n,o):
  if isinstance(o,h5py.Dataset) and o.ndim==1:c.append((n,o))
 h.visititems(v)
 for n,o in c:
  if n.lower().endswith("strain"):return o
 if len(c)==1:return c[0][1]
 raise RuntimeError("strain dataset not found")
def piece(path,src,lo,hi,fs):
 with h5py.File(path,"r") as h:
  d=strain(h);dur=float(src["duration_s"])
  if abs(d.shape[0]/dur-fs)>1e-6:raise RuntimeError("sample rate mismatch")
  g=float(src["gps_start"]);return np.asarray(d[int(round((lo-g)*fs)):int(round((hi-g)*fs))],dtype=np.float64)
def transform(ref,paths,M,helper):
 s=BR[ref["branch"]];fs=s["fs"];a=ref["gps"]-CONTEXT;z=ref["gps"]+TARGET;xs=[];last=None
 for b in ref["sources"]:
  q=M[b];g=float(q["gps_start"]);e=g+float(q["duration_s"]);lo=max(a,g);hi=min(z,e)
  if hi<=lo:continue
  if last is not None and abs(lo-last)>.5/fs:raise RuntimeError("noncontiguous")
  xs.append(piece(paths[b],q,lo,hi,fs));last=hi
 raw=np.concatenate(xs) if len(xs)>1 else xs[0]
 if len(raw)!=int(round(68*fs)) or not np.isfinite(raw).all():raise RuntimeError("raw gate")
 morph,_=helper.deterministic_whiten(raw[:int(64*fs)],raw[int(64*fs):],fs,s["band"])
 tf,_,_=helper.r1t_stft(morph,fs,s["band"],s["nperseg"],s["hop"],s["nfft"])
 return morph.astype(np.float32),tf.astype(np.float32)
def materialize(sel,M,helper,panel,work,rawroot):
 meta={}
 for gn,r in sorted(sel.items()):
  cp=Path(panel)/(safe(gn)+".npz")
  if cp.exists():
   z=np.load(cp,allow_pickle=False)
   if z["t"].shape[0]!=32:raise RuntimeError("panel cache shape")
   meta[gn]={"mode":"cache","sha256":fsha(cp)};continue
  req=sorted({b for ss in r["required_hdf5_basenames_per_window"] for b in ss},key=lambda b:int(M[b]["gps_start"]));paths={}
  try:
   for b in req:paths[b]=acquire(M[b],work,rawroot)
   ts=[];fs=[]
   for i,(gps,ss) in enumerate(zip(r["target_gps_starts"],r["required_hdf5_basenames_per_window"])):
    t,f=transform({"branch":r["branch"],"gps":float(gps),"sources":sorted(ss,key=lambda b:int(M[b]["gps_start"]))},paths,M,helper);ts.append(t);fs.append(f)
    if (i+1)%8==0:print(f"VALID_MATERIALIZE {gn} {i+1}/32",flush=True)
   tmp=cp.with_suffix(".tmp")
   with tmp.open("wb") as h:np.savez(h,t=np.stack(ts),f=np.stack(fs))
   os.replace(tmp,cp);meta[gn]={"mode":"materialized","sha256":fsha(cp)}
  finally:
   for p in paths.values():p.unlink(missing_ok=True)
 return meta
def model_load(mm,ck):
 x=torch.load(ck,map_location="cpu",weights_only=False);m=mm.F2RepresentationModel().float();m.load_state_dict(x["model"]);m.eval();return m
@torch.no_grad()
def emb(m,t,f,l2=False):
 o=m(torch.from_numpy(np.asarray(t,np.float32)).unsqueeze(0),torch.from_numpy(np.asarray(f,np.float32)).unsqueeze(0))
 return o["embedding_l2" if l2 else "embedding"].squeeze(0).cpu().numpy().astype(float)
def panel_emb(m,panel,sel):
 E=[];EL=[]
 for gn,r in sorted(sel.items()):
  z=np.load(Path(panel)/(safe(gn)+".npz"),allow_pickle=False)
  for i in range(32):E.append(emb(m,z["t"][i],z["f"][i],False));EL.append(emb(m,z["t"][i],z["f"][i],True))
 return np.stack(E),np.stack(EL)
def cka(X,Y):
 X=X-X.mean(0);Y=Y-Y.mean(0);return float(np.linalg.norm(X.T@Y,"fro")**2/max(np.linalg.norm(X.T@X,"fro")*np.linalg.norm(Y.T@Y,"fro"),1e-30))
def robust(x):
 x=np.asarray(x,float);x-=np.median(x);sc=1.4826*np.median(np.abs(x));sc=sc if sc>1e-6 else max(np.std(x),1e-6);return (x/sc).astype(np.float32)
def stft(x,br,helper):
 s=BR[br];z,_,_=helper.r1t_stft(x,s["fs"],s["band"],s["nperseg"],s["hop"],s["nfft"]);return z.astype(np.float32)
def ridge(X,y,a=1.):
 mu=X.mean(0);sd=X.std(0);sd=np.where(sd>1e-8,sd,1.);Z=(X-mu)/sd;A=np.c_[Z,np.ones(len(Z))];R=np.eye(A.shape[1]);R[-1,-1]=0.;w=np.linalg.solve(A.T@A+a*R,A.T@y);return mu,sd,w
def pred(q,X):
 mu,sd,w=q;return np.c_[(X-mu)/sd,np.ones(len(X))]@w
def auc(y,s):
 r=rankdata(s);n1=np.sum(y==1);n0=np.sum(y==0);return float((r[y==1].sum()-n1*(n1+1)/2)/(n1*n0))
def spear(a,b):
 ra=rankdata(a);rb=rankdata(b);return 0. if np.std(ra)<1e-12 or np.std(rb)<1e-12 else float(np.corrcoef(ra,rb)[0,1])
def g03(m,base,panel,sel):
 ss=[]
 for gn,r in sorted(sel.items()):
  z=np.load(Path(panel)/(safe(gn)+".npz"),allow_pickle=False);seq=asint(r.get("sequence"),-1)
  for i in range(32):
   a,b=base.views(z["t"][i],z["f"][i],r["branch"],20260919,0,seq,i,True);e1=emb(m,a[0],a[1],True);e2=emb(m,b[0],b[1],True);ss.append(np.dot(e1,e2)/max(np.linalg.norm(e1)*np.linalg.norm(e2),1e-30))
 return np.asarray(ss)
def g04set(br,task,helper):
 rng=np.random.default_rng(EVAL_SEED+(100 if br=="high" else 0)+(1000 if task!="chirp_reverse" else 0));fs=BR[br]["fs"];t=np.arange(BR[br]["temporal"])/fs;X=[];y=[]
 for _ in range(48):
  ph=rng.uniform(0,2*np.pi);noise=rng.normal(0,.10,len(t))
  if task=="chirp_reverse":
   f0,f1=(rng.uniform(80,260),rng.uniform(700,1300)) if br=="low_mid" else (rng.uniform(1800,2600),rng.uniform(3600,4800));k=(f1-f0)/4;x=np.sin(2*np.pi*(f0*t+.5*k*t*t)+ph)+noise;a=robust(x);b=robust(x[::-1].copy())
  else:
   fc=rng.uniform(120,900) if br=="low_mid" else rng.uniform(2200,4400);fm=rng.uniform(1.5,8);d=rng.uniform(.35,.9);car=np.sin(2*np.pi*fc*t+ph);a=robust((1+d*np.sin(2*np.pi*fm*t+rng.uniform(0,2*np.pi)))*car+noise);b=robust(car+noise)
  X.extend([(a,stft(a,br,helper)),(b,stft(b,br,helper))]);y.extend([1,0])
 return X,np.array(y)
def g04(m,br,task,helper):
 X,y=g04set(br,task,helper);E=np.stack([emb(m,t,f) for t,f in X]);tr=np.arange(48);te=np.arange(48,96);return auc(y[te],pred(ridge(E[tr],2*y[tr]-1),E[te]))
def g05set(f1,helper):
 rng=np.random.default_rng(EVAL_SEED+5000);t=np.arange(16384)/4096.;X=[];Y=[]
 for _ in range(96):
  rep,mod,slope,tone=rng.random(4);coh=.15+.75*slope;auxc=.1+.8*tone;f0=55+55*slope;f_end=170+210*slope;k=(f_end-f0)/4
  chirp=np.sin(2*np.pi*(f0*t+.5*k*t*t)+rng.uniform(0,2*np.pi));car=np.sin(2*np.pi*(120+180*tone)*t+rng.uniform(0,2*np.pi));env=1+(.1+.8*mod)*np.sin(2*np.pi*(1.5+5*mod)*t+rng.uniform(0,2*np.pi));pulse=np.zeros_like(t);spacing=.35+.75*(1-rep)
  for c in np.arange(.35,3.8,spacing):pulse+=np.exp(-.5*((t-c)/(.012+.025*(1-rep)))**2)
  h=robust(chirp+.45*env*car+(.15+.75*rep)*pulse+.12*rng.normal(size=len(t)));lag=int(rng.integers(-20,21));ind=robust(rng.normal(size=len(t)));l=coh*np.roll(h,lag)+math.sqrt(max(1-coh*coh,1e-6))*ind;aux=auxc*h+math.sqrt(max(1-auxc*auxc,1e-6))*robust(rng.normal(size=len(t)))
  feat=f1.extract_classical_features({"H1":h[::4].astype(float),"L1":l[::4].astype(float)},1024.,aux_by_detector={"H1":{"SAFE":aux[::4].astype(float)},"L1":{}})
  X.append((h,stft(h,"low_mid",helper)));Y.append(f1.vectorize(feat))
 return X,np.stack(Y)
def g05(m,f1,helper):
 X,Y=g05set(f1,helper);E=np.stack([emb(m,t,f) for t,f in X]);tr=np.arange(48);te=np.arange(48,96);out=[]
 for j in range(6):out.append(abs(spear(Y[te,j],pred(ridge(E[tr],Y[tr,j]),E[te]))))
 return out
def main():
 ap=argparse.ArgumentParser()
 for n in ("model","helper","base_trainer","f1","valid","sources","raw_root","raw_work","panel_root","state","out"):ap.add_argument("--"+n.replace("_","-"),dest=n,type=Path,required=True)
 for s in SEEDS:ap.add_argument(f"--ck-{s}",dest=f"ck_{s}",type=Path,required=True)
 a=ap.parse_args();[p.mkdir(parents=True,exist_ok=True) for p in (a.raw_work,a.panel_root,a.state,a.out)]
 torch.set_num_threads(4);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)
 helper=loadpy(a.helper,"gp");mm=loadpy(a.model,"gm");base=loadpy(a.base_trainer,"gb");f1=loadpy(a.f1,"gf1")
 if tuple(f1.FEATURE_ORDER)!=("tf_excess","coherence","two_detector_residual","repetition","modulation","instrumental"):raise RuntimeError("F1 feature order mismatch")
 sel=select_panel(rows(a.valid));sp=a.state/"EXTERNAL_VALID_PANEL_SELECTION.json";now={k:asint(v.get("sequence"),-1) for k,v in sel.items()}
 if sp.exists():
  if json.loads(sp.read_text())["group_sequence"]!=now:raise RuntimeError("VALID panel drift")
 else:sp.write_text(json.dumps({"status":"FROZEN_EXTERNAL_VALID_PANEL_V1","group_sequence":now},indent=2,sort_keys=True),encoding="utf-8")
 meta=materialize(sel,man(a.sources),helper,a.panel_root,a.raw_work,a.raw_root);(a.out/"VALID_PANEL_MATERIALIZATION.json").write_text(json.dumps(meta,indent=2,sort_keys=True),encoding="utf-8");print("EXTERNAL_VALID_PANEL_PASS",flush=True)
 models={};E={};EL={}
 for s in SEEDS:
  models[s]=model_load(mm,getattr(a,f"ck_{s}"));E[s],EL[s]=panel_emb(models[s],a.panel_root,sel);np.savez(a.out/f"VALID_EMBEDDINGS_SEED_{s}.npz",embedding=E[s],embedding_l2=EL[s])
 g1={str(s):{"fraction":float(np.mean(E[s].std(0,ddof=1)>=.10)),"median_std":float(np.median(E[s].std(0,ddof=1)))} for s in SEEDS};g1a=float(np.median([x["fraction"] for x in g1.values()]));p1=g1a>=.95
 pairs={f"{x}_{y}":cka(E[x],E[y]) for x,y in ((20260919,20260920),(20260919,20260921),(20260920,20260921))};g2=float(np.median(list(pairs.values())));p2=g2>=.70
 g3d={};alls=[]
 for s in SEEDS:q=g03(models[s],base,a.panel_root,sel);g3d[str(s)]={"median":float(np.median(q))};alls+=q.tolist()
 g3=float(np.median(alls));p3=g3>=.80
 g4d={}
 for s in SEEDS:
  g4d[str(s)]={}
  for br in ("low_mid","high"):g4d[str(s)][br]={t:g04(models[s],br,t,helper) for t in ("chirp_reverse","modulated_demodulated")}
 g4m={t:float(np.median([g4d[str(s)][br][t] for s in SEEDS for br in ("low_mid","high")])) for t in ("chirp_reverse","modulated_demodulated")};p4=all(v>=.80 for v in g4m.values())
 names=list(f1.FEATURE_ORDER);g5d={str(s):dict(zip(names,g05(models[s],f1,helper))) for s in SEEDS};g5={n:float(np.median([g5d[str(s)][n] for s in SEEDS])) for n in names};count=sum(v>=.50 for v in g5.values());p5=count>=4
 status="PASS" if all((p1,p2,p3,p4,p5)) else ("HOLD" if p1 and p3 and p4 else "FAIL")
 R={"status":status,"G01":{"pass":p1,"aggregate_fraction":g1a,"threshold":.95,"per_seed":g1},"G02":{"pass":p2,"median_pairwise_linear_CKA":g2,"threshold":.70,"pairs":pairs},"G03":{"pass":p3,"median_cosine":g3,"threshold":.80,"per_seed":g3d},"G04":{"pass":p4,"threshold_AUROC":.80,"task_median_AUROC":g4m,"detail":g4d},"G05":{"pass":p5,"threshold_abs_spearman":.50,"required_features":4,"passing_features":count,"feature_median_abs_rho":g5,"detail":g5d},"external_validation_windows":320,"zero_lag":False,"retuned":False}
 (a.out/"G01_G05_RESULT.json").write_text(json.dumps(R,indent=2,sort_keys=True),encoding="utf-8")
 for k in ("G01","G02","G03","G04","G05"):print(k+"_RESULT",json.dumps(R[k],sort_keys=True),flush=True)
 print("T0_F2_G01_G05_TERMINAL",status,flush=True)
if __name__=="__main__":main()