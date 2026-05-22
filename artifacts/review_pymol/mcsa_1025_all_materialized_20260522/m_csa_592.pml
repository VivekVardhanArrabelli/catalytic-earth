load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_3IDH.cif", m_csa_592
hide everything
show cartoon, m_csa_592
color gray70, m_csa_592
set cartoon_transparency, 0.8, m_csa_592
select m_csa_592_left, m_csa_592 and chain A and resi 210 and resn ASP
select m_csa_592_right, m_csa_592 and chain A and resi 174 and resn LYS
show sticks, m_csa_592_left or m_csa_592_right
color tv_red, m_csa_592_left
color tv_blue, m_csa_592_right
distance m_csa_592_distance, (m_csa_592 and chain A and resi 210 and resn ASP and name CA), (m_csa_592 and chain A and resi 174 and resn LYS and name CA)
label m_csa_592_distance, "13.668 A"
zoom m_csa_592_left or m_csa_592_right, 8
set dash_width, 3
set label_size, 18
