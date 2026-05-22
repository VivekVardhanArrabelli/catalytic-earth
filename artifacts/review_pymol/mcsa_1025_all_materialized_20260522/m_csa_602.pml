load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_1KEZ.cif", m_csa_602
hide everything
show cartoon, m_csa_602
color gray70, m_csa_602
set cartoon_transparency, 0.8, m_csa_602
select m_csa_602_left, m_csa_602 and chain A and resi 259 and resn HIS
select m_csa_602_right, m_csa_602 and chain A and resi 143 and resn ALA
show sticks, m_csa_602_left or m_csa_602_right
color tv_red, m_csa_602_left
color tv_blue, m_csa_602_right
distance m_csa_602_distance, (m_csa_602 and chain A and resi 259 and resn HIS and name CA), (m_csa_602 and chain A and resi 143 and resn ALA and name CA)
label m_csa_602_distance, "11.482 A"
zoom m_csa_602_left or m_csa_602_right, 8
set dash_width, 3
set label_size, 18
