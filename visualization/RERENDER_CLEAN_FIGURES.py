"""Regenerate publication labels from retained numeric inputs only.

No strain, model, inference, cut or stored numerical record is changed.
"""
from pathlib import Path
import csv, hashlib, json, shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import importlib.util

HERE=Path(__file__).resolve().parent
OUT=HERE.parent/'figures'
OLD=HERE/'original_figures'
DATA=HERE/'data'
OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
def load(n):return json.loads((DATA/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
reports=[]
def save(fig,stem,inputs,checks,exts=('png','pdf','svg')):
    for ext in exts:fig.savefig(OUT/(stem+'.'+ext),dpi=220,facecolor='white',bbox_inches='tight')
    reports.append({'stem':stem,'status':'REGENERATED_FROM_UNCHANGED_NUMERICAL_INPUTS','inputs':[{ 'path':str(p.relative_to(HERE)),'sha256':sha(p)} for p in inputs],'checks':checks,'visible_text':[t.get_text() for t in fig.findobj(matplotlib.text.Text) if t.get_text()]})
    plt.close(fig)

def packets():
    counts=load('p2_counts.json');g={x['control']:x for x in counts['controls']}
    controls=['original','time_reversed','incoherent'];labels=['Original signal','Time reversed','Extra detector delays'];x=np.arange(3)
    fig,axes=plt.subplots(1,2,figsize=(12.1,4.9),sharey=True)
    numeric={}
    for ax,key,title in zip(axes,['above','upward'],['A  Threshold exceedances','B  New upward crossings from matched noise']):
        for j,(method,label,color) in enumerate([('COHERENCE','Correlation ratio','#2166ac'),('ENERGY','Energy ratio','#c26927')]):
            v=[g[c]['methods'][method][key] for c in controls];numeric[key+':'+method]=v
            bars=ax.bar(x+(j-.5)*.34,v,width=.32,color=color,label=label)
            for b,vv in zip(bars,v):ax.text(b.get_x()+b.get_width()/2,vv+.8,f'{vv}/48',ha='center',fontsize=10)
        ax.set_xticks(x,labels,rotation=10,ha='right');ax.set_ylim(0,55);ax.set_title(title,loc='left',fontsize=10);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
    assert numeric['above:COHERENCE']==[48,48,38] and numeric['upward:COHERENCE']==[40,40,30]
    axes[0].set_ylabel('Variant count (48 per control)');axes[0].legend(frameon=False,ncol=2,loc='upper left',bbox_to_anchor=(0,-.25))
    fig.suptitle('Short structured transients: threshold response and timing controls',fontsize=13)
    fig.text(.06,.02,'Twelve reused noise contexts in six source blocks; fixed cuts without matched false-alarm rates.\nBaseline-positive counts: correlation 8/48; energy 4/48. All downward crossings: zero.',fontsize=8.5)
    fig.subplots_adjust(top=.83,bottom=.32,wspace=.12)
    save(fig,'P2_DUYARLILIK_VE_KONTROLLER',[DATA/'p2_counts.json'],numeric)

def lag_plot(kind,stem,title):
    records=[load('p4_baseline.json'),load(f'p4_{kind}_original.json'),load(f'p4_{kind}_delayed.json')]
    fig,axs=plt.subplots(2,1,figsize=(10.4,7),sharex=True)
    colors=['#91989c','#287a66','#bf475e'];labels=['Unmodified noise','Original projection','Extra-delay copy'];pair='H1_L1'
    fs=records[0]['diagnostic']['rate_hz'];cap=records[0]['diagnostic']['per_pair'][pair]['physical_cap_samples']/fs*1e3
    curve_hashes=[]
    for ax,key in zip(axs,['raw_correlation','envelope_power_correlation']):
        for r,col,lab in zip(records,colors,labels):
            d=r['diagnostic']['per_pair'][pair][key];lag=np.asarray(d['lag_samples'],dtype=np.float64)/fs*1e3;y=np.asarray(d['signed_normalized_correlation'],dtype=np.float64)
            expected=float(d['broad_abs_max']);assert np.max(np.abs(y))==expected
            displayed=np.abs(y) if key=='raw_correlation' else y
            ax.plot(lag,displayed,color=col,lw=.9,label=lab)
            curve_hashes.append({'input':r['header']['noise_id'],'channel':key,'lag_samples_sha256':hashlib.sha256(np.asarray(d['lag_samples'],dtype=np.int64).tobytes()).hexdigest(),'signed_values_sha256':hashlib.sha256(y.tobytes()).hexdigest(),'broad_abs_max':expected})
        ax.axvspan(-cap,cap,color='#a9c7ad',alpha=.3,label='Light-travel interval')
        delay=records[-1]['declared_pair_source_delays_s'][pair]*1e3;ax.axvline(delay,color='#4c4141',ls='--',lw=1,label='Declared source lag')
        d=records[-1]['diagnostic']['per_pair'][pair][key];y=np.asarray(d['signed_normalized_correlation']);ix=np.argmax(np.abs(y));lag=np.asarray(d['lag_samples'])/fs*1e3
        ax.scatter(lag[ix],np.abs(y[ix]) if key=='raw_correlation' else y[ix],s=32,facecolors='none',edgecolors='black',label='Broad maximum')
        ax.grid(alpha=.16);ax.set_xlim(-350,350)
    axs[0].set_title('A  Absolute normalized correlation of whitened strain',loc='left',fontsize=11);axs[0].set_ylabel(r'$|r(\ell)|$')
    axs[1].set_title('B  Centered analytic-envelope-power correlation',loc='left',fontsize=11);axs[1].set_ylabel(r'$r_{\rm envelope}(\ell)$');axs[1].set_xlabel('Signed lag (ms); positive means H1 delayed relative to L1')
    inset=axs[0].inset_axes([.67,.50,.29,.4])
    for r,col in zip(records,colors):
        d=r['diagnostic']['per_pair'][pair]['raw_correlation'];x=np.asarray(d['lag_samples'])/fs*1e3;y=np.abs(np.asarray(d['signed_normalized_correlation']));ix=np.abs(x)<=cap;inset.plot(x[ix],y[ix],lw=.8,color=col)
    inset.set_title('Light-travel interval',fontsize=8);inset.tick_params(labelsize=8);inset.grid(alpha=.15)
    score=records[-1]['scores']['COHERENCE'];cut=load('p2_counts.json')['thresholds']['COHERENCE']['O4a']
    axs[0].text(.02,.04,f'Extra-delay correlation ratio: {score:.3f}; cut: {cut:.3f}',transform=axs[0].transAxes,fontsize=9,bbox=dict(facecolor='white',edgecolor='none',alpha=.9,pad=2))
    raw=records[-1]['diagnostic']['per_pair'][pair]['raw_correlation'];env=records[-1]['diagnostic']['per_pair'][pair]['envelope_power_correlation']
    def peak(d):return np.asarray(d['lag_samples'])[np.argmax(np.abs(d['signed_normalized_correlation']))]/fs*1e3
    axs[1].text(.02,.04,f'Envelope broad peak: {peak(env):.2f} ms; declared source lag: {delay:.2f} ms',transform=axs[1].transAxes,fontsize=9,bbox=dict(facecolor='white',edgecolor='none',alpha=.9,pad=2))
    fig.suptitle(title,fontsize=13,y=.99);h,l=axs[0].get_legend_handles_labels();fig.legend(h,l,ncol=3,loc='upper center',bbox_to_anchor=(.5,.958),frameon=False,fontsize=9)
    fig.subplots_adjust(top=.82,hspace=.23,left=.09,right=.98,bottom=.09)
    save(fig,stem,[DATA/'p4_baseline.json',DATA/f'p4_{kind}_original.json',DATA/f'p4_{kind}_delayed.json'],{'exact_original_curve_arrays_used':True,'curves':curve_hashes,'declared_delay_ms':delay,'raw_peak_ms':peak(raw),'envelope_peak_ms':peak(env),'correlation_ratio':score,'fixed_cut':cut})

def conditional():
    r=load('foreground_result.json')
    with np.load(DATA/'foreground_transform_maxima.npz',allow_pickle=False) as x:v=x['joint_maximum'].copy();obs=float(x['identity_joint_maximum'])
    strict=int(np.sum(v>obs));ties=int(np.sum(v==obs));count=strict+ties;p=(1+count)/(1+len(v));assert count==1711 and p==r['p_report']
    fig,ax=plt.subplots(figsize=(9.2,5.7));fig.subplots_adjust(left=.1,right=.97,top=.81,bottom=.21)
    lo,hi=min(v.min(),obs),max(v.max(),obs);pad=max((hi-lo)*.025,.1);bins=np.linspace(lo-pad,hi+pad,46)
    ax.hist([v[v<obs],v[v==obs],v[v>obs]],bins=bins,stacked=True,color=['#B7C6D0','#E7A64A','#28698B'],edgecolor='white',linewidth=.35,label=[f'Below observed ({len(v)-count})',f'Exact ties ({ties})',f'Above observed ({strict})'])
    ax.axvline(obs,color='#1D2429',lw=1.8,ls='--');ax.set_xlabel('Joint maximum standardized learned-ranking score');ax.set_ylabel('Number of transformations');ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True);ax.legend(frameon=False,loc='upper left',fontsize=9)
    ax.text(.98,.97,f'Observed maximum: {obs:.3f}\n{count}/4096 maxima at least as large\np = 1712/4097 = {p:.5f}\nNo rejection at alpha = 0.05',transform=ax.transAxes,ha='right',va='top',fontsize=9,bbox=dict(facecolor='white',edgecolor='#D9E0E4',boxstyle='round,pad=.6'))
    fig.text(.1,.94,'Registered conditional randomization test',fontsize=16,weight='bold');fig.text(.1,.884,'192 four-second targets (768 s); 4096 fixed within-source transformations',fontsize=10)
    fig.text(.1,.075,'Exact ties and the finite-simulation +1 correction are included.',fontsize=9);fig.text(.1,.035,'Conditional test only; no universal detector-noise false-alarm probability is established.',fontsize=9)
    save(fig,'F7_CONDITIONAL_RESULT',[DATA/'foreground_result.json',DATA/'foreground_transform_maxima.npz'],{'strict':strict,'ties':ties,'p':p,'histogram_bins':bins.tolist(),'values_sha256':hashlib.sha256(v.tobytes()).hexdigest()})

def pilot():
    r=load('pilot_result.json');a=r['assessment'];b=a['primary_blocks'];labels=[f"{v['topology']} / source {i+1}" for i,v in enumerate(b)];learned=[100*v['recovery_fraction']['F4'] for v in b];energy=[100*v['recovery_fraction']['energy'] for v in b]
    fig,(ax,ax2)=plt.subplots(1,2,figsize=(12.2,4.9),gridspec_kw={'width_ratios':[3,1.1]});x=np.arange(6);w=.34;colors=['#5B5FC7','#148879']
    for j,(values,label) in enumerate([(learned,'Learned ranking'),(energy,'Band-energy ratio')]):
        bars=ax.bar(x+(j-.5)*w,values,w,label=label,color=colors[j]);ax.bar_label(bars,fmt='%.0f%%',padding=3,fontsize=9)
    ax.set(xticks=x,xticklabels=labels,ylim=(0,112),ylabel='Prespecified response fraction (%)',title='Six physical source blocks');ax.tick_params(axis='x',labelsize=8);ax.set_yticks([0,25,50,75,100]);ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True);ax.legend(frameon=False,ncols=2,fontsize=9)
    v=[100*a['source_balanced_recovery'][k] for k in ['F4','energy']];bars=ax2.bar([0,1],v,color=colors,width=.6);ax2.bar_label(bars,labels=['12.5%','62.5%'],padding=4,fontsize=11);ax2.set(xticks=[0,1],xticklabels=['Learned\nranking','Energy\nratio'],ylim=(0,112),title='Equal source-block weighting');ax2.set_yticks([0,25,50,75,100]);ax2.grid(axis='y',alpha=.18);ax2.set_axisbelow(True)
    fig.suptitle('Strain-level pilot: limited response of the tested learned ranking',fontsize=14,weight='bold')
    fig.text(.5,.03,'64 original injections, eight reused noise contexts and six source blocks. Cuts were fixed on separate calibration records.\nThe shared-noise panel does not establish sensitivity at equal false-alarm rates.',ha='center',fontsize=9)
    fig.subplots_adjust(top=.82,bottom=.24,left=.07,right=.98,wspace=.28)
    assert v==[12.5,62.5]
    save(fig,'PILOT_RECOVERY_COMPARISON',[DATA/'pilot_result.json'],{'block_learned_percent':learned,'block_energy_percent':energy,'equal_block_percent':v})

