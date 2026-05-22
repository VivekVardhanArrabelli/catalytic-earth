load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_2DLN.cif", m_csa_883
hide everything
show cartoon, m_csa_883
color gray70, m_csa_883
set cartoon_transparency, 0.8, m_csa_883
select m_csa_883_left, m_csa_883 and chain A and resi 270 and resn GLU
select m_csa_883_right, m_csa_883 and chain A and resi 216 and resn TYR
show sticks, m_csa_883_left or m_csa_883_right
color tv_red, m_csa_883_left
color tv_blue, m_csa_883_right
distance m_csa_883_distance, (m_csa_883 and chain A and resi 270 and resn GLU and name CA), (m_csa_883 and chain A and resi 216 and resn TYR and name CA)
label m_csa_883_distance, "18.890 A"
zoom m_csa_883_left or m_csa_883_right, 8
set dash_width, 3
set label_size, 18
