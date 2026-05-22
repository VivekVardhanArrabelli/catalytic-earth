load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_2HXT.cif", m_csa_961
hide everything
show cartoon, m_csa_961
color gray70, m_csa_961
set cartoon_transparency, 0.8, m_csa_961
select m_csa_961_left, m_csa_961 and chain A and resi 324 and resn ASP
select m_csa_961_right, m_csa_961 and chain A and resi 220 and resn LYS
show sticks, m_csa_961_left or m_csa_961_right
color tv_red, m_csa_961_left
color tv_blue, m_csa_961_right
distance m_csa_961_distance, (m_csa_961 and chain A and resi 324 and resn ASP and name CA), (m_csa_961 and chain A and resi 220 and resn LYS and name CA)
label m_csa_961_distance, "18.275 A"
zoom m_csa_961_left or m_csa_961_right, 8
set dash_width, 3
set label_size, 18
