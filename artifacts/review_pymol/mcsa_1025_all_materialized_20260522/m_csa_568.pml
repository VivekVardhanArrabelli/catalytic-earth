load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_1GA8.cif", m_csa_568
hide everything
show cartoon, m_csa_568
color gray70, m_csa_568
set cartoon_transparency, 0.8, m_csa_568
select m_csa_568_left, m_csa_568 and chain A and resi 250 and resn LYS
select m_csa_568_right, m_csa_568 and chain A and resi 188 and resn ASP
show sticks, m_csa_568_left or m_csa_568_right
color tv_red, m_csa_568_left
color tv_blue, m_csa_568_right
distance m_csa_568_distance, (m_csa_568 and chain A and resi 250 and resn LYS and name CA), (m_csa_568 and chain A and resi 188 and resn ASP and name CA)
label m_csa_568_distance, "19.293 A"
zoom m_csa_568_left or m_csa_568_right, 8
set dash_width, 3
set label_size, 18
