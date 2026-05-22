load "artifacts/v3_mcsa_pymol_twelfth_materialized_coordinates_20260522/pdb_1R1J.cif", m_csa_623
hide everything
show cartoon, m_csa_623
color gray70, m_csa_623
set cartoon_transparency, 0.8, m_csa_623
select m_csa_623_left, m_csa_623 and chain A and resi 534 and resn HIS
select m_csa_623_right, m_csa_623 and chain A and resi 664 and resn ARG
show sticks, m_csa_623_left or m_csa_623_right
color tv_red, m_csa_623_left
color tv_blue, m_csa_623_right
distance m_csa_623_distance, (m_csa_623 and chain A and resi 534 and resn HIS and name CA), (m_csa_623 and chain A and resi 664 and resn ARG and name CA)
label m_csa_623_distance, "15.438 A"
zoom m_csa_623_left or m_csa_623_right, 8
set dash_width, 3
set label_size, 18
