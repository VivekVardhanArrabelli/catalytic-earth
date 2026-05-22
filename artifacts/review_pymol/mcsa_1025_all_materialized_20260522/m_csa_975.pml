load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_4ECS.cif", m_csa_975
hide everything
show cartoon, m_csa_975
color gray70, m_csa_975
set cartoon_transparency, 0.8, m_csa_975
select m_csa_975_left, m_csa_975 and chain A and resi 58 and resn ARG
select m_csa_975_right, m_csa_975 and chain A and resi 116 and resn SER
show sticks, m_csa_975_left or m_csa_975_right
color tv_red, m_csa_975_left
color tv_blue, m_csa_975_right
distance m_csa_975_distance, (m_csa_975 and chain A and resi 58 and resn ARG and name CA), (m_csa_975 and chain A and resi 116 and resn SER and name CA)
label m_csa_975_distance, "21.887 A"
zoom m_csa_975_left or m_csa_975_right, 8
set dash_width, 3
set label_size, 18
