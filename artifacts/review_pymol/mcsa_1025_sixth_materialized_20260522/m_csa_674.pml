load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_1UF7.cif", m_csa_674
hide everything
show cartoon, m_csa_674
color gray70, m_csa_674
set cartoon_transparency, 0.8, m_csa_674
select m_csa_674_left, m_csa_674 and chain A and resi 46 and resn GLU
select m_csa_674_right, m_csa_674 and chain A and resi 126 and resn LYS
show sticks, m_csa_674_left or m_csa_674_right
color tv_red, m_csa_674_left
color tv_blue, m_csa_674_right
distance m_csa_674_distance, (m_csa_674 and chain A and resi 46 and resn GLU and name CA), (m_csa_674 and chain A and resi 126 and resn LYS and name CA)
label m_csa_674_distance, "9.683 A"
zoom m_csa_674_left or m_csa_674_right, 8
set dash_width, 3
set label_size, 18
