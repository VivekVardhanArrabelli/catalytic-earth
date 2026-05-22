load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_2FOK.cif", m_csa_927
hide everything
show cartoon, m_csa_927
color gray70, m_csa_927
set cartoon_transparency, 0.8, m_csa_927
select m_csa_927_left, m_csa_927 and chain A and resi 450 and resn ASP
select m_csa_927_right, m_csa_927 and chain A and resi 469 and resn LYS
show sticks, m_csa_927_left or m_csa_927_right
color tv_red, m_csa_927_left
color tv_blue, m_csa_927_right
distance m_csa_927_distance, (m_csa_927 and chain A and resi 450 and resn ASP and name CA), (m_csa_927 and chain A and resi 469 and resn LYS and name CA)
label m_csa_927_distance, "9.520 A"
zoom m_csa_927_left or m_csa_927_right, 8
set dash_width, 3
set label_size, 18
