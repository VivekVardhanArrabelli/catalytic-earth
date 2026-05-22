load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_1ZRZ.cif", m_csa_756
hide everything
show cartoon, m_csa_756
color gray70, m_csa_756
set cartoon_transparency, 0.8, m_csa_756
select m_csa_756_left, m_csa_756 and chain A and resi 146 and resn ASP
select m_csa_756_right, m_csa_756 and chain A and resi 151 and resn ASN
show sticks, m_csa_756_left or m_csa_756_right
color tv_red, m_csa_756_left
color tv_blue, m_csa_756_right
distance m_csa_756_distance, (m_csa_756 and chain A and resi 146 and resn ASP and name CA), (m_csa_756 and chain A and resi 151 and resn ASN and name CA)
label m_csa_756_distance, "7.811 A"
zoom m_csa_756_left or m_csa_756_right, 8
set dash_width, 3
set label_size, 18
