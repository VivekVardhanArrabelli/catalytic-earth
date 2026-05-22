load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_1J7G.cif", m_csa_748
hide everything
show cartoon, m_csa_748
color gray70, m_csa_748
set cartoon_transparency, 0.8, m_csa_748
select m_csa_748_left, m_csa_748 and chain A and resi 78 and resn GLN
select m_csa_748_right, m_csa_748 and chain A and resi 80 and resn THR
show sticks, m_csa_748_left or m_csa_748_right
color tv_red, m_csa_748_left
color tv_blue, m_csa_748_right
distance m_csa_748_distance, (m_csa_748 and chain A and resi 78 and resn GLN and name CA), (m_csa_748 and chain A and resi 80 and resn THR and name CA)
label m_csa_748_distance, "5.476 A"
zoom m_csa_748_left or m_csa_748_right, 8
set dash_width, 3
set label_size, 18
