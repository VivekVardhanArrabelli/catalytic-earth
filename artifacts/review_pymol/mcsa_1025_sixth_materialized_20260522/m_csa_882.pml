load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_1QMH.cif", m_csa_882
hide everything
show cartoon, m_csa_882
color gray70, m_csa_882
set cartoon_transparency, 0.8, m_csa_882
select m_csa_882_left, m_csa_882 and chain A and resi 14 and resn GLU
select m_csa_882_right, m_csa_882 and chain A and resi 309 and resn HIS
show sticks, m_csa_882_left or m_csa_882_right
color tv_red, m_csa_882_left
color tv_blue, m_csa_882_right
distance m_csa_882_distance, (m_csa_882 and chain A and resi 14 and resn GLU and name CA), (m_csa_882 and chain A and resi 309 and resn HIS and name CA)
label m_csa_882_distance, "6.948 A"
zoom m_csa_882_left or m_csa_882_right, 8
set dash_width, 3
set label_size, 18