def development():
    base=DATA/'development_receipts'
    units=[json.loads(p.read_text()) for p in sorted((base/'UNITS').glob('*.json'))];noise=[json.loads(p.read_text()) for p in sorted((base/'BASELINES').glob('*.json'))];r=load('coherence_dev_result.json');cuts=r['assessment']['thresholds'];methods=['COHERENCE','ENERGY','FROZEN_F4'];panels=[('Original injections',[v for v in units if v['variant']['control']=='original']),('Extra-delay controls',[v for v in units if v['variant']['control']=='incoherent']),('Unmodified development noise',noise)]
    fig,axs=plt.subplots(1,3,figsize=(12.2,5),sharey=True);numeric={}
    for ax,(title,rows) in zip(axs,panels):
        vals=[sum(v['scores'][m]>cuts[m][v['header']['topology']] for v in rows) for m in methods];n=len(rows);numeric[title]={'n':n,'counts':vals};ax.bar(range(3),np.asarray(vals)/n*100,color=['#138779','#D39420','#6862B9'],width=.62)
        for i,v in enumerate(vals):ax.text(i,v/n*100+3,f'{v}/{n}',ha='center',fontsize=11)
        ax.set_xticks(range(3),['Correlation\nratio','Energy\nratio','Learned\nranking']);ax.set_title(title,fontsize=10,pad=13);ax.set_ylim(0,119);ax.set_yticks([0,25,50,75,100]);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
    assert numeric['Original injections']=={'n':32,'counts':[32,24,0]}
    axs[0].set_ylabel('Threshold exceedances (%)');fig.suptitle('Paired development comparison at method-specific fixed cuts',fontsize=14,weight='bold')
    fig.text(.5,.07,'24 calibration contexts; four development contexts in two source blocks. No independent confirmation or equal false-alarm comparison.',ha='center',fontsize=8.5)
    fig.text(.5,.025,'All four accepted extra-delay controls were modulated waveforms; time-reversed signals also gave 32/32 correlation exceedances.',ha='center',fontsize=8.5)
    fig.tight_layout(rect=[0,.14,1,.92],w_pad=2)
    save(fig,'KORELASYON_DEV_KARSILASTIRMA',[DATA/'coherence_dev_result.json']+sorted((base/'UNITS').glob('*.json'))+sorted((base/'BASELINES').glob('*.json')),numeric)

