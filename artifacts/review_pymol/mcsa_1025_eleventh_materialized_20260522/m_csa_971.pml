load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_2DE2.cif", m_csa_971
hide everything
show cartoon, m_csa_971
color gray70, m_csa_971
set cartoon_transparency, 0.8, m_csa_971
select m_csa_971_left, m_csa_971 and chain A and resi 60 and resn HIS
select m_csa_971_right, m_csa_971 and chain A and resi 73 and resn GLY
show sticks, m_csa_971_left or m_csa_971_right
color tv_red, m_csa_971_left
color tv_blue, m_csa_971_right
distance m_csa_971_distance, (m_csa_971 and chain A and resi 60 and resn HIS and name CA), (m_csa_971 and chain A and resi 73 and resn GLY and name CA)
label m_csa_971_distance, "19.035 A"
zoom m_csa_971_left or m_csa_971_right, 8
set dash_width, 3
set label_size, 18
