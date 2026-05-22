load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_1PBG.cif", m_csa_877
hide everything
show cartoon, m_csa_877
color gray70, m_csa_877
set cartoon_transparency, 0.8, m_csa_877
select m_csa_877_left, m_csa_877 and chain A and resi 160 and resn GLU
select m_csa_877_right, m_csa_877 and chain A and resi 375 and resn GLU
show sticks, m_csa_877_left or m_csa_877_right
color tv_red, m_csa_877_left
color tv_blue, m_csa_877_right
distance m_csa_877_distance, (m_csa_877 and chain A and resi 160 and resn GLU and name CA), (m_csa_877 and chain A and resi 375 and resn GLU and name CA)
label m_csa_877_distance, "10.345 A"
zoom m_csa_877_left or m_csa_877_right, 8
set dash_width, 3
set label_size, 18
