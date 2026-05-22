load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_1PGS.cif", m_csa_878
hide everything
show cartoon, m_csa_878
color gray70, m_csa_878
set cartoon_transparency, 0.8, m_csa_878
select m_csa_878_left, m_csa_878 and chain A and resi 118 and resn GLU
select m_csa_878_right, m_csa_878 and chain A and resi 206 and resn GLU
show sticks, m_csa_878_left or m_csa_878_right
color tv_red, m_csa_878_left
color tv_blue, m_csa_878_right
distance m_csa_878_distance, (m_csa_878 and chain A and resi 118 and resn GLU and name CA), (m_csa_878 and chain A and resi 206 and resn GLU and name CA)
label m_csa_878_distance, "15.664 A"
zoom m_csa_878_left or m_csa_878_right, 8
set dash_width, 3
set label_size, 18
