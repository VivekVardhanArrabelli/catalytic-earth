load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_1OFG.cif", m_csa_868
hide everything
show cartoon, m_csa_868
color gray70, m_csa_868
set cartoon_transparency, 0.8, m_csa_868
select m_csa_868_left, m_csa_868 and chain A and resi 129 and resn LYS
select m_csa_868_right, m_csa_868 and chain A and resi 217 and resn TYR
show sticks, m_csa_868_left or m_csa_868_right
color tv_red, m_csa_868_left
color tv_blue, m_csa_868_right
distance m_csa_868_distance, (m_csa_868 and chain A and resi 129 and resn LYS and name CA), (m_csa_868 and chain A and resi 217 and resn TYR and name CA)
label m_csa_868_distance, "9.751 A"
zoom m_csa_868_left or m_csa_868_right, 8
set dash_width, 3
set label_size, 18
