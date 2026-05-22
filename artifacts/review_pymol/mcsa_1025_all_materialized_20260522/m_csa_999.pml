load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_1T8U.cif", m_csa_999
hide everything
show cartoon, m_csa_999
color gray70, m_csa_999
set cartoon_transparency, 0.8, m_csa_999
select m_csa_999_left, m_csa_999 and chain A and resi 28 and resn LYS
select m_csa_999_right, m_csa_999 and chain A and resi 234 and resn LYS
show sticks, m_csa_999_left or m_csa_999_right
color tv_red, m_csa_999_left
color tv_blue, m_csa_999_right
distance m_csa_999_distance, (m_csa_999 and chain A and resi 28 and resn LYS and name CA), (m_csa_999 and chain A and resi 234 and resn LYS and name CA)
label m_csa_999_distance, "26.471 A"
zoom m_csa_999_left or m_csa_999_right, 8
set dash_width, 3
set label_size, 18
