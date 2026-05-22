load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_2HWG.cif", m_csa_920
hide everything
show cartoon, m_csa_920
color gray70, m_csa_920
set cartoon_transparency, 0.8, m_csa_920
select m_csa_920_left, m_csa_920 and chain A and resi 502 and resn CYS
select m_csa_920_right, m_csa_920 and chain A and resi 455 and resn ASP
show sticks, m_csa_920_left or m_csa_920_right
color tv_red, m_csa_920_left
color tv_blue, m_csa_920_right
distance m_csa_920_distance, (m_csa_920 and chain A and resi 502 and resn CYS and name CA), (m_csa_920 and chain A and resi 455 and resn ASP and name CA)
label m_csa_920_distance, "10.676 A"
zoom m_csa_920_left or m_csa_920_right, 8
set dash_width, 3
set label_size, 18
