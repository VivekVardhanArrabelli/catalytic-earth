#!/usr/bin/env python3
"""Fail-closed checks of two real native RFD3 gate outputs; no model execution."""
import argparse
import hashlib
import json
import math
from pathlib import Path

AA = dict(zip('ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL'.split(), 'ARNDCQEGHILKMFPSTWYV'))
ROLES = {'A293': (36, 'HIS'), 'A294': (37, 'GLU'), 'A297': (40, 'HIS'),
         'A316': (152, 'GLU'), 'A377': (115, 'TYR')}
INPUT_SHAS = {'water_fixed':'5d3cac4d1588bb5662b2f3b8a61e896d012601526e85ce553262775892d1c390',
              'water_unfixed':'43399d8c7b3e89f663306789d9abc2bc07f4b07b7c5fb9fbfaebe4ab8875a943'}
PDB_SHA = '85830251fcf93fb26c00a6c79cfb6c2815b444e3db941e7470cf341cb8ebb8e0'
API_SHA = '79baccb07cc65924ffd833615e5de6bcb186eeb1c87eedbc4324777c63f7e9ee'

def require(value, message):
    if not value:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_stage(directory, filename, receipt):
    path = directory/filename
    expected = [x['sha256'] for x in receipt['stages'] if x['file']==filename]
    require(len(expected)==1 and sha(path)==expected[0], 'Native snapshot hash mismatch')
    return json.loads(path.read_text())

