load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_1JH6.cif", m_csa_794
hide everything
show cartoon, m_csa_794
color gray70, m_csa_794
set cartoon_transparency, 0.8, m_csa_794
select m_csa_794_left, m_csa_794 and chain A and resi 117 and resn MET
select m_csa_794_right, m_csa_794 and chain A and resi 124 and resn TYR
show sticks, m_csa_794_left or m_csa_794_right
color tv_red, m_csa_794_left
color tv_blue, m_csa_794_right
distance m_csa_794_distance, (m_csa_794 and chain A and resi 117 and resn MET and name CA), (m_csa_794 and chain A and resi 124 and resn TYR and name CA)
label m_csa_794_distance, "16.513 A"
zoom m_csa_794_left or m_csa_794_right, 8
set dash_width, 3
set label_size, 18
