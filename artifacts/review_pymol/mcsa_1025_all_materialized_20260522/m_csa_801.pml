load "artifacts/v3_mcsa_pymol_twelfth_materialized_coordinates_20260522/pdb_1KWS.cif", m_csa_801
hide everything
show cartoon, m_csa_801
color gray70, m_csa_801
set cartoon_transparency, 0.8, m_csa_801
select m_csa_801_left, m_csa_801 and chain A and resi 122 and resn ASP
select m_csa_801_right, m_csa_801 and chain A and resi 207 and resn GLU
show sticks, m_csa_801_left or m_csa_801_right
color tv_red, m_csa_801_left
color tv_blue, m_csa_801_right
distance m_csa_801_distance, (m_csa_801 and chain A and resi 122 and resn ASP and name CA), (m_csa_801 and chain A and resi 207 and resn GLU and name CA)
label m_csa_801_distance, "17.213 A"
zoom m_csa_801_left or m_csa_801_right, 8
set dash_width, 3
set label_size, 18
