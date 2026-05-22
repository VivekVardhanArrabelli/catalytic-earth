load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_1FO6.cif", m_csa_671
hide everything
show cartoon, m_csa_671
color gray70, m_csa_671
set cartoon_transparency, 0.8, m_csa_671
select m_csa_671_left, m_csa_671 and chain A and resi 127 and resn LYS
select m_csa_671_right, m_csa_671 and chain A and resi 197 and resn ASN
show sticks, m_csa_671_left or m_csa_671_right
color tv_red, m_csa_671_left
color tv_blue, m_csa_671_right
distance m_csa_671_distance, (m_csa_671 and chain A and resi 127 and resn LYS and name CA), (m_csa_671 and chain A and resi 197 and resn ASN and name CA)
label m_csa_671_distance, "12.982 A"
zoom m_csa_671_left or m_csa_671_right, 8
set dash_width, 3
set label_size, 18
