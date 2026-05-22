load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_1VOM.cif", m_csa_534
hide everything
show cartoon, m_csa_534
color gray70, m_csa_534
set cartoon_transparency, 0.8, m_csa_534
select m_csa_534_left, m_csa_534 and chain A and resi 186 and resn THR
select m_csa_534_right, m_csa_534 and chain A and resi 459 and resn GLU
show sticks, m_csa_534_left or m_csa_534_right
color tv_red, m_csa_534_left
color tv_blue, m_csa_534_right
distance m_csa_534_distance, (m_csa_534 and chain A and resi 186 and resn THR and name CA), (m_csa_534 and chain A and resi 459 and resn GLU and name CA)
label m_csa_534_distance, "14.892 A"
zoom m_csa_534_left or m_csa_534_right, 8
set dash_width, 3
set label_size, 18
