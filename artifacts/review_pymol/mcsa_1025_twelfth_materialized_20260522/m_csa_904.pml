load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_1QGX.cif", m_csa_904
hide everything
show cartoon, m_csa_904
color gray70, m_csa_904
set cartoon_transparency, 0.8, m_csa_904
select m_csa_904_left, m_csa_904 and chain A and resi 49 and resn ASP
select m_csa_904_right, m_csa_904 and chain A and resi 294 and resn ASP
show sticks, m_csa_904_left or m_csa_904_right
color tv_red, m_csa_904_left
color tv_blue, m_csa_904_right
distance m_csa_904_distance, (m_csa_904 and chain A and resi 49 and resn ASP and name CA), (m_csa_904 and chain A and resi 294 and resn ASP and name CA)
label m_csa_904_distance, "14.055 A"
zoom m_csa_904_left or m_csa_904_right, 8
set dash_width, 3
set label_size, 18
