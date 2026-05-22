load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_2RNF.cif", m_csa_693
hide everything
show cartoon, m_csa_693
color gray70, m_csa_693
set cartoon_transparency, 0.8, m_csa_693
select m_csa_693_left, m_csa_693 and chain A and resi 41 and resn LYS
select m_csa_693_right, m_csa_693 and chain A and resi 117 and resn HIS
show sticks, m_csa_693_left or m_csa_693_right
color tv_red, m_csa_693_left
color tv_blue, m_csa_693_right
distance m_csa_693_distance, (m_csa_693 and chain A and resi 41 and resn LYS and name CA), (m_csa_693 and chain A and resi 117 and resn HIS and name CA)
label m_csa_693_distance, "15.505 A"
zoom m_csa_693_left or m_csa_693_right, 8
set dash_width, 3
set label_size, 18
