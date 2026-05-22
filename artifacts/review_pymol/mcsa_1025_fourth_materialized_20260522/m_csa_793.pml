load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_1QWN.cif", m_csa_793
hide everything
show cartoon, m_csa_793
color gray70, m_csa_793
set cartoon_transparency, 0.8, m_csa_793
select m_csa_793_left, m_csa_793 and chain A and resi 471 and resn HIS
select m_csa_793_right, m_csa_793 and chain A and resi 341 and resn ASP
show sticks, m_csa_793_left or m_csa_793_right
color tv_red, m_csa_793_left
color tv_blue, m_csa_793_right
distance m_csa_793_distance, (m_csa_793 and chain A and resi 471 and resn HIS and name CA), (m_csa_793 and chain A and resi 341 and resn ASP and name CA)
label m_csa_793_distance, "13.782 A"
zoom m_csa_793_left or m_csa_793_right, 8
set dash_width, 3
set label_size, 18
