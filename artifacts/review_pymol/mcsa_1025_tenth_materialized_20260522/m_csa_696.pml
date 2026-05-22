load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_1DGK.cif", m_csa_696
hide everything
show cartoon, m_csa_696
color gray70, m_csa_696
set cartoon_transparency, 0.8, m_csa_696
select m_csa_696_left, m_csa_696 and chain N and resi 539 and resn ARG
select m_csa_696_right, m_csa_696 and chain N and resi 657 and resn ASP
show sticks, m_csa_696_left or m_csa_696_right
color tv_red, m_csa_696_left
color tv_blue, m_csa_696_right
distance m_csa_696_distance, (m_csa_696 and chain N and resi 539 and resn ARG and name CA), (m_csa_696 and chain N and resi 657 and resn ASP and name CA)
label m_csa_696_distance, "12.497 A"
zoom m_csa_696_left or m_csa_696_right, 8
set dash_width, 3
set label_size, 18
