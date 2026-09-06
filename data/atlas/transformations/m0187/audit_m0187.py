import hashlib, json, xml.etree.ElementTree as ET
from pathlib import Path
from rdkit import Chem

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SRC = REPO / 'data/atlas/atlas10/sources/mcsa/M0187.json'
CAN = {
    'CHEBI:17756': HERE / 'CHEBI_17756.mol',
    'CHEBI:32382': HERE / 'CHEBI_32382.mol',
}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(p):
 m=Chem.MolFromMolFile(str(p),sanitize=True,removeHs=False)
 Chem.AssignStereochemistry(m,cleanIt=True,force=True)
 return m

def mrv_step(s):
 root=ET.fromstring(s['content_utf8'])
 atoms=list(root.findall('.//atom'))
 ad={a.attrib['id']:a.attrib for a in atoms}
 bonds=[]
 for b in root.findall('.//bond'):
  st=b.find('bondStereo')
  bonds.append({'id':b.attrib.get('id'),'refs':b.attrib['atomRefs2'].split(),'order':b.attrib.get('order'),'convention':b.attrib.get('convention'),'stereo':None if st is None else st.text})
 # ligand covalent component, seeded by raw label. This deliberately excludes cxn:coord.
 seeds={i for i,a in ad.items() if a.get('mrvExtraLabel')=='chebi:17756'}
 adj={i:set() for i in ad}
 for b in bonds:
  if b['order'] is not None:
   x,y=b['refs']; adj[x].add(y);adj[y].add(x)
 comp=set(seeds); todo=list(seeds)
 while todo:
  x=todo.pop()
  for y in adj[x]:
   if y not in comp: comp.add(y);todo.append(y)
 # RDKit whole model for source stereo assignment; atom order follows MRV atomArray.
 mol=Chem.MolFromMrvBlock(s['content_utf8'],sanitize=True,removeHs=False)
 Chem.AssignStereochemistry(mol,cleanIt=True,force=True)
 rd={a.attrib['id']: mol.GetAtomWithIdx(i) for i,a in enumerate(atoms)}
 ligand_atoms=[]
 for i in sorted(comp,key=lambda x:int(x[1:])):
  a=ad[i]; ra=rd[i]
  ligand_atoms.append({
   'source_atom_ref':i,'element':a['elementType'],'formal_charge':int(a.get('formalCharge','0')),
   'raw_label':a.get('mrvExtraLabel'),'cip':ra.GetProp('_CIPCode') if ra.HasProp('_CIPCode') else None,
  })
 ligand_bonds=[b for b in bonds if set(b['refs'])<=comp]
 flows=[]
 for f in root.findall('.//MEFlow'):
  points=[]
  for c in f:
   points.append({'kind':c.tag,'atom_refs':(c.attrib.get('atomRefs') or c.attrib.get('atomRef')).replace('m1.','').split()})
  flows.append({'flow_id':f.attrib['id'],'points':points})
 return {'step_id':s['step_id'],'source_sha256':s['content_sha256'],'is_product':s['is_product'],
         'ligand_seed_label':'chebi:17756' if seeds else None,'ligand_atoms':ligand_atoms,'ligand_bonds':ligand_bonds,'flows':flows}

def mol_summary(k,m,p):
 Chem.AssignStereochemistry(m,cleanIt=True,force=True)
 return {'id':k,'sha256':sha(p),'atoms':m.GetNumAtoms(),'heavy_atoms':m.GetNumHeavyAtoms(),
  'formal_charge':Chem.GetFormalCharge(m),
  'cip':[{ 'atom_index_1based':a.GetIdx()+1,'element':a.GetSymbol(),'cip':a.GetProp('_CIPCode')} for a in m.GetAtoms() if a.HasProp('_CIPCode')],
  'canonical_rank_break_ties_false':list(Chem.CanonicalRankAtoms(m,breakTies=False,includeChirality=False)),
  'canonical_rank_chiral_break_ties_false':list(Chem.CanonicalRankAtoms(m,breakTies=False,includeChirality=True))}

D=json.loads(SRC.read_text())
steps=[mrv_step(s) for s in D['step_schemes']]
cm={k:canonical(p) for k,p in CAN.items()}
# Canonical participant matches anywhere in each complete source panel.  This is
# separate from the raw source labels and catches an unlabeled product graph.
panel_canonical_matches={}
for source_row in D['step_schemes']:
 full=Chem.MolFromMrvBlock(source_row['content_utf8'],sanitize=True,removeHs=False)
 panel_row={}
 for participant_id,query in cm.items():
  for use_chirality in (False,True):
   raw_matches=full.GetSubstructMatches(
       query,useChirality=use_chirality,uniquify=False,maxMatches=1000
   )
   panel_row[f"{participant_id}:{'chiral' if use_chirality else 'achiral'}"]={
       'count':len(raw_matches),
       'source_atom_maps':[
           [f'a{source_index+1}' for source_index in match]
           for match in raw_matches
       ],
   }
 panel_canonical_matches[str(source_row['step_id'])]=panel_row
