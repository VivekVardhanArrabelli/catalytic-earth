load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_3UXJ.cif", m_csa_967
hide everything
show cartoon, m_csa_967
color gray70, m_csa_967
set cartoon_transparency, 0.8, m_csa_967
select m_csa_967_left, m_csa_967 and chain A and resi 200 and resn THR
select m_csa_967_right, m_csa_967 and chain A and resi 237 and resn GLU
show sticks, m_csa_967_left or m_csa_967_right
color tv_red, m_csa_967_left
color tv_blue, m_csa_967_right
distance m_csa_967_distance, (m_csa_967 and chain A and resi 200 and resn THR and name CA), (m_csa_967 and chain A and resi 237 and resn GLU and name CA)
label m_csa_967_distance, "15.385 A"
zoom m_csa_967_left or m_csa_967_right, 8
set dash_width, 3
set label_size, 18
