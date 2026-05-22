load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_1UAS.cif", m_csa_913
hide everything
show cartoon, m_csa_913
color gray70, m_csa_913
set cartoon_transparency, 0.8, m_csa_913
select m_csa_913_left, m_csa_913 and chain A and resi 130 and resn ASP
select m_csa_913_right, m_csa_913 and chain A and resi 185 and resn ASP
show sticks, m_csa_913_left or m_csa_913_right
color tv_red, m_csa_913_left
color tv_blue, m_csa_913_right
distance m_csa_913_distance, (m_csa_913 and chain A and resi 130 and resn ASP and name CA), (m_csa_913 and chain A and resi 185 and resn ASP and name CA)
label m_csa_913_distance, "11.501 A"
zoom m_csa_913_left or m_csa_913_right, 8
set dash_width, 3
set label_size, 18
