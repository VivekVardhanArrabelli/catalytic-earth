load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_1A4Y.cif", m_csa_564
hide everything
show cartoon, m_csa_564
color gray70, m_csa_564
set cartoon_transparency, 0.8, m_csa_564
select m_csa_564_left, m_csa_564 and chain B and resi 40 and resn LYS
select m_csa_564_right, m_csa_564 and chain B and resi 114 and resn HIS
show sticks, m_csa_564_left or m_csa_564_right
color tv_red, m_csa_564_left
color tv_blue, m_csa_564_right
distance m_csa_564_distance, (m_csa_564 and chain B and resi 40 and resn LYS and name CA), (m_csa_564 and chain B and resi 114 and resn HIS and name CA)
label m_csa_564_distance, "15.348 A"
zoom m_csa_564_left or m_csa_564_right, 8
set dash_width, 3
set label_size, 18
