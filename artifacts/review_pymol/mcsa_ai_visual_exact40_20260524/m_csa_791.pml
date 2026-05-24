# Review-only PyMOL focus script for m_csa:791
# colicin-E9; target=metal_dependent_hydrolase
load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_1FR2.cif", m_csa_791
hide everything, m_csa_791
show cartoon, m_csa_791
color gray70, m_csa_791
set cartoon_transparency, 0.78, m_csa_791
select m_csa_791_left, m_csa_791 and chain B and resi 96 and resn ARG
select m_csa_791_right, m_csa_791 and chain B and resi 5 and resn ARG
show sticks, m_csa_791_left or m_csa_791_right
show spheres, (m_csa_791_left or m_csa_791_right) and name CA
color tv_red, m_csa_791_left
color tv_blue, m_csa_791_right
distance m_csa_791_distance, (m_csa_791 and chain B and resi 96 and resn ARG and name CA), (m_csa_791 and chain B and resi 5 and resn ARG and name CA)
label m_csa_791_distance, "19.640 A"
zoom m_csa_791_left or m_csa_791_right, 8
set dash_width, 3
set label_size, 18
set sphere_scale, 0.32
