load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_1QHO.cif", m_csa_905
hide everything
show cartoon, m_csa_905
color gray70, m_csa_905
set cartoon_transparency, 0.8, m_csa_905
select m_csa_905_left, m_csa_905 and chain A and resi 228 and resn ASP
select m_csa_905_right, m_csa_905 and chain A and resi 329 and resn ASP
show sticks, m_csa_905_left or m_csa_905_right
color tv_red, m_csa_905_left
color tv_blue, m_csa_905_right
distance m_csa_905_distance, (m_csa_905 and chain A and resi 228 and resn ASP and name CA), (m_csa_905 and chain A and resi 329 and resn ASP and name CA)
label m_csa_905_distance, "12.038 A"
zoom m_csa_905_left or m_csa_905_right, 8
set dash_width, 3
set label_size, 18
