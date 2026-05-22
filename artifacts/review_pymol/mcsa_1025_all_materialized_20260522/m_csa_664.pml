load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_2DHN.cif", m_csa_664
hide everything
show cartoon, m_csa_664
color gray70, m_csa_664
set cartoon_transparency, 0.8, m_csa_664
select m_csa_664_left, m_csa_664 and chain A and resi 100 and resn LYS
select m_csa_664_right, m_csa_664 and chain A and resi 22 and resn GLU
show sticks, m_csa_664_left or m_csa_664_right
color tv_red, m_csa_664_left
color tv_blue, m_csa_664_right
distance m_csa_664_distance, (m_csa_664 and chain A and resi 100 and resn LYS and name CA), (m_csa_664 and chain A and resi 22 and resn GLU and name CA)
label m_csa_664_distance, "11.576 A"
zoom m_csa_664_left or m_csa_664_right, 8
set dash_width, 3
set label_size, 18
