load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_2P8B.cif", m_csa_958
hide everything
show cartoon, m_csa_958
color gray70, m_csa_958
set cartoon_transparency, 0.8, m_csa_958
select m_csa_958_left, m_csa_958 and chain A and resi 163 and resn LYS
select m_csa_958_right, m_csa_958 and chain A and resi 267 and resn LYS
show sticks, m_csa_958_left or m_csa_958_right
color tv_red, m_csa_958_left
color tv_blue, m_csa_958_right
distance m_csa_958_distance, (m_csa_958 and chain A and resi 163 and resn LYS and name CA), (m_csa_958 and chain A and resi 267 and resn LYS and name CA)
label m_csa_958_distance, "17.912 A"
zoom m_csa_958_left or m_csa_958_right, 8
set dash_width, 3
set label_size, 18
