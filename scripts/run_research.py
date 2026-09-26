#!/usr/bin/env python3
"""Bounded audit-led numerical research, not a resumed DR8 production run."""
from __future__ import annotations
import argparse,concurrent.futures,hashlib,json,os,platform,sys,time,traceback
from pathlib import Path
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[name]='1'
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from bass_he.geometry import EvidenceCache,atomic_json,contour_geometry,radial_quadrature
from bass_he.spectral import find_exceptional_point,monodromy
from bass_he.rotation import full_rotation_batch
from bass_he.transport import apply_eq50
from arseny_reimpl.eq50_scoped import ordered_scoped_branches,branch_state_indices
from arseny_reimpl.cross_section import projectile_velocity_au
from arseny_reimpl.rotational import full_rotational_probability
from run_contract import bind_run,run_lock,snapshot_geometry

REF_DELTA={'Q12':1.42615,'Q23':.32002,'Qother':.48038,'Qm1':.68560,'S23':.46940}
BRANCHES=ordered_scoped_branches()


def source_identity():
    h=hashlib.sha256()
    for p in sorted((ROOT/'src').rglob('*.py')):
        h.update(str(p.relative_to(ROOT)).encode()+b'\0'+p.read_bytes())
    return h.hexdigest()


def geometry_worker(job):
    name,ep,rho,panels=job;t=time.perf_counter()
    try:
        result=contour_geometry(ep,rho,panels=panels)
        return dict(branch=name,rho=rho,panels=panels,status='SUCCESS',result=result,elapsed_s=time.perf_counter()-t)
    except Exception:
        return dict(branch=name,rho=rho,panels=panels,status='FAILED',traceback=traceback.format_exc(),elapsed_s=time.perf_counter()-t)


def assembly(ep_map,geometry,energies,rhos,*,steps=32):
    E=np.array(energies,float);r=np.array(rhos,float);nr=len(r);ne=len(E)
    delta=np.zeros((nr,len(BRANCHES)));active=np.zeros_like(delta,dtype=bool)
    for i,rho in enumerate(r):
        for k,branch in enumerate(BRANCHES):
            active[i,k]=rho<=branch.support_cutoff
            if active[i,k]:delta[i,k]=geometry[(branch.name,float(rho))]['delta']
    batchE=np.tile(E,nr);batchR=np.repeat(r,ne)
    prot=full_rotation_batch(3,batchE,batchR,steps=steps)
    v=np.array([projectile_velocity_au(x) for x in batchE]);d=np.repeat(delta,ne,axis=0);mask=np.repeat(active,ne,axis=0)
    events=[]
    for b in BRANCHES:
        i,j=branch_state_indices(b);events.append((i-1,j-1,b.state_b[0]==3))
    # Initial H(1s) = united-atom 2p sigma, j=3 => zero-based index 2.
    initial=np.eye(10)[:,[2]]
    out={}
    for factor in (1,2):
        p=np.where(mask,np.exp(-factor*d/v[:,None]),0.)
        y=apply_eq50(p,events,prot,initial)[...,0].reshape(nr,ne,10)
        out[str(factor)]=y
    return out


