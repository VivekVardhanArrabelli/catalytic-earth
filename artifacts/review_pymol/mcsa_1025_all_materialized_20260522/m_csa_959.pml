load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_3DG6.cif", m_csa_959
hide everything
show cartoon, m_csa_959
color gray70, m_csa_959
set cartoon_transparency, 0.8, m_csa_959
select m_csa_959_left, m_csa_959 and chain A and resi 162 and resn LYS
select m_csa_959_right, m_csa_959 and chain A and resi 266 and resn LYS
show sticks, m_csa_959_left or m_csa_959_right
color tv_red, m_csa_959_left
color tv_blue, m_csa_959_right
distance m_csa_959_distance, (m_csa_959 and chain A and resi 162 and resn LYS and name CA), (m_csa_959 and chain A and resi 266 and resn LYS and name CA)
label m_csa_959_distance, "17.129 A"
zoom m_csa_959_left or m_csa_959_right, 8
set dash_width, 3
set label_size, 18
