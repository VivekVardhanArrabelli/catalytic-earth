load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_1QV0.cif", m_csa_768
hide everything
show cartoon, m_csa_768
color gray70, m_csa_768
set cartoon_transparency, 0.8, m_csa_768
select m_csa_768_left, m_csa_768 and chain A and resi 92 and resn TRP
select m_csa_768_right, m_csa_768 and chain A and resi 138 and resn TYR
show sticks, m_csa_768_left or m_csa_768_right
color tv_red, m_csa_768_left
color tv_blue, m_csa_768_right
distance m_csa_768_distance, (m_csa_768 and chain A and resi 92 and resn TRP and name CA), (m_csa_768 and chain A and resi 138 and resn TYR and name CA)
label m_csa_768_distance, "22.795 A"
zoom m_csa_768_left or m_csa_768_right, 8
set dash_width, 3
set label_size, 18
