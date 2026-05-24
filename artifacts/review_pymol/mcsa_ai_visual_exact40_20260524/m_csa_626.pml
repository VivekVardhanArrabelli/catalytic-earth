# Review-only PyMOL focus script for m_csa:626
# bontoxilysin; target=metal_dependent_hydrolase
load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_1EPW.cif", m_csa_626
hide everything, m_csa_626
show cartoon, m_csa_626
color gray70, m_csa_626
set cartoon_transparency, 0.78, m_csa_626
select m_csa_626_left, m_csa_626 and chain A and resi 233 and resn HIS
select m_csa_626_right, m_csa_626 and chain A and resi 369 and resn ARG
show sticks, m_csa_626_left or m_csa_626_right
show spheres, (m_csa_626_left or m_csa_626_right) and name CA
color tv_red, m_csa_626_left
color tv_blue, m_csa_626_right
distance m_csa_626_distance, (m_csa_626 and chain A and resi 233 and resn HIS and name CA), (m_csa_626 and chain A and resi 369 and resn ARG and name CA)
label m_csa_626_distance, "17.957 A"
zoom m_csa_626_left or m_csa_626_right, 8
set dash_width, 3
set label_size, 18
set sphere_scale, 0.32
