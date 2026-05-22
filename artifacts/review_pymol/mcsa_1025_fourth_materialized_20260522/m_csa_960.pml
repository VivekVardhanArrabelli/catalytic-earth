load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_2QJJ.cif", m_csa_960
hide everything
show cartoon, m_csa_960
color gray70, m_csa_960
set cartoon_transparency, 0.8, m_csa_960
select m_csa_960_left, m_csa_960 and chain A and resi 339 and resn GLU
select m_csa_960_right, m_csa_960 and chain A and resi 402 and resn TRP
show sticks, m_csa_960_left or m_csa_960_right
color tv_red, m_csa_960_left
color tv_blue, m_csa_960_right
distance m_csa_960_distance, (m_csa_960 and chain A and resi 339 and resn GLU and name CA), (m_csa_960 and chain A and resi 402 and resn TRP and name CA)
label m_csa_960_distance, "19.258 A"
zoom m_csa_960_left or m_csa_960_right, 8
set dash_width, 3
set label_size, 18
