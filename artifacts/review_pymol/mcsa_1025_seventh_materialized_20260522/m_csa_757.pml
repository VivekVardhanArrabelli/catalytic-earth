load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_1STC.cif", m_csa_757
hide everything
show cartoon, m_csa_757
color gray70, m_csa_757
set cartoon_transparency, 0.8, m_csa_757
select m_csa_757_left, m_csa_757 and chain E and resi 184 and resn ASP
select m_csa_757_right, m_csa_757 and chain E and resi 201 and resn THR
show sticks, m_csa_757_left or m_csa_757_right
color tv_red, m_csa_757_left
color tv_blue, m_csa_757_right
distance m_csa_757_distance, (m_csa_757 and chain E and resi 184 and resn ASP and name CA), (m_csa_757 and chain E and resi 201 and resn THR and name CA)
label m_csa_757_distance, "13.582 A"
zoom m_csa_757_left or m_csa_757_right, 8
set dash_width, 3
set label_size, 18
