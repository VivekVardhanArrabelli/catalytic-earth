load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_1B65.cif", m_csa_676
hide everything
show cartoon, m_csa_676
color gray70, m_csa_676
set cartoon_transparency, 0.8, m_csa_676
select m_csa_676_left, m_csa_676 and chain A and resi 289 and resn GLY
select m_csa_676_right, m_csa_676 and chain A and resi 218 and resn ASN
show sticks, m_csa_676_left or m_csa_676_right
color tv_red, m_csa_676_left
color tv_blue, m_csa_676_right
distance m_csa_676_distance, (m_csa_676 and chain A and resi 289 and resn GLY and name CA), (m_csa_676 and chain A and resi 218 and resn ASN and name CA)
label m_csa_676_distance, "9.257 A"
zoom m_csa_676_left or m_csa_676_right, 8
set dash_width, 3
set label_size, 18
