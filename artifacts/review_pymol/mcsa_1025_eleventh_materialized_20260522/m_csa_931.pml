load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_2PTH.cif", m_csa_931
hide everything
show cartoon, m_csa_931
color gray70, m_csa_931
set cartoon_transparency, 0.8, m_csa_931
select m_csa_931_left, m_csa_931 and chain A and resi 68 and resn ASN
select m_csa_931_right, m_csa_931 and chain A and resi 93 and resn ASP
show sticks, m_csa_931_left or m_csa_931_right
color tv_red, m_csa_931_left
color tv_blue, m_csa_931_right
distance m_csa_931_distance, (m_csa_931 and chain A and resi 68 and resn ASN and name CA), (m_csa_931 and chain A and resi 93 and resn ASP and name CA)
label m_csa_931_distance, "13.862 A"
zoom m_csa_931_left or m_csa_931_right, 8
set dash_width, 3
set label_size, 18
