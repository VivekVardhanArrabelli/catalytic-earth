load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_1RA0.cif", m_csa_710
hide everything
show cartoon, m_csa_710
color gray70, m_csa_710
set cartoon_transparency, 0.8, m_csa_710
select m_csa_710_left, m_csa_710 and chain A and resi 67 and resn HIS
select m_csa_710_right, m_csa_710 and chain A and resi 221 and resn GLU
show sticks, m_csa_710_left or m_csa_710_right
color tv_red, m_csa_710_left
color tv_blue, m_csa_710_right
distance m_csa_710_distance, (m_csa_710 and chain A and resi 67 and resn HIS and name CA), (m_csa_710 and chain A and resi 221 and resn GLU and name CA)
label m_csa_710_distance, "15.358 A"
zoom m_csa_710_left or m_csa_710_right, 8
set dash_width, 3
set label_size, 18
