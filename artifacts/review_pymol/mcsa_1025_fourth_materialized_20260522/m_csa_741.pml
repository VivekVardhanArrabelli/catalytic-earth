load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_1KAE.cif", m_csa_741
hide everything
show cartoon, m_csa_741
color gray70, m_csa_741
set cartoon_transparency, 0.8, m_csa_741
select m_csa_741_left, m_csa_741 and chain B and resi 419 and resn HIS
select m_csa_741_right, m_csa_741 and chain A and resi 326 and resn GLU
show sticks, m_csa_741_left or m_csa_741_right
color tv_red, m_csa_741_left
color tv_blue, m_csa_741_right
distance m_csa_741_distance, (m_csa_741 and chain B and resi 419 and resn HIS and name CA), (m_csa_741 and chain A and resi 326 and resn GLU and name CA)
label m_csa_741_distance, "16.249 A"
zoom m_csa_741_left or m_csa_741_right, 8
set dash_width, 3
set label_size, 18
