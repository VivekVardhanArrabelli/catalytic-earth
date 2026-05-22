load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_1V0E.cif", m_csa_829
hide everything
show cartoon, m_csa_829
color gray70, m_csa_829
set cartoon_transparency, 0.8, m_csa_829
select m_csa_829_left, m_csa_829 and chain A and resi 337 and resn GLU
select m_csa_829_right, m_csa_829 and chain A and resi 403 and resn ARG
show sticks, m_csa_829_left or m_csa_829_right
color tv_red, m_csa_829_left
color tv_blue, m_csa_829_right
distance m_csa_829_distance, (m_csa_829 and chain A and resi 337 and resn GLU and name CA), (m_csa_829 and chain A and resi 403 and resn ARG and name CA)
label m_csa_829_distance, "32.835 A"
zoom m_csa_829_left or m_csa_829_right, 8
set dash_width, 3
set label_size, 18
