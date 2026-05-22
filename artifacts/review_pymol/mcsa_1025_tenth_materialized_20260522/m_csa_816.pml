load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_1NW9.cif", m_csa_816
hide everything
show cartoon, m_csa_816
color gray70, m_csa_816
set cartoon_transparency, 0.8, m_csa_816
select m_csa_816_left, m_csa_816 and chain B and resi 99 and resn GLY
select m_csa_816_right, m_csa_816 and chain B and resi 39 and resn ARG
show sticks, m_csa_816_left or m_csa_816_right
color tv_red, m_csa_816_left
color tv_blue, m_csa_816_right
distance m_csa_816_distance, (m_csa_816 and chain B and resi 99 and resn GLY and name CA), (m_csa_816 and chain B and resi 39 and resn ARG and name CA)
label m_csa_816_distance, "11.784 A"
zoom m_csa_816_left or m_csa_816_right, 8
set dash_width, 3
set label_size, 18
