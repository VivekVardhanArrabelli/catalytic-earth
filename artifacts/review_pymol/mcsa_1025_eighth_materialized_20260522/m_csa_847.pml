load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_1EHY.cif", m_csa_847
hide everything
show cartoon, m_csa_847
color gray70, m_csa_847
set cartoon_transparency, 0.8, m_csa_847
select m_csa_847_left, m_csa_847 and chain A and resi 246 and resn ASP
select m_csa_847_right, m_csa_847 and chain A and resi 215 and resn TYR
show sticks, m_csa_847_left or m_csa_847_right
color tv_red, m_csa_847_left
color tv_blue, m_csa_847_right
distance m_csa_847_distance, (m_csa_847 and chain A and resi 246 and resn ASP and name CA), (m_csa_847 and chain A and resi 215 and resn TYR and name CA)
label m_csa_847_distance, "22.310 A"
zoom m_csa_847_left or m_csa_847_right, 8
set dash_width, 3
set label_size, 18
