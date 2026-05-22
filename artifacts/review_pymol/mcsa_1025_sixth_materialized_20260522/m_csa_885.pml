load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_2CJA.cif", m_csa_885
hide everything
show cartoon, m_csa_885
color gray70, m_csa_885
set cartoon_transparency, 0.8, m_csa_885
select m_csa_885_left, m_csa_885 and chain A and resi 481 and resn CYS
select m_csa_885_right, m_csa_885 and chain A and resi 358 and resn GLU
show sticks, m_csa_885_left or m_csa_885_right
color tv_red, m_csa_885_left
color tv_blue, m_csa_885_right
distance m_csa_885_distance, (m_csa_885 and chain A and resi 481 and resn CYS and name CA), (m_csa_885 and chain A and resi 358 and resn GLU and name CA)
label m_csa_885_distance, "22.034 A"
zoom m_csa_885_left or m_csa_885_right, 8
set dash_width, 3
set label_size, 18
