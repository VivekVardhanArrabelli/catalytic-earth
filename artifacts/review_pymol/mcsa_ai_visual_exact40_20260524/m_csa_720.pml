# Review-only PyMOL focus script for m_csa:720
# creatininase; target=metal_dependent_hydrolase
load "artifacts/v3_mcsa_pymol_twelfth_materialized_coordinates_20260522/pdb_1J2U.cif", m_csa_720
hide everything, m_csa_720
show cartoon, m_csa_720
color gray70, m_csa_720
set cartoon_transparency, 0.78, m_csa_720
select m_csa_720_left, m_csa_720 and chain A and resi 183 and resn GLU
select m_csa_720_right, m_csa_720 and chain A and resi 122 and resn GLU
show sticks, m_csa_720_left or m_csa_720_right
show spheres, (m_csa_720_left or m_csa_720_right) and name CA
color tv_red, m_csa_720_left
color tv_blue, m_csa_720_right
distance m_csa_720_distance, (m_csa_720 and chain A and resi 183 and resn GLU and name CA), (m_csa_720 and chain A and resi 122 and resn GLU and name CA)
label m_csa_720_distance, "15.535 A"
zoom m_csa_720_left or m_csa_720_right, 8
set dash_width, 3
set label_size, 18
set sphere_scale, 0.32
