load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_1GP1.cif", m_csa_851
hide everything
show cartoon, m_csa_851
color gray70, m_csa_851
set cartoon_transparency, 0.8, m_csa_851
select m_csa_851_left, m_csa_851 and chain A and resi 158 and resn TRP
select m_csa_851_right, m_csa_851 and chain A and resi 80 and resn GLN
show sticks, m_csa_851_left or m_csa_851_right
color tv_red, m_csa_851_left
color tv_blue, m_csa_851_right
distance m_csa_851_distance, (m_csa_851 and chain A and resi 158 and resn TRP and name CA), (m_csa_851 and chain A and resi 80 and resn GLN and name CA)
label m_csa_851_distance, "9.695 A"
zoom m_csa_851_left or m_csa_851_right, 8
set dash_width, 3
set label_size, 18
