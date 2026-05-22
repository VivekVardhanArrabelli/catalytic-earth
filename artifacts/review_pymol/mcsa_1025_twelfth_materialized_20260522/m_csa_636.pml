load "artifacts/v3_mcsa_pymol_twelfth_materialized_coordinates_20260522/pdb_1UAQ.cif", m_csa_636
hide everything
show cartoon, m_csa_636
color gray70, m_csa_636
set cartoon_transparency, 0.8, m_csa_636
select m_csa_636_left, m_csa_636 and chain A and resi 62 and resn HIS
select m_csa_636_right, m_csa_636 and chain A and resi 89 and resn SER
show sticks, m_csa_636_left or m_csa_636_right
color tv_red, m_csa_636_left
color tv_blue, m_csa_636_right
distance m_csa_636_distance, (m_csa_636 and chain A and resi 62 and resn HIS and name CA), (m_csa_636 and chain A and resi 89 and resn SER and name CA)
label m_csa_636_distance, "11.674 A"
zoom m_csa_636_left or m_csa_636_right, 8
set dash_width, 3
set label_size, 18
