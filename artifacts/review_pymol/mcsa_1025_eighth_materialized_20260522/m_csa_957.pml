load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_1TKK.cif", m_csa_957
hide everything
show cartoon, m_csa_957
color gray70, m_csa_957
set cartoon_transparency, 0.8, m_csa_957
select m_csa_957_left, m_csa_957 and chain A and resi 162 and resn LYS
select m_csa_957_right, m_csa_957 and chain A and resi 268 and resn LYS
show sticks, m_csa_957_left or m_csa_957_right
color tv_red, m_csa_957_left
color tv_blue, m_csa_957_right
distance m_csa_957_distance, (m_csa_957 and chain A and resi 162 and resn LYS and name CA), (m_csa_957 and chain A and resi 268 and resn LYS and name CA)
label m_csa_957_distance, "17.208 A"
zoom m_csa_957_left or m_csa_957_right, 8
set dash_width, 3
set label_size, 18
