# Review-only PyMOL focus script for m_csa:955
# tuberculosinol synthase; target=metal_dependent_hydrolase
load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_3WQL.cif", m_csa_955
hide everything, m_csa_955
show cartoon, m_csa_955
color gray70, m_csa_955
set cartoon_transparency, 0.78, m_csa_955
select m_csa_955_left, m_csa_955 and chain B and resi 51 and resn TYR
select m_csa_955_right, m_csa_955 and chain B and resi 34 and resn ASP
show sticks, m_csa_955_left or m_csa_955_right
show spheres, (m_csa_955_left or m_csa_955_right) and name CA
color tv_red, m_csa_955_left
color tv_blue, m_csa_955_right
distance m_csa_955_distance, (m_csa_955 and chain B and resi 51 and resn TYR and name CA), (m_csa_955 and chain B and resi 34 and resn ASP and name CA)
label m_csa_955_distance, "13.995 A"
zoom m_csa_955_left or m_csa_955_right, 8
set dash_width, 3
set label_size, 18
set sphere_scale, 0.32
