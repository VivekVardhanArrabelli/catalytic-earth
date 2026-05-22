load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_1G99.cif", m_csa_643
hide everything
show cartoon, m_csa_643
color gray70, m_csa_643
set cartoon_transparency, 0.8, m_csa_643
select m_csa_643_left, m_csa_643 and chain A and resi 384 and resn GLU
select m_csa_643_right, m_csa_643 and chain A and resi 241 and resn ARG
show sticks, m_csa_643_left or m_csa_643_right
color tv_red, m_csa_643_left
color tv_blue, m_csa_643_right
distance m_csa_643_distance, (m_csa_643 and chain A and resi 384 and resn GLU and name CA), (m_csa_643 and chain A and resi 241 and resn ARG and name CA)
label m_csa_643_distance, "21.966 A"
zoom m_csa_643_left or m_csa_643_right, 8
set dash_width, 3
set label_size, 18
