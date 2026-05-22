load "artifacts/v3_mcsa_pymol_twelfth_materialized_coordinates_20260522/pdb_1JMS.cif", m_csa_632
hide everything
show cartoon, m_csa_632
color gray70, m_csa_632
set cartoon_transparency, 0.8, m_csa_632
select m_csa_632_left, m_csa_632 and chain A and resi 214 and resn ASP
select m_csa_632_right, m_csa_632 and chain A and resi 305 and resn ASP
show sticks, m_csa_632_left or m_csa_632_right
color tv_red, m_csa_632_left
color tv_blue, m_csa_632_right
distance m_csa_632_distance, (m_csa_632 and chain A and resi 214 and resn ASP and name CA), (m_csa_632 and chain A and resi 305 and resn ASP and name CA)
label m_csa_632_distance, "7.556 A"
zoom m_csa_632_left or m_csa_632_right, 8
set dash_width, 3
set label_size, 18
