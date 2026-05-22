load "artifacts/v3_mcsa_pymol_twelfth_materialized_coordinates_20260522/pdb_1RTD.cif", m_csa_1000
hide everything
show cartoon, m_csa_1000
color gray70, m_csa_1000
set cartoon_transparency, 0.8, m_csa_1000
select m_csa_1000_left, m_csa_1000 and chain A and resi 185 and resn ASP
select m_csa_1000_right, m_csa_1000 and chain A and resi 220 and resn LYS
show sticks, m_csa_1000_left or m_csa_1000_right
color tv_red, m_csa_1000_left
color tv_blue, m_csa_1000_right
distance m_csa_1000_distance, (m_csa_1000 and chain A and resi 185 and resn ASP and name CA), (m_csa_1000 and chain A and resi 220 and resn LYS and name CA)
label m_csa_1000_distance, "11.666 A"
zoom m_csa_1000_left or m_csa_1000_right, 8
set dash_width, 3
set label_size, 18
