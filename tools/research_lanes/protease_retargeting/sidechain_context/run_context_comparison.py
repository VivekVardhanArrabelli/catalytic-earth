#!/usr/bin/env python3
"""Eight fixed-backbone sequence assignments and80 unconditioned RF3 outputs.

No provisioning, download, retry, replacement or backbone generation. The
completed water-conditioning experiment is imported unchanged as a consumer.
"""
import argparse,hashlib,json,os,signal,subprocess,sys,time,traceback
from pathlib import Path
COMMON=Path(__file__).resolve().parents[1]/'water_conditioning'
sys.path.insert(0,str(COMMON))
import run_prospective_designs as old
SCAFFOLD_SHA='1e764d610d69a29b76b942c625b6950ec0eb4f4ca0ea30cc0b2fc91cdd11bca2'
MPNN_SHA='161cd264061fda9680cbb940255522ae42f2966c552d045d87913d9452a80970'
SEEDS=(200,201,202,203)

def assignments(scaffold):
    base=old.assigned_manifest();base['question']='Fixed-sidechain geometric context during sequence design on one retained scaffold'
    base['selection']='Scaffold water_fixed_seed3 selected post hoc from previous completed experiment; new paired sequence seeds'
    base['candidates']=[]
    for seed in SEEDS:
        for revealed in (False,True):
            arm='context_revealed' if revealed else 'context_hidden';cid=f'{arm}_seed{seed}'
            base['candidates'].append({'id':cid,'arm':arm,'pair_seed':seed,'mpnn_seed':seed,'atomize_side_chains':revealed,'status':'assigned_not_started','enzyme_sequence':None,'enzyme_sha256':None,'scaffold_path':str(scaffold),'scaffold_sha256':SCAFFOLD_SHA,'mpnn_output_path':None,'rf3_input_paths':{'monomer':None,'ES':None},'rf3_output_dirs':{'monomer':None,'ES':None},'rf3_assignments':[{'state':state,'seed':0,'sample':sample,'status':'assigned_not_started','path':None} for state in ('monomer','ES') for sample in range(5)]})
    return base

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for name in ('foundry-root','out-dir','checkpoint-dir','checkpoint-receipt','native-context-receipt'):ap.add_argument('--'+name,type=Path)
    ap.add_argument('--execute',action='store_true');ap.add_argument('--max-seconds',type=int,default=5400);args=ap.parse_args()
    package=Path(__file__).resolve().parent;scaffold=package/'selected_scaffold.cif.gz'
    old.require(args.out_dir and args.foundry_root,'out-dir and foundry-root required')
    out=args.out_dir.resolve();out.mkdir(parents=True,exist_ok=False);manifest=assignments(scaffold);mp=out/'candidate_manifest.json';old.save(mp,manifest)
    old.require(old.digest(scaffold)==SCAFFOLD_SHA,'Selected scaffold changed')
    old.require(old.digest(COMMON/'run_prospective_designs.py')=='61941360db3d14939a3f35649f88ac06a1b021244f1ab4390d7b7922fae1be42','Shared frozen consumer changed')
    pins=json.loads((package/'consumer_source_pins.json').read_text())
    for relative,pin in pins['files'].items():old.require(old.digest(args.foundry_root/relative)==pin,f'Native consumer changed:{relative}')
    manifest.update(runner_sha256=old.digest(__file__),shared_consumer_sha256=old.digest(COMMON/'run_prospective_designs.py'),decision_sha256=old.digest(package/'prospective_context_comparison.json'),consumer_source_pins_sha256=old.digest(package/'consumer_source_pins.json'));old.save(mp,manifest)
    if not args.execute:return print(f'Prepared all8 assignments without model execution:{mp}')
    old.require(1<=args.max_seconds<=6600,'Run must leave retrieval reserve inside2-hour cap')
    old.require(args.checkpoint_dir and args.checkpoint_receipt and args.native_context_receipt,'Native context and checkpoint receipts required')
    receipt=json.loads(args.native_context_receipt.read_text());old.require(receipt.get('status')=='passed_native_context_pair' and receipt.get('model_execution') is False,'Actual native context pair has not passed')
    old.require(receipt.get('scaffold_sha256')==SCAFFOLD_SHA,'Context gate used different scaffold')
    manifest['native_context_receipt']={'path':str(args.native_context_receipt.resolve()),'sha256':old.digest(args.native_context_receipt)}
    checks={r['file']:r for r in json.loads(args.checkpoint_receipt.read_text())['checkpoints']};ckpts={}
    for model,expected in [('mpnn',MPNN_SHA),('rf3',old.RF3_SHA)]:
        name,size=old.WEIGHTS[model];p=args.checkpoint_dir.resolve()/name;old.require(p.stat().st_size==size and old.digest(p)==expected==checks[name]['sha256'],f'Checkpoint changed:{name}');ckpts[model]=str(p)
    manifest['checkpoint_receipts']=list(checks.values());old.save(mp,manifest)
    env=os.environ.copy();old.require(not env.get('LOCAL_MSA_DIRS'),'Unset LOCAL_MSA_DIRS');env['PYTHONPATH']=os.pathsep.join(str(args.foundry_root.resolve()/s) for s in ('src','models/mpnn/src','models/rf3/src','models/rfd3/src'))
    deadline=time.monotonic()+args.max_seconds;commands=[]
    def command(tokens,label):
        remaining=deadline-time.monotonic();old.require(remaining>0,'Runtime exhausted');log=out/'logs'/f'{label}.log';log.parent.mkdir(exist_ok=True);row={'label':label,'argv':[str(t) for t in tokens],'started_unix':time.time(),'status':'running'};commands.append(row);old.save(out/'commands.json',commands)
        with log.open('w') as f:
            proc=subprocess.Popen(row['argv'],stdout=f,stderr=subprocess.STDOUT,env=env,start_new_session=True)
            try:code=proc.wait(timeout=remaining)
            except (subprocess.TimeoutExpired,KeyboardInterrupt):
                os.killpg(proc.pid,signal.SIGTERM)
                try:proc.wait(timeout=10)
                except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
                row.update(status='stopped_at_runtime_limit_or_interrupt',returncode=proc.returncode,finished_unix=time.time());old.save(out/'commands.json',commands);raise
        row.update(status='completed' if code==0 else 'failed',returncode=code,finished_unix=time.time());old.save(out/'commands.json',commands);old.require(code==0,f'Native stage{label} failed; see{log}')
    try:
        for c in manifest['candidates']:
            d=out/'candidates'/c['id'];d.mkdir(parents=True)
            try:
                cfg={'model_type':'ligand_mpnn','checkpoint_path':ckpts['mpnn'],'is_legacy_weights':True,'out_directory':str(d/'mpnn'),'write_fasta':True,'write_structures':True,'inputs':[{'structure_path':str(scaffold),'name':c['id'],'seed':c['mpnn_seed'],'batch_size':1,'number_of_batches':1,'temperature':0.1,'structure_noise':0.0,'atomize_side_chains':c['atomize_side_chains'],'remove_ccds':[],'remove_waters':False,'fixed_residues':[f'A{r}' for r in old.ROLES]+[f'B{r}' for r in range(1,13)]}]}
                config=d/'mpnn_config.json';old.save(config,cfg)
                command([sys.executable,COMMON/'run_prospective_designs.py','--worker','mpnn-gate','--worker-config',config],c['id']+'_mpnn_gate')
                c['status']='mpnn_started';old.save(mp,manifest)
                command([sys.executable,'-m','mpnn.inference','--config_json',config],c['id']+'_mpnn')
                structure=d/'mpnn'/f'{c["id"]}_b0_d0.cif';old.require(structure.exists() and len(list(structure.parent.glob('*.cif')))==1,'Exactly one sequence-design output required')
                for path in reversed(env['PYTHONPATH'].split(os.pathsep)):
                    if path not in sys.path:sys.path.insert(0,path)
                report=old.identities(old.native_array(structure));old.save(d/'mpnn_output_identity.json',report);enzyme=report['sequences']['A'];c.update(status='sequence_ready',enzyme_sequence=enzyme,enzyme_sha256=hashlib.sha256(enzyme.encode()).hexdigest(),mpnn_output_path=str(structure),mpnn_output_sha256=old.digest(structure))
                for state in ('monomer','ES'):
                    name=f'{c["id"]}_{state}';components=[{'seq':enzyme,'chain_id':'A'}]
                    if state=='ES':components += [{'seq':old.TARGET,'chain_id':'B'},{'smiles':'[Zn+2].O','chain_id':'C'}]
                    path=d/f'rf3_{state}.json';old.save(path,{'name':name,'components':components});c['rf3_input_paths'][state]=str(path);c['rf3_output_dirs'][state]=str(out/'rf3/predictions'/name)
            except Exception:c.update(status='failed_no_replacement',error=traceback.format_exc())
            finally:old.save(mp,manifest)
            if time.monotonic()>=deadline:break
        ready=[c for c in manifest['candidates'] if c['status']=='sequence_ready'];remaining=deadline-time.monotonic();manifest['RF3_start_budget_check']={'remaining_seconds':remaining,'minimum_seconds':900,'status':'eligible' if ready and remaining>=900 else 'not_started_preserve_missingness'}
        if ready and remaining>=900:
            config=out/'rf3/config.json';old.save(config,{'checkpoint':ckpts['rf3'],'out_dir':str(out/'rf3/predictions'),'inputs':[{'path':c['rf3_input_paths'][s],'state':s,'enzyme_sequence':c['enzyme_sequence']} for c in ready for s in ('monomer','ES')]})
            for c in ready:c['status']='rf3_started'
            old.save(mp,manifest);command([sys.executable,package/'rf3_seeded_worker.py','--config',config],'all_assigned_available_RF3')
    except BaseException:manifest['run_error']=traceback.format_exc();raise
    finally:
        for c in manifest['candidates']:
            for a in c['rf3_assignments']:
                folder=c['rf3_output_dirs'][a['state']];name=f'{c["id"]}_{a["state"]}_seed-0_sample-{a["sample"]}_model.cif';matches=list(Path(folder).rglob(name)) if folder and Path(folder).exists() else [];a.update(status='produced_pending_measurement' if len(matches)==1 else ('missing' if not matches else 'ambiguous'),path=str(matches[0]) if len(matches)==1 else None)
                if len(matches)==1:a['sha256']=old.digest(matches[0])
            if all(a['status']=='produced_pending_measurement' for a in c['rf3_assignments']):c['status']='all_10_predictions_produced_pending_measurement'
            elif c['status'] in ('assigned_not_started','sequence_ready','rf3_started'):c['status']='incomplete_no_replacement'
        manifest.update(observed_RF3_outputs=sum(a['status']=='produced_pending_measurement' for c in manifest['candidates'] for a in c['rf3_assignments']),completed_unix=time.time());old.save(mp,manifest)

if __name__=='__main__':main()
