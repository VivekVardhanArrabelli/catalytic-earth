load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_1HR6.cif", m_csa_657
hide everything
show cartoon, m_csa_657
color gray70, m_csa_657
set cartoon_transparency, 0.8, m_csa_657
select m_csa_657_left, m_csa_657 and chain B and resi 131 and resn GLU
select m_csa_657_right, m_csa_657 and chain B and resi 54 and resn GLU
show sticks, m_csa_657_left or m_csa_657_right
color tv_red, m_csa_657_left
color tv_blue, m_csa_657_right
distance m_csa_657_distance, (m_csa_657 and chain B and resi 131 and resn GLU and name CA), (m_csa_657 and chain B and resi 54 and resn GLU and name CA)
label m_csa_657_distance, "13.228 A"
zoom m_csa_657_left or m_csa_657_right, 8
set dash_width, 3
set label_size, 18
