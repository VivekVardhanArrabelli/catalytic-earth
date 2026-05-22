load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_1OZH.cif", m_csa_722
hide everything
show cartoon, m_csa_722
color gray70, m_csa_722
set cartoon_transparency, 0.8, m_csa_722
select m_csa_722_left, m_csa_722 and chain A and resi 474 and resn ASP
select m_csa_722_right, m_csa_722 and chain A and resi 422 and resn MET
show sticks, m_csa_722_left or m_csa_722_right
color tv_red, m_csa_722_left
color tv_blue, m_csa_722_right
distance m_csa_722_distance, (m_csa_722 and chain A and resi 474 and resn ASP and name CA), (m_csa_722 and chain A and resi 422 and resn MET and name CA)
label m_csa_722_distance, "15.345 A"
zoom m_csa_722_left or m_csa_722_right, 8
set dash_width, 3
set label_size, 18
