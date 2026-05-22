load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_1DE3.cif", m_csa_832
hide everything
show cartoon, m_csa_832
color gray70, m_csa_832
set cartoon_transparency, 0.8, m_csa_832
select m_csa_832_left, m_csa_832 and chain A and resi 50 and resn HIS
select m_csa_832_right, m_csa_832 and chain A and resi 137 and resn HIS
show sticks, m_csa_832_left or m_csa_832_right
color tv_red, m_csa_832_left
color tv_blue, m_csa_832_right
distance m_csa_832_distance, (m_csa_832 and chain A and resi 50 and resn HIS and name CA), (m_csa_832 and chain A and resi 137 and resn HIS and name CA)
label m_csa_832_distance, "16.187 A"
zoom m_csa_832_left or m_csa_832_right, 8
set dash_width, 3
set label_size, 18
