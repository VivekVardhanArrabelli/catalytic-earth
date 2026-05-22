load "artifacts/v3_mcsa_pymol_twelfth_materialized_coordinates_20260522/pdb_1GP5.cif", m_csa_685
hide everything
show cartoon, m_csa_685
color gray70, m_csa_685
set cartoon_transparency, 0.8, m_csa_685
select m_csa_685_left, m_csa_685 and chain A and resi 288 and resn HIS
select m_csa_685_right, m_csa_685 and chain A and resi 213 and resn LYS
show sticks, m_csa_685_left or m_csa_685_right
color tv_red, m_csa_685_left
color tv_blue, m_csa_685_right
distance m_csa_685_distance, (m_csa_685 and chain A and resi 288 and resn HIS and name CA), (m_csa_685 and chain A and resi 213 and resn LYS and name CA)
label m_csa_685_distance, "16.476 A"
zoom m_csa_685_left or m_csa_685_right, 8
set dash_width, 3
set label_size, 18
