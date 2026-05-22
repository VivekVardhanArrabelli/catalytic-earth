load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_1SES.cif", m_csa_884
hide everything
show cartoon, m_csa_884
color gray70, m_csa_884
set cartoon_transparency, 0.8, m_csa_884
select m_csa_884_left, m_csa_884 and chain A and resi 345 and resn GLU
select m_csa_884_right, m_csa_884 and chain A and resi 256 and resn ARG
show sticks, m_csa_884_left or m_csa_884_right
color tv_red, m_csa_884_left
color tv_blue, m_csa_884_right
distance m_csa_884_distance, (m_csa_884 and chain A and resi 345 and resn GLU and name CA), (m_csa_884 and chain A and resi 256 and resn ARG and name CA)
label m_csa_884_distance, "16.093 A"
zoom m_csa_884_left or m_csa_884_right, 8
set dash_width, 3
set label_size, 18
