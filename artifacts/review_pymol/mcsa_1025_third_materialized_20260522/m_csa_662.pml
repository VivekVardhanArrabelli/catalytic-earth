load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_1BO1.cif", m_csa_662
hide everything
show cartoon, m_csa_662
color gray70, m_csa_662
set cartoon_transparency, 0.8, m_csa_662
select m_csa_662_left, m_csa_662 and chain A and resi 278 and resn ASP
select m_csa_662_right, m_csa_662 and chain A and resi 150 and resn LYS
show sticks, m_csa_662_left or m_csa_662_right
color tv_red, m_csa_662_left
color tv_blue, m_csa_662_right
distance m_csa_662_distance, (m_csa_662 and chain A and resi 278 and resn ASP and name CA), (m_csa_662 and chain A and resi 150 and resn LYS and name CA)
label m_csa_662_distance, "17.534 A"
zoom m_csa_662_left or m_csa_662_right, 8
set dash_width, 3
set label_size, 18
