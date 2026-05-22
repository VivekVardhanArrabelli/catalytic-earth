load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_7NN9.cif", m_csa_828
hide everything
show cartoon, m_csa_828
color gray70, m_csa_828
set cartoon_transparency, 0.8, m_csa_828
select m_csa_828_left, m_csa_828 and chain A and resi 70 and resn ASP
select m_csa_828_right, m_csa_828 and chain A and resi 212 and resn ARG
show sticks, m_csa_828_left or m_csa_828_right
color tv_red, m_csa_828_left
color tv_blue, m_csa_828_right
distance m_csa_828_distance, (m_csa_828 and chain A and resi 70 and resn ASP and name CA), (m_csa_828 and chain A and resi 212 and resn ARG and name CA)
label m_csa_828_distance, "17.518 A"
zoom m_csa_828_left or m_csa_828_right, 8
set dash_width, 3
set label_size, 18