def check_arm(directory, arm, source):
    receipt=json.loads((directory/'native_execution_receipt.json').read_text())
    require(receipt['status']=='native_load_build_and_pipeline_parse_completed_pending_chemical_review', 'Native execution did not complete')
    require(receipt['input_sha256']==INPUT_SHAS[arm] and receipt['native_api_sha256']==API_SHA, 'Input/native API identity changed')
    loaded=load_stage(directory,'native_loaded_atoms.json',receipt)
    built=load_stage(directory,'native_built_atoms.json',receipt)
    reports={}
    for stage,d in [('loaded',loaded),('built',built)]:
        a=d['annotations']; n=len(a['res_id'])
        require(all(len(x)==n for x in a.values()), 'Annotation length mismatch')
        require(len(d['coordinates'])==n and all(math.isfinite(x) for xyz in d['coordinates'] for x in xyz), 'Nonfinite/missing coordinates')
        def index(chain,residue,atom):
            found=[i for i in range(n) if (a['chain_id'][i],a['res_id'][i],a['atom_name'][i])==(chain,residue,atom)]
            require(len(found)==1, f'Nonunique required atom {chain}{residue}:{atom}')
            return found[0]
        lengths={c:len({a['res_id'][i] for i in range(n) if a['chain_id'][i]==c}) for c in set(a['chain_id'])}
        require(lengths==({'A':14,'B':12,'C':1} if stage=='loaded' else {'A':187,'B':12,'C':1}), 'Unexpected component lengths')
        zinc=index('C',1,'ZN1'); water=index('C',1,'O1'); g=index('B',7,'C'); m=index('B',8,'N')
        ligand=[i for i in range(n) if a['chain_id'][i]=='C']
        require(set(ligand)=={zinc,water}, 'Ligand atoms missing/added')
        require(a['element'][zinc].upper()=='ZN' and a['element'][water].upper()=='O', 'Ligand element changed')
        require(a['res_name'][zinc]==a['res_name'][water]=='ZnO', 'Ligand renamed')
        require(a['charge'][zinc]==2 and a['charge'][water]==0, 'Zn/water formal charge not preserved')
        require(all(a['is_motif_atom_with_fixed_seq'][i] for i in ligand), 'Ligand species not fixed')
        require(a['is_motif_atom_with_fixed_coord'][zinc] and bool(a['is_motif_atom_with_fixed_coord'][water])==(arm=='water_fixed'), 'Incorrect ligand coordinate masks')
        require(not any(zinc in edge[:2] or water in edge[:2] for edge in d['bonds']), 'Invented ligand covalent bond')
        peptide=[i for i in range(n) if a['chain_id'][i]=='B']
        names={j:{a['res_name'][i] for i in peptide if a['res_id'][i]==j} for j in range(1,13)}
        require(all(len(x)==1 for x in names.values()), 'Peptide residue identity ambiguous')
        sequence=''.join(AA[next(iter(names[j]))] for j in range(1,13))
        require(sequence=='ALQSSWGMMGML' and all(a['is_motif_atom_with_fixed_seq'][i] for i in peptide), 'Peptide sequence/mask changed')
        fixedB={(a['res_id'][i],a['atom_name'][i]) for i in peptide if a['is_motif_atom_with_fixed_coord'][i]}
        require(fixedB=={(j,atom) for j in (7,8) for atom in ('N','CA','C','O')}, 'Reactive backbone mask changed')
        motif=[i for i in range(n) if a['chain_id'][i]=='A' and (stage=='loaded' or a['src_component'][i].startswith('A'))]
        require(len(motif)==119 and all(a['is_motif_atom_with_fixed_coord'][i] for i in motif), 'Source motif coordinates released/lost')
        component=lambda i: f"A{a['res_id'][i]}" if stage=='loaded' else a['src_component'][i]
        require({component(i) for i in motif if a['is_motif_atom_with_fixed_seq'][i]}==set(ROLES), 'Catalytic/variable sequence mask changed')
        delta=[source['C',1,'ZN1'][j]-d['coordinates'][zinc][j] for j in range(3)]
        max_error=max(math.dist(source['A',int(component(i)[1:]),a['atom_name'][i]],
                                [x+t for x,t in zip(d['coordinates'][i],delta)]) for i in motif)
        require(max_error<1e-5, 'Source catalytic-motif geometry changed beyond common translation')
        role_map={}
        for src,(target,resname) in ROLES.items():
            role=[i for i in motif if component(i)==src]
            expected=int(src[1:]) if stage=='loaded' else target
            require({a['res_id'][i] for i in role}=={expected} and {a['res_name'][i] for i in role}=={resname}, 'Role mapping changed')
            role_map[src]=expected
        explicit=[edge for edge in d['bonds'] if set(edge[:2])=={g,m}]
        if stage=='loaded': require(len(explicit)==1 and explicit[0][2]==1, 'Loaded G7C-M8N ordinary single bond missing')
        require(abs(math.dist(d['coordinates'][g],d['coordinates'][m])-math.dist(source['B',7,'C'],source['B',8,'N']))<1e-5, 'Reactive bond geometry changed')
        reports[stage]={'atom_count':n,'chain_residue_counts':lengths,'peptide_sequence':sequence,
                        'Zn_formal_charge':a['charge'][zinc],'O_formal_charge':a['charge'][water],
                        'water_index':water,'water_coord_fixed':bool(a['is_motif_atom_with_fixed_coord'][water]),
                        'source_motif_atoms_fixed':len(motif),'max_source_coordinate_error_A':max_error,
                        'role_residue_map':role_map,'G7C_M8N_explicit_bonds':explicit}
    return reports,built

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--fixed',type=Path,required=True)
    p.add_argument('--free',type=Path,required=True)
    p.add_argument('--source-pdb',type=Path,default=None,
                   help='Optional; defaults to the source PDB recorded in the fixed gate input')
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    report={'status':'failed','model_execution':False,'verifier_sha256':sha(Path(__file__))}
    try:
        if args.source_pdb is None:
            fixed_receipt=json.loads((args.fixed/'native_execution_receipt.json').read_text())
            input_path=Path(fixed_receipt['input'])
            require(sha(input_path)==INPUT_SHAS['water_fixed'], 'Recorded fixed input bytes changed')
            input_spec=json.loads(input_path.read_text())
            args.source_pdb=(input_path.parent/Path(input_spec['des']['input'])).resolve()
        require(sha(args.source_pdb)==PDB_SHA, 'Prospective PDB bytes changed')
        report['source_pdb']={'path':str(args.source_pdb.resolve()),'sha256':PDB_SHA}
        source={}
        for line in args.source_pdb.read_text().splitlines():
            if line[:6] in ('ATOM  ','HETATM'):
                key=(line[21],int(line[22:26]),line[12:16].strip())
                require(key not in source, 'Duplicate source atom')
                source[key]=[float(line[i:i+8]) for i in (30,38,46)]
        fixed,f=check_arm(args.fixed,'water_fixed',source)
        free,u=check_arm(args.free,'water_unfixed',source)
        require(set(f['annotations'])==set(u['annotations']), 'Annotation categories differ')
        diffs=[{'annotation':key,'atom_index':i,'fixed':x,'free':y}
               for key in f['annotations'] for i,(x,y) in enumerate(zip(f['annotations'][key],u['annotations'][key])) if x!=y]
        water=fixed['built']['water_index']
        require(diffs==[{'annotation':'is_motif_atom_with_fixed_coord','atom_index':water,'fixed':True,'free':False}], 'Arm difference extends beyond water coordinate mask')
        coords=[i for i,(x,y) in enumerate(zip(f['coordinates'],u['coordinates'])) if x!=y]
        require(coords==[water] and u['coordinates'][water]==[0.,0.,0.], 'Native masking changed other coordinates or failed to clear water')
        require(f['bonds']==u['bonds'], 'Arm bond graphs differ')
        report.update(status='passed_actual_native_pair_checks',arms={'water_fixed':fixed,'water_unfixed':free},
                      annotation_differences=diffs,coordinate_difference_indices=coords,
                      qualification='Loaded ordinary peptide edge and chemistry verified. Standard polymer edges are not explicitly retained in the native built graph; this is recorded, not classified as a bug. No inference or catalytic activity follows from acceptance.')
    except Exception as error:
        report['error']=f'{type(error).__name__}: {error}'
        raise
    finally:
        with args.output.open('x') as f: json.dump(report,f,indent=2);f.write('\n')

if __name__=='__main__': main()
