load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_1PUD.cif", m_csa_881
hide everything
show cartoon, m_csa_881
color gray70, m_csa_881
set cartoon_transparency, 0.8, m_csa_881
select m_csa_881_left, m_csa_881 and chain A and resi 323 and resn CYS
select m_csa_881_right, m_csa_881 and chain A and resi 102 and resn ASP
show sticks, m_csa_881_left or m_csa_881_right
color tv_red, m_csa_881_left
color tv_blue, m_csa_881_right
distance m_csa_881_distance, (m_csa_881 and chain A and resi 323 and resn CYS and name CA), (m_csa_881 and chain A and resi 102 and resn ASP and name CA)
label m_csa_881_distance, "32.121 A"
zoom m_csa_881_left or m_csa_881_right, 8
set dash_width, 3
set label_size, 18
