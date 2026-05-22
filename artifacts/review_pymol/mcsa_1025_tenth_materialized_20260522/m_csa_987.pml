load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_3AMZ.cif", m_csa_987
hide everything
show cartoon, m_csa_987
color gray70, m_csa_987
set cartoon_transparency, 0.8, m_csa_987
select m_csa_987_left, m_csa_987 and chain A and resi 802 and resn GLU
select m_csa_987_right, m_csa_987 and chain A and resi 880 and resn ARG
show sticks, m_csa_987_left or m_csa_987_right
color tv_red, m_csa_987_left
color tv_blue, m_csa_987_right
distance m_csa_987_distance, (m_csa_987 and chain A and resi 802 and resn GLU and name CA), (m_csa_987 and chain A and resi 880 and resn ARG and name CA)
label m_csa_987_distance, "16.146 A"
zoom m_csa_987_left or m_csa_987_right, 8
set dash_width, 3
set label_size, 18
