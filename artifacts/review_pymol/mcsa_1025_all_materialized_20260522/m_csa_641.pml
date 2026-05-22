load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_1PWV.cif", m_csa_641
hide everything
show cartoon, m_csa_641
color gray70, m_csa_641
set cartoon_transparency, 0.8, m_csa_641
select m_csa_641_left, m_csa_641 and chain A and resi 690 and resn HIS
select m_csa_641_right, m_csa_641 and chain A and resi 728 and resn TYR
show sticks, m_csa_641_left or m_csa_641_right
color tv_red, m_csa_641_left
color tv_blue, m_csa_641_right
distance m_csa_641_distance, (m_csa_641 and chain A and resi 690 and resn HIS and name CA), (m_csa_641 and chain A and resi 728 and resn TYR and name CA)
label m_csa_641_distance, "13.968 A"
zoom m_csa_641_left or m_csa_641_right, 8
set dash_width, 3
set label_size, 18
