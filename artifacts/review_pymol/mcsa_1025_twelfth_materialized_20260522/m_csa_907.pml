load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_1RBL.cif", m_csa_907
hide everything
show cartoon, m_csa_907
color gray70, m_csa_907
set cartoon_transparency, 0.8, m_csa_907
select m_csa_907_left, m_csa_907 and chain A and resi 326 and resn LYS
select m_csa_907_right, m_csa_907 and chain A and resi 193 and resn LYS
show sticks, m_csa_907_left or m_csa_907_right
color tv_red, m_csa_907_left
color tv_blue, m_csa_907_right
distance m_csa_907_distance, (m_csa_907 and chain A and resi 326 and resn LYS and name CA), (m_csa_907 and chain A and resi 193 and resn LYS and name CA)
label m_csa_907_distance, "18.527 A"
zoom m_csa_907_left or m_csa_907_right, 8
set dash_width, 3
set label_size, 18