def frequency():
    fig,ax=plt.subplots(figsize=(10.3,4.8));y=[3,2,1,0];labels=['Solar-mass Dyson configuration at 1 AU','Galactic-centre compact-object beacon','Tested transient-comparison band','Published warp-collapse example (1 km)']
    values=[(6.34e-8,6.34e-8),(0.00063,0.00107),(64,768),(3e5,3e5)];annot=[r'$\simeq6.34\times10^{-8}$ Hz (illustrative orbit)','0.63–1.07 mHz','64–768 Hz',r'$\simeq300$ kHz']
    for yy,(a,b),note in zip(y,values,annot):
        ax.plot([a,b],[yy,yy],lw=6,color='#246a8a',solid_capstyle='round') if a!=b else ax.scatter([a],[yy],s=40,color='#246a8a');ax.annotate(note,(a,yy),xytext=(0,10),textcoords='offset points',ha='left',fontsize=9)
    ax.set_xscale('log');ax.set_xlim(1e-9,3e7);ax.set_ylim(-.5,3.7);ax.set_yticks(y,labels);ax.set_xlabel('Characteristic gravitational-wave frequency (Hz), logarithmic scale');ax.grid(axis='x',alpha=.2);fig.suptitle('Physical example scales and the tested transient band',fontsize=13)
    fig.text(.04,.015,'Illustrative model scales, not a sensitivity curve or a source detection. Persistent signals require a suitable long-duration analysis.',fontsize=8.5);fig.tight_layout(rect=(0,.055,1,.94))
    save(fig,'FREKANS_KAPSAMI',[HERE/'original_plot_sources/physical_frequency_scope_0.py'],{'model_frequency_intervals_hz':values,'supported_model_scales_preserved':True,'removed_unsupported_illustration':{'label':'Proposed GW emitter','frequency_hz':1e9,'reason':'No supporting source among verified publication references; not a measured result'}})