# Canonical R/S graph matches. Chirality requires query stereo tags, use full molecules both directions.
matches={}
for a,ma in cm.items():
 for b,mb in cm.items():
  without = mb.GetSubstructMatches(ma,useChirality=False,uniquify=False,maxMatches=1000)
  with_chiral = mb.GetSubstructMatches(ma,useChirality=True,uniquify=False,maxMatches=1000)
  matches[f'{a}_query_in_{b}']={
    'without_chirality_count':len(without),
    'without_chirality_maps_zero_based':[list(item) for item in without],
    'with_chirality_count':len(with_chiral),
    'with_chirality_maps_zero_based':[list(item) for item in with_chiral],
  }
# exact shared-ID heavy-atom bond changes S1->S2
s1,s2=steps[0],steps[1]
def bdict(s):
 return {tuple(sorted(b['refs'])):(b['order'],b['stereo']) for b in s['ligand_bonds'] if all(next(a for a in s['ligand_atoms'] if a['source_atom_ref']==x)['element']!='H' for x in b['refs'])}
b1,b2=bdict(s1),bdict(s2)
diffs=[]
for e in sorted(set(b1)|set(b2),key=lambda z:tuple(int(x[1:]) for x in z)):
 if b1.get(e)!=b2.get(e): diffs.append({'atom_refs':list(e),'step1':b1.get(e),'step2':b2.get(e)})
# Explicit H attachment differences across entire raw panels for H65/H66/H67.
def all_bonds(sraw):
 root=ET.fromstring(sraw['content_utf8']); out={}
 for b in root.findall('.//bond'):
  if b.attrib.get('order') is not None:
   for x in b.attrib['atomRefs2'].split(): out.setdefault(x,[]).append({'bond_id':b.attrib.get('id'),'refs':b.attrib['atomRefs2'].split(),'order':b.attrib['order']})
 return out
hs=[]
for h in ['a65','a66','a67']:
 hs.append({'atom_ref':h,'step1':all_bonds(D['step_schemes'][0]).get(h,[]),'step2':all_bonds(D['step_schemes'][1]).get(h,[])})
# Raw atom bookkeeping changes across the two panels, independent of chemistry names.
def raw_atoms(sraw):
 root=ET.fromstring(sraw['content_utf8'])
 return {a.attrib['id']:a.attrib for a in root.findall('.//atom')}
ra1,ra2=raw_atoms(D['step_schemes'][0]),raw_atoms(D['step_schemes'][1])
attribute_diffs=[]
for atom_ref in sorted(set(ra1)|set(ra2),key=lambda x:int(x[1:])):
 changes={}
 for key in ('elementType','formalCharge','lonePair','mrvExtraLabel','mrvAlias'):
  left=None if atom_ref not in ra1 else ra1[atom_ref].get(key)
  right=None if atom_ref not in ra2 else ra2[atom_ref].get(key)
  if left!=right: changes[key]=[left,right]
 if atom_ref not in ra1 or atom_ref not in ra2:
  changes['presence']=[atom_ref in ra1,atom_ref in ra2]
 if changes: attribute_diffs.append({'atom_ref':atom_ref,'changes':changes})
out={
 'audit_method':{'rdkit_version':Chem.rdBase.rdkitVersion,'mrv_parse':'Chem.MolFromMrvBlock(sanitize=True, removeHs=False)','canonical_parse':'Chem.MolFromMolFile(sanitize=True, removeHs=False)','ligand_component':'covalent-order bonds from raw chebi:17756 seeds; cxn:coord excluded'},
 'source_snapshot':{'path':str(SRC.relative_to(REPO)),'sha256':sha(SRC)},
 'canonical_structures':[mol_summary(k,cm[k],CAN[k]) for k in CAN],
 'complete_panel_canonical_participant_matches':panel_canonical_matches,
 'canonical_graph_matches':matches,
 'steps':steps,
 'step1_to_step2_same_id_heavy_bond_differences':diffs,
 'step1_to_step2_selected_hydrogen_attachments':hs,
 'step1_to_step2_raw_atom_attribute_differences':attribute_diffs,
 'limitations':['RDKit CIP assignments are project computational analysis, not literal source labels.','No product ligand is present in Step 3 or terminal Step 4, so product stereochemistry is not a terminal-panel observation.','Shared atom identifiers support direct comparison only between retained Step 1 and Step 2 bytes; they are not assumed across renumbered later panels.','Canonical graph automorphisms leave remote phenyl positions symmetry-equivalent; no arbitrary unique full-ring map is asserted.']
}
opath = HERE / 'retained_graph_audit.json'
opath.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(opath)
print('sha256',sha(opath))
brief_steps = [
    {
        'step': x['step_id'],
        'ligand_n': len(x['ligand_atoms']),
        'charge': sum(a['formal_charge'] for a in x['ligand_atoms']),
        'cip': [a for a in x['ligand_atoms'] if a['cip']],
    }
    for x in steps
]
print(json.dumps({'canonical': out['canonical_structures'], 'matches': matches,
                  'diffs': diffs, 'H': hs, 'steps': brief_steps}, indent=2))
