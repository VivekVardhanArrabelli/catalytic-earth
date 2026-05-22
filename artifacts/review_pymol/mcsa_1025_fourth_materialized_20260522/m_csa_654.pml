load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_1OJ4.cif", m_csa_654
hide everything
show cartoon, m_csa_654
color gray70, m_csa_654
set cartoon_transparency, 0.8, m_csa_654
select m_csa_654_left, m_csa_654 and chain A and resi 10 and resn LYS
select m_csa_654_right, m_csa_654 and chain A and resi 141 and resn ASP
show sticks, m_csa_654_left or m_csa_654_right
color tv_red, m_csa_654_left
color tv_blue, m_csa_654_right
distance m_csa_654_distance, (m_csa_654 and chain A and resi 10 and resn LYS and name CA), (m_csa_654 and chain A and resi 141 and resn ASP and name CA)
label m_csa_654_distance, "8.985 A"
zoom m_csa_654_left or m_csa_654_right, 8
set dash_width, 3
set label_size, 18
