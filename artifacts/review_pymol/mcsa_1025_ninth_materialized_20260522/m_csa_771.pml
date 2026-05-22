load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_1UK7.cif", m_csa_771
hide everything
show cartoon, m_csa_771
color gray70, m_csa_771
set cartoon_transparency, 0.8, m_csa_771
select m_csa_771_left, m_csa_771 and chain A and resi 34 and resn SER
select m_csa_771_right, m_csa_771 and chain A and resi 224 and resn ASP
show sticks, m_csa_771_left or m_csa_771_right
color tv_red, m_csa_771_left
color tv_blue, m_csa_771_right
distance m_csa_771_distance, (m_csa_771 and chain A and resi 34 and resn SER and name CA), (m_csa_771 and chain A and resi 224 and resn ASP and name CA)
label m_csa_771_distance, "15.052 A"
zoom m_csa_771_left or m_csa_771_right, 8
set dash_width, 3
set label_size, 18
