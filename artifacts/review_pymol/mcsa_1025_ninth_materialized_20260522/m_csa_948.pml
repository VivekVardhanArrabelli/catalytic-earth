load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_1M3S.cif", m_csa_948
hide everything
show cartoon, m_csa_948
color gray70, m_csa_948
set cartoon_transparency, 0.8, m_csa_948
select m_csa_948_left, m_csa_948 and chain A and resi 161 and resn ASP
select m_csa_948_right, m_csa_948 and chain B and resi 89 and resn SER
show sticks, m_csa_948_left or m_csa_948_right
color tv_red, m_csa_948_left
color tv_blue, m_csa_948_right
distance m_csa_948_distance, (m_csa_948 and chain A and resi 161 and resn ASP and name CA), (m_csa_948 and chain B and resi 89 and resn SER and name CA)
label m_csa_948_distance, "40.044 A"
zoom m_csa_948_left or m_csa_948_right, 8
set dash_width, 3
set label_size, 18
