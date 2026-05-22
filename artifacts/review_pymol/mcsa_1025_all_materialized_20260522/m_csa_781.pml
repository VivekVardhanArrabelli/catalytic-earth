load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_1P4N.cif", m_csa_781
hide everything
show cartoon, m_csa_781
color gray70, m_csa_781
set cartoon_transparency, 0.8, m_csa_781
select m_csa_781_left, m_csa_781 and chain A and resi 304 and resn PHE
select m_csa_781_right, m_csa_781 and chain A and resi 36 and resn LYS
show sticks, m_csa_781_left or m_csa_781_right
color tv_red, m_csa_781_left
color tv_blue, m_csa_781_right
distance m_csa_781_distance, (m_csa_781 and chain A and resi 304 and resn PHE and name CA), (m_csa_781 and chain A and resi 36 and resn LYS and name CA)
label m_csa_781_distance, "28.848 A"
zoom m_csa_781_left or m_csa_781_right, 8
set dash_width, 3
set label_size, 18
