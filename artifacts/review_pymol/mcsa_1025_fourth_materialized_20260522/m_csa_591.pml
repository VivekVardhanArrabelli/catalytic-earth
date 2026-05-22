load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_1HFS.cif", m_csa_591
hide everything
show cartoon, m_csa_591
color gray70, m_csa_591
set cartoon_transparency, 0.8, m_csa_591
select m_csa_591_left, m_csa_591 and chain A and resi 124 and resn HIS
select m_csa_591_right, m_csa_591 and chain A and resi 115 and resn GLU
show sticks, m_csa_591_left or m_csa_591_right
color tv_red, m_csa_591_left
color tv_blue, m_csa_591_right
distance m_csa_591_distance, (m_csa_591 and chain A and resi 124 and resn HIS and name CA), (m_csa_591 and chain A and resi 115 and resn GLU and name CA)
label m_csa_591_distance, "10.619 A"
zoom m_csa_591_left or m_csa_591_right, 8
set dash_width, 3
set label_size, 18
