#!/usr/bin/env python3
"""Execute native MPNN preprocessing/mask/context methods; no learned forward or sampling."""
import argparse,csv,hashlib,importlib.metadata,inspect,json,sys,traceback
from pathlib import Path
PINS={
'models/mpnn/src/mpnn/utils/inference.py':'aad78c4ac571293dd64a52cc02f0b9ea4cd80a2ff7194f185bd8e6c5d744ff1b',
'models/mpnn/src/mpnn/pipelines/mpnn.py':'2b23d9e3bc240e624fd442b75520490f805e263f4b96dccb670b558d4fa69424',
'models/mpnn/src/mpnn/model/mpnn.py':'1aeae0716775140f8189b3734d05dab369c2a0328ae74d669b031f9c861b06b2',
'models/mpnn/src/mpnn/model/layers/graph_embeddings.py':'5b82a1277ce141f6166060231c95e8e41849fd47e34b853c604975011e04ffd5',
'models/mpnn/src/mpnn/collate/feature_collator.py':'40649fbebf40a1c655dae87ca48399ee71b726411884accbc6149581ba73edb6',
'models/mpnn/src/mpnn/transforms/feature_aggregation/mpnn.py':'8e4872302a898a9290d8fbe3a8f92fbc2961a225f1fc8f1ed379670de1fdfff3',
'models/mpnn/src/mpnn/transforms/feature_aggregation/user_settings.py':'779217c71d40e210f6af934cf6a90426e588dfd447eec864550cb5c9b53fb748'}
SCAFFOLD_SHA='1e764d610d69a29b76b942c625b6950ec0eb4f4ca0ea30cc0b2fc91cdd11bca2'
ROLES={36:'HIS',37:'GLU',40:'HIS',115:'TYR',152:'GLU'}
FIXED=[f'A{x}' for x in ROLES]+[f'B{x}' for x in range(1,13)]
AA=dict(zip('ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL'.split(),'ARNDCQEGHILKMFPSTWYV'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def require(ok,msg):
 if not ok:raise ValueError(msg)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--foundry-root',type=Path,required=True);p.add_argument('--scaffold',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
 require(not args.output.exists(),'Output already exists');args.output.parent.mkdir(parents=True,exist_ok=True)
 foundry=args.foundry_root.resolve();report={'status':'failed','model_execution':False,'checkpoint_loaded':False,'trained_inference_or_sampling':False,'neural_forward_executed':False,'device':'cpu','source_commit':'0932f1cb165ae7d413c11b1a7acc04ee31758817','checker_sha256':sha(__file__),'scaffold':str(args.scaffold.resolve()),'scaffold_sha256':sha(args.scaffold),'arms':{}}
 try:
  require(report['scaffold_sha256']==SCAFFOLD_SHA,'Wrong retained scaffold')
  for rel,pin in PINS.items():require(sha(foundry/rel)==pin,f'Native source changed: {rel}')
  sys.path[:0]=[str(foundry/'src'),str(foundry/'models/mpnn/src')]
  import numpy as np
  import torch
  from atomworks.ml.utils.token import get_token_starts
  from mpnn.utils.inference import MPNNInferenceInput
  from mpnn.pipelines.mpnn import build_mpnn_transform_pipeline
  from mpnn.collate.feature_collator import FeatureCollator
  from mpnn.model.mpnn import LigandMPNN
  require(Path(inspect.getfile(MPNNInferenceInput)).resolve().is_relative_to(foundry),'Unexpected imported native source')
  report['source_pins']=PINS;report['versions']={k:importlib.metadata.version(k) for k in ('torch','atomworks','biotite','numpy','rdkit')}
  torch.set_num_threads(4);torch.manual_seed(0)
  # Intact native class only supplies parameter-independent methods and constants.
  # Freshly initialized neural parameters are never loaded, called, or interpreted.
  native=LigandMPNN().cpu().eval();graph=native.graph_featurization_module
  report['native_constructor']={'class':'LigandMPNN','fresh_parameters_initialized_but_unused':True,'num_neighbors':graph.num_neighbors,'num_context_atoms':graph.num_context_atoms,'sidechain_neighbor_residues':graph.num_neighbors_for_atomized_side_chain}
  require(graph.num_neighbors==32 and graph.num_context_atoms==25,'Unexpected native architecture defaults')
  features={};arrays={};csv_rows=[]
  for arm,reveal in [('sidechains_hidden',False),('fixed_sidechains_exposed',True)]:
   config={'structure_path':str(args.scaffold.resolve()),'name':'native_context_gate','seed':200,'batch_size':1,'number_of_batches':1,'temperature':0.1,'structure_noise':0.0,'atomize_side_chains':reveal,'remove_ccds':[],'remove_waters':False,'fixed_residues':FIXED}
   spec=MPNNInferenceInput.from_atom_array_and_dict(input_dict=config);aa=spec.atom_array
   residues={}
   for i in range(len(aa)):
    ch,num=str(aa.chain_id[i]),int(aa.res_id[i]);residues.setdefault(ch,{})[num]=str(aa.res_name[i])
    if ch in ('A','B'):require(bool(aa.mpnn_designed_residue_mask[i])==(ch=='A' and num not in ROLES),'Native sequence mask changed')
   require(sorted(residues['A'])==list(range(1,188)) and sorted(residues['B'])==list(range(1,13)),'A187/B12 changed')
   require(''.join(AA[residues['B'][i]] for i in range(1,13))=='ALQSSWGMMGML','Substrate changed')
   require({i:residues['A'][i] for i in ROLES}==ROLES,'Catalytic identities changed')
   li=np.where(aa.chain_id=='C')[0];require(len(li)==2,'Ligand atom count changed')
   require({str(aa.element[i]).upper():int(aa.charge[i]) for i in li}=={'O':0,'ZN':2},'Zn/water charge changed')
   require(np.isfinite(aa.coord[li]).all(),'Nonfinite ligand coordinate');require(not any(i in li or j in li for i,j,_ in aa.bonds.as_array()),'Ligand covalent edge appeared')
   cfg=spec.input_dict
   pipeline=build_mpnn_transform_pipeline(model_type='ligand_mpnn',is_inference=True,minimal_return=True,device='cpu',**{k:cfg[k] for k in ('occupancy_threshold_sidechain','occupancy_threshold_backbone','undesired_res_names') if cfg[k] is not None})
   payload={'atom_array':aa.copy(),**{k:cfg[k] for k in ('structure_noise','decode_type','causality_pattern','initialize_sequence_embedding_with_ground_truth','atomize_side_chains','repeat_sample_num','features_to_return')}}
   output=pipeline(payload);network=FeatureCollator()([output]);f=network['input_features'];features[arm]={k:(v.clone() if isinstance(v,torch.Tensor) else v) for k,v in f.items()};arrays[arm]=output['atom_array']
   nonatom=output['atom_array'][~output['atom_array'].atomize];tokens=nonatom[get_token_starts(nonatom)];ids=[f'{x.chain_id}{int(x.res_id)}' for x in tokens]
   require(ids==[f'A{x}' for x in range(1,188)]+[f'B{x}' for x in range(1,13)],'Native token map changed')
   require(bool(torch.isfinite(f['X'][f['X_m'].bool()]).all()),'Nonfinite valid polymer atom feature')
   native.sample_and_construct_masks(f)
   fixed=[ids[i] for i in range(len(ids)) if not bool(f['designed_residue_mask'][0,i])];shown=[ids[i] for i in range(len(ids)) if not bool(f['hide_side_chain_mask'][0,i])]
   require(set(fixed)==set(FIXED),'Post-mask fixed residues changed');require(set(shown)==(set(FIXED) if reveal else set()),'Incorrect native exposure mask')
   require(bool(f['residue_mask'].all()),'A polymer residue was invalidated')
   # Native geometry-only path used by graph forward, without learned projections.
   graph.noise_structure(f)
   virtual,vmask=graph.construct_X_virtual_atoms(f['X'],f['X_m'],f['S'])
   rep,rmask=graph.construct_X_rep_atoms(f['X'],f['X_m'],f['S'])
   _,neighbor=graph.compute_representative_atom_pairwise_distances(rep,rmask,f['residue_mask'])
   side,side_mask=graph.construct_X_side_chain(f['X'],f['X_m'],f['S'])
   eligible=side_mask & ~f['hide_side_chain_mask'][:,:,None]
   require(bool(torch.isfinite(side[eligible]).all()),'Nonfinite exposed sidechain')
   require(bool(f['Y_m'].all()) and sorted(f['Y_t'][0].tolist())==[8,30] and bool(torch.isfinite(f['Y']).all()),'Ligand input context changed')
   lig=graph.gather_nearest_ligand_atoms(f['Y'],f['Y_m'],f['Y_t'],virtual,vmask,f['residue_mask'])
   context=lig
   if reveal:
    sc=graph.gather_nearest_atomized_side_chain_atoms(f['X'],f['X_m'],f['S'],neighbor,f['hide_side_chain_mask'])
    context=graph.combine_ligand_and_atomized_side_chain_atoms(*lig,*sc,virtual,vmask,f['residue_mask'])
   coords,mask,types=context;require(bool(torch.isfinite(coords[mask.bool()]).all()),'Nonfinite visible context')
   # Match gathered coordinates/types back to exact native source atoms.
   pool={}
   def add(atom_id,atomic_num,xyz):pool.setdefault((int(atomic_num),*map(float,xyz)),[]).append(atom_id)
   ligand_array=output['atom_array'][output['atom_array'].atomize]
   for i,atom in enumerate(ligand_array):add(f'{atom.chain_id}{int(atom.res_id)}:{atom.atom_name}',f['Y_t'][0,i],f['Y'][0,i].tolist())
   exposed=[]
   for i,j in torch.nonzero(eligible[0],as_tuple=False).tolist():
    atomid=f'{ids[i]}:{graph.SIDE_CHAIN_ATOM_NAMES[j]}';add(atomid,graph.side_chain_atom_types[j],side[0,i,j].tolist());exposed.append(atomid)
   inclusion=[]
   for i,rid in enumerate(ids):
    context_ids=[]
    for j in torch.nonzero(mask[0,i],as_tuple=False).flatten().tolist():
     key=(int(types[0,i,j]),*map(float,coords[0,i,j].tolist()));matches=pool.get(key,[]);require(len(matches)==1,'Ambiguous gathered atom correspondence');context_ids.append(matches[0])
    row={'arm':arm,'residue':rid,'sequence_fixed':rid in FIXED,'sidechain_revealed':rid in shown,'valid_context_atoms':len(context_ids),'Zn_in_context':'C1:ZN1' in context_ids,'water_in_context':'C1:O1' in context_ids,'context_atom_ids':';'.join(context_ids)};csv_rows.append(row);inclusion.append(row)
   report['arms'][arm]={'input':config,'fixed_residues':fixed,'revealed_residues':shown,'exposed_sidechain_atom_ids':exposed,'exposed_sidechain_atom_count':len(exposed),'ligand_Y_shape':list(f['Y'].shape),'context_shape':list(coords.shape),'minimum_valid_context_atoms':int(mask.sum(-1).min()),'maximum_valid_context_atoms':int(mask.sum(-1).max()),'masked_nonfinite_X_entries':int((~torch.isfinite(f['X'])).sum()),'all_visible_context_coordinates_finite':True,
    'Zn_visible_residue_count':sum(x['Zn_in_context'] for x in inclusion),'water_visible_residue_count':sum(x['water_in_context'] for x in inclusion),'fixed_site_context':[x for x in inclusion if x['residue'] in FIXED],
    'context_coordinate_sha256':hashlib.sha256(coords.detach().numpy().tobytes()).hexdigest(),'context_mask_sha256':hashlib.sha256(mask.detach().numpy().tobytes()).hexdigest(),
    'pre_mask_features':{k:{'shape':list(v.shape),'dtype':str(v.dtype),'sha256':hashlib.sha256(v.detach().numpy().tobytes()).hexdigest()} if isinstance(v,torch.Tensor) else v for k,v in features[arm].items()}}
  hidden,exposed=features.values();require(set(hidden)==set(exposed),'Feature keys differ')
  differences=[k for k in hidden if not (np.array_equal(hidden[k].detach().numpy(),exposed[k].detach().numpy(),equal_nan=True) if isinstance(hidden[k],torch.Tensor) else hidden[k]==exposed[k])]
  require(differences==['atomize_side_chains'],'Pre-mask features differ beyond switch')
  a,b=arrays.values();require(a.get_annotation_categories()==b.get_annotation_categories(),'Annotation categories changed')
  require(all(np.array_equal(a.get_annotation(k),b.get_annotation(k),equal_nan=True) if a.get_annotation(k).dtype.kind in 'fc' else np.array_equal(a.get_annotation(k),b.get_annotation(k)) for k in a.get_annotation_categories()),'Native annotations changed')
  require(np.array_equal(a.coord,b.coord,equal_nan=True) and np.array_equal(a.bonds.as_array(),b.bonds.as_array()),'Native coordinates or topology changed')
  table=args.output.with_suffix('.contexts.csv')
  with table.open('x',newline='') as f:
   wr=csv.DictWriter(f,fieldnames=list(csv_rows[0]));wr.writeheader();wr.writerows(csv_rows)
  report.update(status='passed_native_context_pair',pre_mask_feature_differences=differences,unchanged_native_atom_annotations_coordinates_and_bonds=True,context_table={'path':str(table.resolve()),'sha256':sha(table),'rows':len(csv_rows)},
   qualification='Actual native preprocessing, inference masks and parameter-independent context gathering executed on the retained scaffold. Fresh module parameters are unused; no checkpoint, neural encoder/decoder forward, sequence sample or prediction was evaluated. True exposes fixed enzyme and peptide sidechains excluding CB, and may replace Zn/water in finite nearest-neighbor context. No quality/activity/Atlas benefit follows.')
 except Exception:
  report['error']=traceback.format_exc();raise
 finally:
  with args.output.open('x') as f:json.dump(report,f,indent=2);f.write('\n')
  print(json.dumps({'status':report['status'],'output':str(args.output),'sha256':sha(args.output)}))
if __name__=='__main__':main()
