# Review-only PyMOL focus script for m_csa:668
# leishmanolysin; target=metal_dependent_hydrolase
load "artifacts/v3_mcsa_pymol_twelfth_materialized_coordinates_20260522/pdb_1LML.cif", m_csa_668
hide everything, m_csa_668
show cartoon, m_csa_668
color gray70, m_csa_668
set cartoon_transparency, 0.78, m_csa_668
select m_csa_668_left, m_csa_668 and chain A and resi 235 and resn HIS
select m_csa_668_right, m_csa_668 and chain A and resi 166 and resn GLU
show sticks, m_csa_668_left or m_csa_668_right
show spheres, (m_csa_668_left or m_csa_668_right) and name CA
color tv_red, m_csa_668_left
color tv_blue, m_csa_668_right
distance m_csa_668_distance, (m_csa_668 and chain A and resi 235 and resn HIS and name CA), (m_csa_668 and chain A and resi 166 and resn GLU and name CA)
label m_csa_668_distance, "10.900 A"
zoom m_csa_668_left or m_csa_668_right, 8
set dash_width, 3
set label_size, 18
set sphere_scale, 0.32
