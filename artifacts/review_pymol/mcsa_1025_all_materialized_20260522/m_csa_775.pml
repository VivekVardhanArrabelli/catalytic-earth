load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_2CY0.cif", m_csa_775
hide everything
show cartoon, m_csa_775
color gray70, m_csa_775
set cartoon_transparency, 0.8, m_csa_775
select m_csa_775_left, m_csa_775 and chain A and resi 64 and resn LYS
select m_csa_775_right, m_csa_775 and chain A and resi 100 and resn ASP
show sticks, m_csa_775_left or m_csa_775_right
color tv_red, m_csa_775_left
color tv_blue, m_csa_775_right
distance m_csa_775_distance, (m_csa_775 and chain A and resi 64 and resn LYS and name CA), (m_csa_775 and chain A and resi 100 and resn ASP and name CA)
label m_csa_775_distance, "11.068 A"
zoom m_csa_775_left or m_csa_775_right, 8
set dash_width, 3
set label_size, 18
