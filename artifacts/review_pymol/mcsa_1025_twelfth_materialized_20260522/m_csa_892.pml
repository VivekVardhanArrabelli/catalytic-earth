load "artifacts/v3_mcsa_pymol_twelfth_materialized_coordinates_20260522/pdb_2DOR.cif", m_csa_892
hide everything
show cartoon, m_csa_892
color gray70, m_csa_892
set cartoon_transparency, 0.8, m_csa_892
select m_csa_892_left, m_csa_892 and chain A and resi 43 and resn LYS
select m_csa_892_right, m_csa_892 and chain A and resi 130 and resn CYS
show sticks, m_csa_892_left or m_csa_892_right
color tv_red, m_csa_892_left
color tv_blue, m_csa_892_right
distance m_csa_892_distance, (m_csa_892 and chain A and resi 43 and resn LYS and name CA), (m_csa_892 and chain A and resi 130 and resn CYS and name CA)
label m_csa_892_distance, "11.869 A"
zoom m_csa_892_left or m_csa_892_right, 8
set dash_width, 3
set label_size, 18
