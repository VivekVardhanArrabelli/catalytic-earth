load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_1STD.cif", m_csa_910
hide everything
show cartoon, m_csa_910
color gray70, m_csa_910
set cartoon_transparency, 0.8, m_csa_910
select m_csa_910_left, m_csa_910 and chain A and resi 50 and resn TYR
select m_csa_910_right, m_csa_910 and chain A and resi 31 and resn ASP
show sticks, m_csa_910_left or m_csa_910_right
color tv_red, m_csa_910_left
color tv_blue, m_csa_910_right
distance m_csa_910_distance, (m_csa_910 and chain A and resi 50 and resn TYR and name CA), (m_csa_910 and chain A and resi 31 and resn ASP and name CA)
label m_csa_910_distance, "19.593 A"
zoom m_csa_910_left or m_csa_910_right, 8
set dash_width, 3
set label_size, 18
