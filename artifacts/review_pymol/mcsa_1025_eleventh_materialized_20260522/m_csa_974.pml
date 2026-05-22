load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_4PIV.cif", m_csa_974
hide everything
show cartoon, m_csa_974
color gray70, m_csa_974
set cartoon_transparency, 0.8, m_csa_974
select m_csa_974_left, m_csa_974 and chain A and resi 561 and resn SER
select m_csa_974_right, m_csa_974 and chain A and resi 535 and resn LYS
show sticks, m_csa_974_left or m_csa_974_right
color tv_red, m_csa_974_left
color tv_blue, m_csa_974_right
distance m_csa_974_distance, (m_csa_974 and chain A and resi 561 and resn SER and name CA), (m_csa_974 and chain A and resi 535 and resn LYS and name CA)
label m_csa_974_distance, "11.763 A"
zoom m_csa_974_left or m_csa_974_right, 8
set dash_width, 3
set label_size, 18
