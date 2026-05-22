load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_2DBT.cif", m_csa_819
hide everything
show cartoon, m_csa_819
color gray70, m_csa_819
set cartoon_transparency, 0.8, m_csa_819
select m_csa_819_left, m_csa_819 and chain A and resi 118 and resn GLU
select m_csa_819_right, m_csa_819 and chain A and resi 165 and resn ASN
show sticks, m_csa_819_left or m_csa_819_right
color tv_red, m_csa_819_left
color tv_blue, m_csa_819_right
distance m_csa_819_distance, (m_csa_819 and chain A and resi 118 and resn GLU and name CA), (m_csa_819 and chain A and resi 165 and resn ASN and name CA)
label m_csa_819_distance, "15.990 A"
zoom m_csa_819_left or m_csa_819_right, 8
set dash_width, 3
set label_size, 18