def initial_timeline():
    with (DATA/'timeline_initial_scores.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
    with np.load(DATA/'foreground_transform_maxima.npz',allow_pickle=False) as n:null=n['joint_maximum'].copy();observed=float(n['identity_joint_maximum'])
    fig=plt.figure(figsize=(11,8));gs=fig.add_gridspec(3,1,height_ratios=[1,1,.8]);axs=[fig.add_subplot(gs[i]) for i in range(3)];checks={}
    for ax,run,col in zip(axs[:2],['O4a','O4b'],['#296c92','#2b805f']):
        rr=[v for v in rows if v['topology']==run];times=np.array([float(v['target_gps']) for v in rr]);scores=np.array([float(v['f4_consensus']) for v in rr]);days=(times-times.min())/86400;best=int(np.argmax(scores));ax.scatter(days,scores,s=23,color=col,alpha=.85);ax.scatter(days[best],scores[best],s=80,facecolors='none',edgecolors='#b93450');ax.set_title(f'{run}: 96 separated four-second targets; 384 s target data',loc='left',fontsize=10);ax.set_ylabel('Fixed learned-ranking score');ax.set_xlabel(f'Days from first sample (GPS {times.min():.0f})');ax.grid(axis='y',alpha=.18);ax.annotate(f'Maximum: {scores[best]:.2f}\nGPS {times[best]:.0f}',(days[best],scores[best]),xytext=(8,-24),textcoords='offset points',fontsize=8);checks[run]={'n':len(rr),'max':float(scores.max()),'times_sha256':hashlib.sha256(times.tobytes()).hexdigest(),'scores_sha256':hashlib.sha256(scores.tobytes()).hexdigest()}
    axs[2].hist(null,bins=40,color='#a5bdcc',edgecolor='white');axs[2].axvline(observed,color='#b93450',label=f'Observed maximum: {observed:.2f}');axs[2].set_xlabel('Maximum learned-ranking score over the 192 targets');axs[2].set_ylabel('Transformations');axs[2].legend(frameon=False,fontsize=9);axs[2].set_title('Existing within-source conditional comparison: p = 0.418',loc='left',fontsize=10)
    assert all(v['n']==96 for v in checks.values());fig.suptitle('Observed learned-ranking scores at their actual sample times',fontsize=14);fig.tight_layout(rect=(0,.045,1,.95),h_pad=1.8);fig.text(.07,.008,'Gaps are unobserved intervals. The 4096 conditional transformations are not independent full-search background trials.',fontsize=8.5)
    save(fig,'GW_MEVCUT_192_ZAMAN_SKOR',[DATA/'timeline_initial_scores.csv',DATA/'foreground_transform_maxima.npz'],checks)

def survey_injections():
    """Call the exact original heatmap recipe with label-only corrections."""
    spec=importlib.util.spec_from_file_location('original_survey_figure_recipe',HERE/'original_plot_sources/EXPORT_SURVEY_FIGURES.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    result=load('survey_injection_result.json');original_save=matplotlib.figure.Figure.savefig
    numeric=[]
    def label_only_save(fig,path,*args,**kwargs):
        for item in fig.findobj(matplotlib.text.Text):
            v=item.get_text()
            v=v.replace('Fraction of eligible source contexts','Fraction of planned source contexts')
            title_map={
                'Feature screen: context new crossings':'Feature statistic\nNew context crossings',
                'Energy: context new crossings':'Log-energy ratio\nNew context crossings',
                'Feature screen: group new crossings':'Feature statistic\nNew group crossings',
                'Energy: group new crossings':'Log-energy ratio\nNew group crossings',
            }
            v=title_map.get(v,v)
            item.set_text(v)
        if not numeric:
            numeric.extend(np.asarray(ax.images[0].get_array()).tolist() for ax in fig.axes if ax.images)
        return original_save(fig,path,*args,**kwargs)
    matplotlib.figure.Figure.savefig=label_only_save
    try:module.injection_plot(result,OUT)
    finally:matplotlib.figure.Figure.savefig=original_save
    assert len(numeric)==4
    reports.append({'stem':'CPU4096_INJECTION_RESPONSE','status':'ORIGINAL_RECIPE_LABEL_ONLY_ADAPTER','inputs':[{'path':'data/survey_injection_result.json','sha256':sha(DATA/'survey_injection_result.json')},{'path':'original_plot_sources/EXPORT_SURVEY_FIGURES.py','sha256':sha(HERE/'original_plot_sources/EXPORT_SURVEY_FIGURES.py')}],'checks':{'all_four_original_heatmap_arrays':numeric,'denominator_label':'planned source contexts, retaining already-positive group opportunities in the denominator'},'visible_text_corrections':['eligible source contexts -> planned source contexts','Feature screen -> Feature statistic','Energy -> Log-energy ratio','All four panel titles wrapped into two lines to avoid colorbar collision']})

def main():
    for p in OLD.iterdir():
        if p.is_file():shutil.copy2(p,OUT/p.name)
    packets();lag_plot('p2','P4_ACTUAL_P2_DELAYS',r'Phase-coded packet ($h_{\rm rss}=10^{-20}$ Hz$^{-1/2}$)');lag_plot('p3','P4_ACTUAL_P3_DELAYS',r'Rocket–exhaust memory ($T=0.01$ s)');conditional();pilot();development();frequency();initial_timeline();survey_injections()
    (HERE.parent/'FIGURE_LANGUAGE_AUDIT.json').write_text(json.dumps({'status':'PASS_REGENERATED_LABELS_FROM_RETAINED_DATA','regenerated_figures':reports,'new_strain_or_neural_computations':0,'source_data_changed':False},indent=2)+'\n')
    print(json.dumps({'redrawn':len(reports),'out':str(OUT)}))

if __name__=='__main__':main()
