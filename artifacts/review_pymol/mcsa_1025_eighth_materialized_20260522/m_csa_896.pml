load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_2PEC.cif", m_csa_896
hide everything
show cartoon, m_csa_896
color gray70, m_csa_896
set cartoon_transparency, 0.8, m_csa_896
select m_csa_896_left, m_csa_896 and chain A and resi 129 and resn ASP
select m_csa_896_right, m_csa_896 and chain A and resi 218 and resn ARG
show sticks, m_csa_896_left or m_csa_896_right
color tv_red, m_csa_896_left
color tv_blue, m_csa_896_right
distance m_csa_896_distance, (m_csa_896 and chain A and resi 129 and resn ASP and name CA), (m_csa_896 and chain A and resi 218 and resn ARG and name CA)
label m_csa_896_distance, "16.556 A"
zoom m_csa_896_left or m_csa_896_right, 8
set dash_width, 3
set label_size, 18
