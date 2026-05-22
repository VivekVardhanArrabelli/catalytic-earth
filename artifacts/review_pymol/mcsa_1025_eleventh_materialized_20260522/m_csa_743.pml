load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_1GQG.cif", m_csa_743
hide everything
show cartoon, m_csa_743
color gray70, m_csa_743
set cartoon_transparency, 0.8, m_csa_743
select m_csa_743_left, m_csa_743 and chain A and resi 66 and resn HIS
select m_csa_743_right, m_csa_743 and chain A and resi 73 and resn GLU
show sticks, m_csa_743_left or m_csa_743_right
color tv_red, m_csa_743_left
color tv_blue, m_csa_743_right
distance m_csa_743_distance, (m_csa_743 and chain A and resi 66 and resn HIS and name CA), (m_csa_743 and chain A and resi 73 and resn GLU and name CA)
label m_csa_743_distance, "12.129 A"
zoom m_csa_743_left or m_csa_743_right, 8
set dash_width, 3
set label_size, 18
