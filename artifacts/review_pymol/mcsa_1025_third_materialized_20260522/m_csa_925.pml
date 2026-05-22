load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_2BII.cif", m_csa_925
hide everything
show cartoon, m_csa_925
color gray70, m_csa_925
set cartoon_transparency, 0.8, m_csa_925
select m_csa_925_left, m_csa_925 and chain B and resi 211 and resn ASP
select m_csa_925_right, m_csa_925 and chain B and resi 79 and resn CYS
show sticks, m_csa_925_left or m_csa_925_right
color tv_red, m_csa_925_left
color tv_blue, m_csa_925_right
distance m_csa_925_distance, (m_csa_925 and chain B and resi 211 and resn ASP and name CA), (m_csa_925 and chain B and resi 79 and resn CYS and name CA)
label m_csa_925_distance, "11.928 A"
zoom m_csa_925_left or m_csa_925_right, 8
set dash_width, 3
set label_size, 18
