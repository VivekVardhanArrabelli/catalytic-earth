load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_3WQL.cif", m_csa_954
hide everything
show cartoon, m_csa_954
color gray70, m_csa_954
set cartoon_transparency, 0.8, m_csa_954
select m_csa_954_left, m_csa_954 and chain B and resi 34 and resn ASP
select m_csa_954_right, m_csa_954 and chain B and resi 90 and resn TYR
show sticks, m_csa_954_left or m_csa_954_right
color tv_red, m_csa_954_left
color tv_blue, m_csa_954_right
distance m_csa_954_distance, (m_csa_954 and chain B and resi 34 and resn ASP and name CA), (m_csa_954 and chain B and resi 90 and resn TYR and name CA)
label m_csa_954_distance, "16.976 A"
zoom m_csa_954_left or m_csa_954_right, 8
set dash_width, 3
set label_size, 18
