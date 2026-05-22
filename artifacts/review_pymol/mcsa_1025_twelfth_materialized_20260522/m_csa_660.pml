load "artifacts/v3_mcsa_pymol_twelfth_materialized_coordinates_20260522/pdb_1DO6.cif", m_csa_660
hide everything
show cartoon, m_csa_660
color gray70, m_csa_660
set cartoon_transparency, 0.8, m_csa_660
select m_csa_660_left, m_csa_660 and chain A and resi 47 and resn HIS
select m_csa_660_right, m_csa_660 and chain A and resi 15 and resn LYS
show sticks, m_csa_660_left or m_csa_660_right
color tv_red, m_csa_660_left
color tv_blue, m_csa_660_right
distance m_csa_660_distance, (m_csa_660 and chain A and resi 47 and resn HIS and name CA), (m_csa_660 and chain A and resi 15 and resn LYS and name CA)
label m_csa_660_distance, "12.766 A"
zoom m_csa_660_left or m_csa_660_right, 8
set dash_width, 3
set label_size, 18
