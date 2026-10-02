"""Case-specific translation of inert author source; no author code execution.

Rebuild one ALQSSWGMMG G7-M8 motif input from the retained first-round
template. Neither inference, random sampling nor author notebook execution
occurs here. The public candidate remains pending native consumer validation.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MOTIF = HERE / '251222_motif_with_ANISOU.pdb'
NOTEBOOK = HERE / 'round1_example.ipynb'
PEPTIDE = 'ALQSSWGMMG'
P1 = 7
CONTIG = '15-100,A293-297,10-100,A28-30,10-100,A376-378,10-100,A315-317,15-100,/0,B1-10'
# Author cell11's first saved origin, reconstructed independently from its
# actual H297/H293/E378 plane, matching the saved printed result to 0.001 A.
ORI = [6.787079050497307, 45.54150783969011, -6.044966758089851]
AA3 = {'A':'ALA','L':'LEU','Q':'GLN','S':'SER','W':'TRP','G':'GLY','M':'MET'}
SIDECHAINS = {
    'ALA':['CB'], 'LEU':['CB','CG','CD1','CD2'],
    'GLN':['CB','CG','CD','OE1','NE2'], 'SER':['CB','OG'],
    'TRP':['CB','CG','CD1','CD2','NE1','CE2','CE3','CZ2','CZ3','CH2'],
    'GLY':[], 'MET':['CB','CG','SD','CE'],
}
BACKBONE = ['N','CA','C','O']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_atoms(path):
    return [line for line in path.read_text().splitlines()
            if line.startswith(('ATOM  ','HETATM'))]

def key(line):
    return line[21], int(line[22:26]), line[12:16].strip()

def xyz(line):
    return [float(line[30:38]), float(line[38:46]), float(line[46:54])]

def new_atom(serial, atom, resname, residue, coord):
    # Canonical PDB atom-name alignment, including one-letter atom elements.
    atom_field = (' ' + atom).ljust(4) if len(atom) < 4 else atom
    return (f'ATOM  {serial:5d} {atom_field:4s} {resname:3s} B{residue:4d}    '
            f'{coord[0]:8.3f}{coord[1]:8.3f}{coord[2]:8.3f}'
            f'{1.0:6.2f}{90.0:6.2f}          {atom[0]:>2s}  ')

def main():
    assert sha(MOTIF) == '3a3a63587f190a741918e0b594bf8be1727592d82a71187cf73689a3e750a344'
    assert sha(NOTEBOOK) == '0e645c88ca9985515f67ddd90aa7d06287f79a6b3dd4ecde1e7403b0086c925a'
    atoms = read_atoms(MOTIF)
    source = {key(line):line for line in atoms}
    notebook = json.loads(NOTEBOOK.read_text())
    # Save the original cells as inert provenance, not an importable module.
    selected_cells = {str(i): {'cell_type':notebook['cells'][i]['cell_type'],
                              'source':notebook['cells'][i]['source']}
                      for i in [7,8,9,11,13,17]}
    (HERE/'author_input_source_cells.json').write_text(json.dumps(selected_cells,indent=2)+'\n')
    output = []
    serial = 1
    # Author cell8 copies chain A and C, in that order, then appends new B.
    for chain in ['A','C']:
        for line in atoms:
            if line[21] == chain:
                output.append(line[:6]+f'{serial:5d}'+line[11:])
                serial += 1
        output.append('TER')
    for residue, letter in enumerate(PEPTIDE,1):
        for atom in BACKBONE + SIDECHAINS[AA3[letter]]:
            coord = xyz(source['B',residue,atom]) if residue in (P1,P1+1) and atom in BACKBONE else [0.0,0.0,0.0]
            output.append(new_atom(serial,atom,AA3[letter],residue,coord))
            serial += 1
    output.extend(['TER','END'])
    pdb = HERE/'ALQSSWGMMG78.pdb'
    pdb.write_text('\n'.join(output)+'\n')
    fixed_b = {f'B{i}':('BKBN' if i in (P1,P1+1) else '') for i in range(1,11)}
    author = {'global_args':{'redesign_motif_sidechains':False},'des':{
        'input':'ALQSSWGMMG78.pdb', 'contig':CONTIG, 'length':'170-200',
        'ligand':'ZO', 'select_unfixed_sequence':'A28-A30,A295-296,A376,A378,A315,A317',
        'select_hotspots':'B3-7', 'select_fixed_atoms':fixed_b, 'ori_token':ORI}}
    (HERE/'tdp_G7_M8_author_dialect.json').write_text(json.dumps(author,indent=2)+'\n')
    # Preserve the source schema/masks. Root's pinned public-source inspection
    # confirms global_args merging and default-fixed A coordinates/sequences.
    # The sole candidate adaptation selects the unchanged ZnO component by C1.
    public = json.loads(json.dumps(author))
    public['des']['ligand'] = 'C1'
    (HERE/'tdp_G7_M8_public_candidate.json').write_text(json.dumps(public,indent=2)+'\n')
    built = {key(line):line for line in read_atoms(pdb)}
    copied = [k for k in source if k[0] in ['A','C']]
    assert all(source[k][11:] == built[k][11:] for k in copied)
    anchors = [('B',r,a) for r in (7,8) for a in BACKBONE]
    assert all(xyz(source[k]) == xyz(built[k]) for k in anchors)
    placeholders = [k for k in built if k[0]=='B' and k not in anchors]
    assert all(xyz(built[k]) == [0.0,0.0,0.0] for k in placeholders)
    assert not any(k[2]=='OXT' for k in built)
    assert built['C',1,'ZN1'][17:20]=='ZnO'
    assert not any(line.startswith('CONECT') for line in output)
    relation = {
      'input':'ALQSSWGMMG78.pdb','input_sha256':sha(pdb),
      'scope':'Source-derived first-round design input, not TDPn3 selected ES geometry and not a generated design.',
      'substrate':{'sequence':PEPTIDE,'assay_sequence':'ALQSSWGMMGML',
                   'model_to_assay_positions':'B1-10 maps to assay1-10; M11/L12 absent.',
                   'scissile_bond':[{'chain':'B','residue_number':7,'residue_name':'GLY','atom_name':'C'},
                                    {'chain':'B','residue_number':8,'residue_name':'MET','atom_name':'N'}],
                   'sequence_fixed':True,'coordinate_fixed_backbone_residues':[7,8]},
      'catalytic_roles':{
        'zinc_ligands':[{'chain':'A','residue_number':293,'residue_name':'HIS','atom_name':'NE2'},
                        {'chain':'A','residue_number':297,'residue_name':'HIS','atom_name':'NE2'},
                        {'chain':'A','residue_number':316,'residue_name':'GLU','atom_name':'OE1'}],
        'general_base':[{'chain':'A','residue_number':294,'residue_name':'GLU','atom_name':n} for n in ['OE1','OE2']],
        'oxyanion_donor':[{'chain':'A','residue_number':377,'residue_name':'TYR','atom_name':n} for n in ['OH','CZ']],
        'water':{'chain':'C','residue_number':1,'residue_name':'ZnO','atom_name':'O1'},
        'zinc':{'chain':'C','residue_number':1,'residue_name':'ZnO','atom_name':'ZN1'}},
      'selection':{'source_contig_ordinal':1,'source_ori_ordinal':1,
                   'contig':CONTIG,'ori':ORI,'scope':'One preselected notebook contig/origin; no grid, sampling or optimization.'},
      'source_provenance':{'notebook':{'file':NOTEBOOK.name,'sha256':sha(NOTEBOOK),'cells':[7,8,9,11,13,17]},
                           'motif':{'file':MOTIF.name,'sha256':sha(MOTIF)},
                           'template_origin':'Notebook cell7 describes substrate/guide strand from Zn45-S_ZnO36 plus active site from4QHP; this is an author hybrid computational input.'},
      'transformations':['Remove ANISOU records; preserve source A/C atom fields except atom serials.',
        'Replace B with the exact10mer; copy only B7/B8 N,CA,C,O coordinates; initialize all other peptide atoms tozero.',
        'Reassign B7 ASN toGLY and B8 PHE toMET identity as the fixed target requires; their source backbone coordinates are reused.',
        'Save one source-style JSON with ligand ZO unchanged for provenance.',
        'Save a public candidate with only ligand selection changed from ZO to C1; preserve the source wrapper, sequence and coordinate masks.'],
      'compatibility_issues':[
        'Author JSON ligand ZO does not literally match input residue name ZnO; public candidate selects C1 and preserves component identity.',
        'Public candidate is not yet validated by the complete native consumer; custom ZnO chemical graph and preprocessing must be checked.',
        'No Zn-O covalent bond was invented; original PDB contains no CONECT record.',
        'Source ori cell11 asks for residue376 OE1 and its fallback selectsGLU378, not Zn ligandGLU316; saved ori output confirms this. Preserved as a placement choice, not a donor-plane claim.',
        'Notebook example epitope dictionary outputs are tau windows; applying its documented generic routine to ALQSSWGMMG is a source-derived reconstruction, not execution of saved TDP commands.'
      ],
      'local_checks':{'source_A_C_atoms_preserved':len(copied),'fixed_substrate_backbone_atoms':len(anchors),
                      'zero_coordinate_substrate_placeholders':len(placeholders),
                      'atom_count_by_chain':dict(Counter(k[0] for k in built)),
                      'no_OXT':True,'no_invented_CONECT':True,'notebook_executed':False,'inference_executed':False},
      'remaining_dependencies':['Native public parser/annotation check for fixed atom and fixed sequence masks, ZnO retention and graph handling.',
        'Pinned RFD3 runtime/checkpoint and authorized capable inference environment.',
        'One bounded diffusion output followed by sequence design and separate monomer/complex evaluation before a fresh candidate can be assessed.']
    }
    (HERE/'tdp_G7_M8_input_provenance.json').write_text(json.dumps(relation,indent=2)+'\n')
    print(json.dumps({'input_sha256':sha(pdb),'checks':relation['local_checks'],
                      'public_candidate_sha256':sha(HERE/'tdp_G7_M8_public_candidate.json'),
                      'provenance_sha256':sha(HERE/'tdp_G7_M8_input_provenance.json')},indent=2))

if __name__=='__main__':
    main()
