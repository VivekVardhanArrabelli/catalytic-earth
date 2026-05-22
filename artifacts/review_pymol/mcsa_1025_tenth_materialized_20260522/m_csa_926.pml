load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_2EBN.cif", m_csa_926
hide everything
show cartoon, m_csa_926
color gray70, m_csa_926
set cartoon_transparency, 0.8, m_csa_926
select m_csa_926_left, m_csa_926 and chain A and resi 130 and resn ASP
select m_csa_926_right, m_csa_926 and chain A and resi 132 and resn GLU
show sticks, m_csa_926_left or m_csa_926_right
color tv_red, m_csa_926_left
color tv_blue, m_csa_926_right
distance m_csa_926_distance, (m_csa_926 and chain A and resi 130 and resn ASP and name CA), (m_csa_926 and chain A and resi 132 and resn GLU and name CA)
label m_csa_926_distance, "5.954 A"
zoom m_csa_926_left or m_csa_926_right, 8
set dash_width, 3
set label_size, 18
