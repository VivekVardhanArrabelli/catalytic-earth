load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_1CJY.cif", m_csa_529
hide everything
show cartoon, m_csa_529
color gray70, m_csa_529
set cartoon_transparency, 0.8, m_csa_529
select m_csa_529_left, m_csa_529 and chain A and resi 200 and resn ARG
select m_csa_529_right, m_csa_529 and chain A and resi 549 and resn ASP
show sticks, m_csa_529_left or m_csa_529_right
color tv_red, m_csa_529_left
color tv_blue, m_csa_529_right
distance m_csa_529_distance, (m_csa_529 and chain A and resi 200 and resn ARG and name CA), (m_csa_529 and chain A and resi 549 and resn ASP and name CA)
label m_csa_529_distance, "15.972 A"
zoom m_csa_529_left or m_csa_529_right, 8
set dash_width, 3
set label_size, 18
