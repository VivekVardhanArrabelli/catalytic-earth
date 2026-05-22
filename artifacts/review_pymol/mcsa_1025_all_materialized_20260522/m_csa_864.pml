load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_1OAC.cif", m_csa_864
hide everything
show cartoon, m_csa_864
color gray70, m_csa_864
set cartoon_transparency, 0.8, m_csa_864
select m_csa_864_left, m_csa_864 and chain A and resi 689 and resn HIS
select m_csa_864_right, m_csa_864 and chain A and resi 383 and resn ASP
show sticks, m_csa_864_left or m_csa_864_right
color tv_red, m_csa_864_left
color tv_blue, m_csa_864_right
distance m_csa_864_distance, (m_csa_864 and chain A and resi 689 and resn HIS and name CA), (m_csa_864 and chain A and resi 383 and resn ASP and name CA)
label m_csa_864_distance, "16.936 A"
zoom m_csa_864_left or m_csa_864_right, 8
set dash_width, 3
set label_size, 18
