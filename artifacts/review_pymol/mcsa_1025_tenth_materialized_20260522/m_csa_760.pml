load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_1L0O.cif", m_csa_760
hide everything
show cartoon, m_csa_760
color gray70, m_csa_760
set cartoon_transparency, 0.8, m_csa_760
select m_csa_760_left, m_csa_760 and chain A and resi 46 and resn GLU
select m_csa_760_right, m_csa_760 and chain A and resi 105 and resn ARG
show sticks, m_csa_760_left or m_csa_760_right
color tv_red, m_csa_760_left
color tv_blue, m_csa_760_right
distance m_csa_760_distance, (m_csa_760 and chain A and resi 46 and resn GLU and name CA), (m_csa_760 and chain A and resi 105 and resn ARG and name CA)
label m_csa_760_distance, "11.655 A"
zoom m_csa_760_left or m_csa_760_right, 8
set dash_width, 3
set label_size, 18
