load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_1QHG.cif", m_csa_833
hide everything
show cartoon, m_csa_833
color gray70, m_csa_833
set cartoon_transparency, 0.8, m_csa_833
select m_csa_833_left, m_csa_833 and chain A and resi 223 and resn ASP
select m_csa_833_right, m_csa_833 and chain A and resi 610 and resn ARG
show sticks, m_csa_833_left or m_csa_833_right
color tv_red, m_csa_833_left
color tv_blue, m_csa_833_right
distance m_csa_833_distance, (m_csa_833 and chain A and resi 223 and resn ASP and name CA), (m_csa_833 and chain A and resi 610 and resn ARG and name CA)
label m_csa_833_distance, "19.538 A"
zoom m_csa_833_left or m_csa_833_right, 8
set dash_width, 3
set label_size, 18
