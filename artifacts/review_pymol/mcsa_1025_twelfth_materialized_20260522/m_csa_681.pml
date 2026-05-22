load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_1GQ8.cif", m_csa_681
hide everything
show cartoon, m_csa_681
color gray70, m_csa_681
set cartoon_transparency, 0.8, m_csa_681
select m_csa_681_left, m_csa_681 and chain A and resi 225 and resn ARG
select m_csa_681_right, m_csa_681 and chain A and resi 113 and resn GLN
show sticks, m_csa_681_left or m_csa_681_right
color tv_red, m_csa_681_left
color tv_blue, m_csa_681_right
distance m_csa_681_distance, (m_csa_681 and chain A and resi 225 and resn ARG and name CA), (m_csa_681 and chain A and resi 113 and resn GLN and name CA)
label m_csa_681_distance, "16.324 A"
zoom m_csa_681_left or m_csa_681_right, 8
set dash_width, 3
set label_size, 18
