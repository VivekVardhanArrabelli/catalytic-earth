load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_1X9H.cif", m_csa_736
hide everything
show cartoon, m_csa_736
color gray70, m_csa_736
set cartoon_transparency, 0.8, m_csa_736
select m_csa_736_left, m_csa_736 and chain A and resi 135 and resn ARG
select m_csa_736_right, m_csa_736 and chain A and resi 298 and resn LYS
show sticks, m_csa_736_left or m_csa_736_right
color tv_red, m_csa_736_left
color tv_blue, m_csa_736_right
distance m_csa_736_distance, (m_csa_736 and chain A and resi 135 and resn ARG and name CA), (m_csa_736 and chain A and resi 298 and resn LYS and name CA)
label m_csa_736_distance, "15.903 A"
zoom m_csa_736_left or m_csa_736_right, 8
set dash_width, 3
set label_size, 18
