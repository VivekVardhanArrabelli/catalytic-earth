load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_1JXH.cif", m_csa_670
hide everything
show cartoon, m_csa_670
color gray70, m_csa_670
set cartoon_transparency, 0.8, m_csa_670
select m_csa_670_left, m_csa_670 and chain A and resi 230 and resn THR
select m_csa_670_right, m_csa_670 and chain A and resi 198 and resn LYS
show sticks, m_csa_670_left or m_csa_670_right
color tv_red, m_csa_670_left
color tv_blue, m_csa_670_right
distance m_csa_670_distance, (m_csa_670 and chain A and resi 230 and resn THR and name CA), (m_csa_670 and chain A and resi 198 and resn LYS and name CA)
label m_csa_670_distance, "15.194 A"
zoom m_csa_670_left or m_csa_670_right, 8
set dash_width, 3
set label_size, 18
