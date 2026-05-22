load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_2QMJ.cif", m_csa_976
hide everything
show cartoon, m_csa_976
color gray70, m_csa_976
set cartoon_transparency, 0.8, m_csa_976
select m_csa_976_left, m_csa_976 and chain A and resi 406 and resn TRP
select m_csa_976_right, m_csa_976 and chain A and resi 539 and resn TRP
show sticks, m_csa_976_left or m_csa_976_right
color tv_red, m_csa_976_left
color tv_blue, m_csa_976_right
distance m_csa_976_distance, (m_csa_976 and chain A and resi 406 and resn TRP and name CA), (m_csa_976 and chain A and resi 539 and resn TRP and name CA)
label m_csa_976_distance, "20.114 A"
zoom m_csa_976_left or m_csa_976_right, 8
set dash_width, 3
set label_size, 18
