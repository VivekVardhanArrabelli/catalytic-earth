load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_1G24.cif", m_csa_824
hide everything
show cartoon, m_csa_824
color gray70, m_csa_824
set cartoon_transparency, 0.8, m_csa_824
select m_csa_824_left, m_csa_824 and chain A and resi 134 and resn SER
select m_csa_824_right, m_csa_824 and chain A and resi 174 and resn GLU
show sticks, m_csa_824_left or m_csa_824_right
color tv_red, m_csa_824_left
color tv_blue, m_csa_824_right
distance m_csa_824_distance, (m_csa_824 and chain A and resi 134 and resn SER and name CA), (m_csa_824 and chain A and resi 174 and resn GLU and name CA)
label m_csa_824_distance, "6.662 A"
zoom m_csa_824_left or m_csa_824_right, 8
set dash_width, 3
set label_size, 18
