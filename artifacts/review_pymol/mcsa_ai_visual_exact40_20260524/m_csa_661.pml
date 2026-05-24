# Review-only PyMOL focus script for m_csa:661
# arylsulfatase; target=metal_dependent_hydrolase
load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_1HDH.cif", m_csa_661
hide everything, m_csa_661
show cartoon, m_csa_661
color gray70, m_csa_661
set cartoon_transparency, 0.78, m_csa_661
select m_csa_661_left, m_csa_661 and chain A and resi 375 and resn LYS
select m_csa_661_right, m_csa_661 and chain A and resi 113 and resn LYS
show sticks, m_csa_661_left or m_csa_661_right
show spheres, (m_csa_661_left or m_csa_661_right) and name CA
color tv_red, m_csa_661_left
color tv_blue, m_csa_661_right
distance m_csa_661_distance, (m_csa_661 and chain A and resi 375 and resn LYS and name CA), (m_csa_661 and chain A and resi 113 and resn LYS and name CA)
label m_csa_661_distance, "17.772 A"
zoom m_csa_661_left or m_csa_661_right, 8
set dash_width, 3
set label_size, 18
set sphere_scale, 0.32
