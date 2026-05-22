load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_1KZH.cif", m_csa_653
hide everything
show cartoon, m_csa_653
color gray70, m_csa_653
set cartoon_transparency, 0.8, m_csa_653
select m_csa_653_left, m_csa_653 and chain A and resi 146 and resn ARG
select m_csa_653_right, m_csa_653 and chain A and resi 206 and resn ASP
show sticks, m_csa_653_left or m_csa_653_right
color tv_red, m_csa_653_left
color tv_blue, m_csa_653_right
distance m_csa_653_distance, (m_csa_653 and chain A and resi 146 and resn ARG and name CA), (m_csa_653 and chain A and resi 206 and resn ASP and name CA)
label m_csa_653_distance, "15.838 A"
zoom m_csa_653_left or m_csa_653_right, 8
set dash_width, 3
set label_size, 18
