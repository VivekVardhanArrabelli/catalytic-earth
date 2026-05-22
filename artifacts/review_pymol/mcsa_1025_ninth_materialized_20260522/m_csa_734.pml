load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_2HI7.cif", m_csa_734
hide everything
show cartoon, m_csa_734
color gray70, m_csa_734
set cartoon_transparency, 0.8, m_csa_734
select m_csa_734_left, m_csa_734 and chain B and resi 48 and resn ARG
select m_csa_734_right, m_csa_734 and chain B and resi 104 and resn CYS
show sticks, m_csa_734_left or m_csa_734_right
color tv_red, m_csa_734_left
color tv_blue, m_csa_734_right
distance m_csa_734_distance, (m_csa_734 and chain B and resi 48 and resn ARG and name CA), (m_csa_734 and chain B and resi 104 and resn CYS and name CA)
label m_csa_734_distance, "17.362 A"
zoom m_csa_734_left or m_csa_734_right, 8
set dash_width, 3
set label_size, 18
