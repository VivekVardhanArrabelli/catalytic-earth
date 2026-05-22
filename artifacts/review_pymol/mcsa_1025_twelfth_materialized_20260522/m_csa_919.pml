load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_1XTC.cif", m_csa_919
hide everything
show cartoon, m_csa_919
color gray70, m_csa_919
set cartoon_transparency, 0.8, m_csa_919
select m_csa_919_left, m_csa_919 and chain A and resi 110 and resn GLU
select m_csa_919_right, m_csa_919 and chain A and resi 7 and resn ARG
show sticks, m_csa_919_left or m_csa_919_right
color tv_red, m_csa_919_left
color tv_blue, m_csa_919_right
distance m_csa_919_distance, (m_csa_919 and chain A and resi 110 and resn GLU and name CA), (m_csa_919 and chain A and resi 7 and resn ARG and name CA)
label m_csa_919_distance, "12.942 A"
zoom m_csa_919_left or m_csa_919_right, 8
set dash_width, 3
set label_size, 18
