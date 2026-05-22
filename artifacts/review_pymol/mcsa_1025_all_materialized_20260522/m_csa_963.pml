load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_4EAY.cif", m_csa_963
hide everything
show cartoon, m_csa_963
color gray70, m_csa_963
set cartoon_transparency, 0.8, m_csa_963
select m_csa_963_left, m_csa_963 and chain A and resi 388 and resn TYR
select m_csa_963_right, m_csa_963 and chain A and resi 253 and resn HIS
show sticks, m_csa_963_left or m_csa_963_right
color tv_red, m_csa_963_left
color tv_blue, m_csa_963_right
distance m_csa_963_distance, (m_csa_963 and chain A and resi 388 and resn TYR and name CA), (m_csa_963 and chain A and resi 253 and resn HIS and name CA)
label m_csa_963_distance, "17.366 A"
zoom m_csa_963_left or m_csa_963_right, 8
set dash_width, 3
set label_size, 18
