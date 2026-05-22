load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_1FHL.cif", m_csa_658
hide everything
show cartoon, m_csa_658
color gray70, m_csa_658
set cartoon_transparency, 0.8, m_csa_658
select m_csa_658_left, m_csa_658 and chain A and resi 136 and resn GLU
select m_csa_658_right, m_csa_658 and chain A and resi 45 and resn ARG
show sticks, m_csa_658_left or m_csa_658_right
color tv_red, m_csa_658_left
color tv_blue, m_csa_658_right
distance m_csa_658_distance, (m_csa_658 and chain A and resi 136 and resn GLU and name CA), (m_csa_658 and chain A and resi 45 and resn ARG and name CA)
label m_csa_658_distance, "14.402 A"
zoom m_csa_658_left or m_csa_658_right, 8
set dash_width, 3
set label_size, 18
