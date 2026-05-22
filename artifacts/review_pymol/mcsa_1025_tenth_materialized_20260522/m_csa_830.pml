load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_2BX4.cif", m_csa_830
hide everything
show cartoon, m_csa_830
color gray70, m_csa_830
set cartoon_transparency, 0.8, m_csa_830
select m_csa_830_left, m_csa_830 and chain A and resi 143 and resn GLY
select m_csa_830_right, m_csa_830 and chain A and resi 41 and resn HIS
show sticks, m_csa_830_left or m_csa_830_right
color tv_red, m_csa_830_left
color tv_blue, m_csa_830_right
distance m_csa_830_distance, (m_csa_830 and chain A and resi 143 and resn GLY and name CA), (m_csa_830 and chain A and resi 41 and resn HIS and name CA)
label m_csa_830_distance, "12.802 A"
zoom m_csa_830_left or m_csa_830_right, 8
set dash_width, 3
set label_size, 18