def execute(args):
    out=Path(args.out)
    sid=source_identity();env=dict(numpy=np.__version__,python=platform.python_version(),machine=platform.machine())
    binding=dict(stage=args.stage,panels=args.panels,quadrature_order=args.order,source_sha256=sid,environment=env,
                 runner_sha256=hashlib.sha256(Path(__file__).read_bytes()+Path(__file__).with_name('run_contract.py').read_bytes()).hexdigest())
    bind_run(out,binding,resume=args.resume)
    cache=EvidenceCache(args.cache_dir or out/'cache');eps={};ep_details=[]
    atomic_json(out/'RUN_SPEC.json',dict(**binding,workers=args.workers,claimed_scope='audit-led bounded research pilot; no production'))
    for b in BRANCHES:
        key=dict(source=sid,environment=env,kind='EP_MONODROMY',name=b.name,depth=96)
        cached=cache.get(key)
        if cached is None:
            t=time.perf_counter()
            try:
                ep=find_exceptional_point(b.state_a,b.state_b,b.R,depth=96)
                mon=monodromy(ep,steps=64,radius=.01)
                if not mon['passed']:raise RuntimeError('monodromy failed')
                cached=dict(ep=ep,monodromy=mon,reference_distance=abs(ep['R']-b.R),elapsed_s=time.perf_counter()-t)
                cache.put(key,cached)
            except Exception:
                atomic_json(out/f'FAIL_EP_{b.name}.json',dict(status='FAILED',traceback=traceback.format_exc()));raise
        eps[b.name]=cached['ep'];ep_details.append(dict(branch=b.name,**cached))
        atomic_json(out/'EP_CERTIFICATES.json',ep_details)
        print('EP',b.name,'R=',cached['ep']['R'],'reference delta=',cached['reference_distance'],flush=True)
    if args.stage=='pilot':
        rhos=np.array([0.,.3]);weights=None
    else:
        # Every frozen support jump AND rotational matching boundary is a split.
        from arseny_reimpl.rotational import s_sigma_boundary
        cuts=sorted(set([0.,s_sigma_boundary(1),s_sigma_boundary(2)]+[b.support_cutoff for b in BRANCHES]))
        rhos,weights=radial_quadrature(cuts,order=args.order)
        atomic_json(out/'QUADRATURE_NODES.json',dict(cutoffs=cuts,rhos=rhos,weights_a0sq=weights,order=args.order))
    jobs=[];geometry={};completed=[]
    for rho in rhos:
        for b in BRANCHES:
            if rho>b.support_cutoff:continue
            key=dict(source=sid,environment=env,kind='CONTOUR',name=b.name,rho=float(rho),panels=args.panels,depth=96)
            cached=cache.get(key)
            if cached is not None:
                geometry[(b.name,float(rho))]=cached['result'];completed.append(cached)
            else:jobs.append((b.name,eps[b.name],float(rho),args.panels))
    def accept(result):
        completed.append(result)
        if result['status']=='SUCCESS':
            key=dict(source=sid,environment=env,kind='CONTOUR',name=result['branch'],rho=result['rho'],panels=result['panels'],depth=96)
            cache.put(key,result);geometry[(result['branch'],result['rho'])]=result['result']
        snapshot_geometry(out,completed,attempt=result)
        print('CONTOUR',result['branch'],result['rho'],result['status'],round(result['elapsed_s'],3),flush=True)
    t=time.perf_counter()
    if args.workers==1:
        for job in jobs:accept(geometry_worker(job))
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
            futures=[pool.submit(geometry_worker,job) for job in jobs]
            for future in concurrent.futures.as_completed(futures):accept(future.result())
    elapsed=time.perf_counter()-t
    snapshot_geometry(out,completed)
    failed=[x for x in completed if x['status']!='SUCCESS']
    summary=dict(stage=args.stage,geometry_jobs=len(completed),new_geometry_jobs=len(jobs),failed_jobs=len(failed),
                 geometry_wall_s=elapsed,workers=args.workers,source_sha256=sid,
                 production_claim=False,exponent_policy_resolved=False)
    if failed:
        summary['status']='UNRESOLVED_GEOMETRY';atomic_json(out/'SUMMARY.json',summary);return 2
    values=assembly(eps,geometry,[.5,5.],rhos)
    cols={}
    for factor,ys in values.items():
        cols[factor]=dict(max_column_sum_defect=float(np.max(abs(ys.sum(-1)-1))),minimum=float(ys.min()),probabilities=ys)
    atomic_json(out/'INITIAL_COLUMN_OUTPUTS.json',dict(energies_keV_u=[.5,5.],rhos=rhos,lanes=cols,
         observable='indexed-state probabilities with inherited upper-shell absorbing rule; no disjoint physical channel assignment'))
    if args.stage=='pilot':
        summary['source_delta_errors']={b.name:abs(geometry[(b.name,0.)]['delta']-REF_DELTA[b.name])/REF_DELTA[b.name] for b in BRANCHES}
        # Paired workload and explicit accuracy, no inflated end-to-end speed claim.
        energies=np.tile([.5,5.],3);rs=np.repeat([.1,.3,.5],2)
        times_old=[];times_new=[]
        for _ in range(3):
            t=time.perf_counter();old=np.array([full_rotational_probability(3,E,r,steps=512) for E,r in zip(energies,rs)])
            times_old.append(time.perf_counter()-t)
            t=time.perf_counter();new=full_rotation_batch(3,energies,rs,steps=32);times_new.append(time.perf_counter()-t)
        finer=full_rotation_batch(3,energies,rs,steps=64)
        summary['rotation_benchmark']=dict(workload='six Nmax3 matrices',legacy_steps=512,new_steps=32,
            legacy_median_s=float(np.median(times_old)),new_batch_median_s=float(np.median(times_new)),
            median_speedup=float(np.median(times_old)/np.median(times_new)),
            max_difference_vs_legacy512=float(np.max(abs(new-old))),
            max_difference_new32_vs_new64=float(np.max(abs(new-finer))))
    else:
        sigma={}
        for factor,ys in values.items():
            off=ys.copy();off[:,:,2]=0.
            area=np.einsum('r,rej->ej',weights,off)
            sigma[factor]=dict(indexed_transition_areas_a0sq=area,reaction_loss_area_a0sq=area.sum(-1))
        atomic_json(out/'SCOPED_EQ54_PILOT.json',dict(energies_keV_u=[.5,5.],lanes=sigma,
          quadrature_order=args.order,claim='FINITE_INDEXED_STATE_PILOT_NOT_CONVERGED_NOT_PHYSICAL_CHANNEL_CROSS_SECTION',
          elastic_cross_section_computed=False,production=False))
    summary['status']='BOUNDED_PILOT_COMPLETE'
    atomic_json(out/'SUMMARY.json',summary);print(json.dumps(summary,indent=2),flush=True)
    return 0

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='runs/research_v2');ap.add_argument('--workers',type=int,default=2)
    ap.add_argument('--stage',choices=['pilot','quadrature'],default='pilot');ap.add_argument('--resume',action='store_true')
    ap.add_argument('--order',type=int,default=1);ap.add_argument('--panels',type=int,default=32)
    ap.add_argument('--cache-dir',default=None,help='optional shared content-addressed geometry cache')
    args=ap.parse_args()
    if not(1<=args.workers<=32):ap.error('--workers must be in 1..32')
    if args.order<1 or args.order>32:ap.error('--order must be in 1..32')
    if args.panels<8 or args.panels%2:ap.error('--panels must be even and >=8')
    with run_lock(args.out):return execute(args)

if __name__=='__main__':raise SystemExit(main())
