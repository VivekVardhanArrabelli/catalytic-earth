load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_1JRP.cif", m_csa_698
hide everything
show cartoon, m_csa_698
color gray70, m_csa_698
set cartoon_transparency, 0.8, m_csa_698
select m_csa_698_left, m_csa_698 and chain B and resi 730 and resn GLU
select m_csa_698_right, m_csa_698 and chain B and resi 310 and resn ARG
show sticks, m_csa_698_left or m_csa_698_right
color tv_red, m_csa_698_left
color tv_blue, m_csa_698_right
distance m_csa_698_distance, (m_csa_698 and chain B and resi 730 and resn GLU and name CA), (m_csa_698 and chain B and resi 310 and resn ARG and name CA)
label m_csa_698_distance, "12.592 A"
zoom m_csa_698_left or m_csa_698_right, 8
set dash_width, 3
set label_size, 18
