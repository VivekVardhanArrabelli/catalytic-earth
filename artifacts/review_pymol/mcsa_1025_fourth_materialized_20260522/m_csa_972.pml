load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_2VZ9.cif", m_csa_972
hide everything
show cartoon, m_csa_972
color gray70, m_csa_972
set cartoon_transparency, 0.8, m_csa_972
select m_csa_972_left, m_csa_972 and chain A and resi 1037 and resn HIS
select m_csa_972_right, m_csa_972 and chain A and resi 885 and resn LEU
show sticks, m_csa_972_left or m_csa_972_right
color tv_red, m_csa_972_left
color tv_blue, m_csa_972_right
distance m_csa_972_distance, (m_csa_972 and chain A and resi 1037 and resn HIS and name CA), (m_csa_972 and chain A and resi 885 and resn LEU and name CA)
label m_csa_972_distance, "14.953 A"
zoom m_csa_972_left or m_csa_972_right, 8
set dash_width, 3
set label_size, 18
