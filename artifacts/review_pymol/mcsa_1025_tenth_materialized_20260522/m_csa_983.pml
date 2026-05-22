load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_2IME.cif", m_csa_983
hide everything
show cartoon, m_csa_983
color gray70, m_csa_983
set cartoon_transparency, 0.8, m_csa_983
select m_csa_983_left, m_csa_983 and chain A and resi 11 and resn SER
select m_csa_983_right, m_csa_983 and chain A and resi 182 and resn ASP
show sticks, m_csa_983_left or m_csa_983_right
color tv_red, m_csa_983_left
color tv_blue, m_csa_983_right
distance m_csa_983_distance, (m_csa_983 and chain A and resi 11 and resn SER and name CA), (m_csa_983 and chain A and resi 182 and resn ASP and name CA)
label m_csa_983_distance, "13.718 A"
zoom m_csa_983_left or m_csa_983_right, 8
set dash_width, 3
set label_size, 18
