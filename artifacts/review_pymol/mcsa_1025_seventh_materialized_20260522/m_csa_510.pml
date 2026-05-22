load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_1BIX.cif", m_csa_510
hide everything
show cartoon, m_csa_510
color gray70, m_csa_510
set cartoon_transparency, 0.8, m_csa_510
select m_csa_510_left, m_csa_510 and chain A and resi 277 and resn ASP
select m_csa_510_right, m_csa_510 and chain A and resi 140 and resn TYR
show sticks, m_csa_510_left or m_csa_510_right
color tv_red, m_csa_510_left
color tv_blue, m_csa_510_right
distance m_csa_510_distance, (m_csa_510 and chain A and resi 277 and resn ASP and name CA), (m_csa_510 and chain A and resi 140 and resn TYR and name CA)
label m_csa_510_distance, "14.513 A"
zoom m_csa_510_left or m_csa_510_right, 8
set dash_width, 3
set label_size, 18
