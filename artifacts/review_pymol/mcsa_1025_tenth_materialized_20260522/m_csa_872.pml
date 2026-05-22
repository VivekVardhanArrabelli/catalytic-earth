load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_1OR8.cif", m_csa_872
hide everything
show cartoon, m_csa_872
color gray70, m_csa_872
set cartoon_transparency, 0.8, m_csa_872
select m_csa_872_left, m_csa_872 and chain A and resi 38 and resn ASP
select m_csa_872_right, m_csa_872 and chain A and resi 140 and resn GLU
show sticks, m_csa_872_left or m_csa_872_right
color tv_red, m_csa_872_left
color tv_blue, m_csa_872_right
distance m_csa_872_distance, (m_csa_872 and chain A and resi 38 and resn ASP and name CA), (m_csa_872 and chain A and resi 140 and resn GLU and name CA)
label m_csa_872_distance, "17.661 A"
zoom m_csa_872_left or m_csa_872_right, 8
set dash_width, 3
set label_size, 18
