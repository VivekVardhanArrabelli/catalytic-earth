load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_1T0U.cif", m_csa_787
hide everything
show cartoon, m_csa_787
color gray70, m_csa_787
set cartoon_transparency, 0.8, m_csa_787
select m_csa_787_left, m_csa_787 and chain A and resi 80 and resn GLU
select m_csa_787_right, m_csa_787 and chain B and resi 223 and resn ARG
show sticks, m_csa_787_left or m_csa_787_right
color tv_red, m_csa_787_left
color tv_blue, m_csa_787_right
distance m_csa_787_distance, (m_csa_787 and chain A and resi 80 and resn GLU and name CA), (m_csa_787 and chain B and resi 223 and resn ARG and name CA)
label m_csa_787_distance, "19.225 A"
zoom m_csa_787_left or m_csa_787_right, 8
set dash_width, 3
set label_size, 18
