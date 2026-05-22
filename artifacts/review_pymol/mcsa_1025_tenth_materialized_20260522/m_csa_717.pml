load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_1X7D.cif", m_csa_717
hide everything
show cartoon, m_csa_717
color gray70, m_csa_717
set cartoon_transparency, 0.8, m_csa_717
select m_csa_717_left, m_csa_717 and chain A and resi 56 and resn GLU
select m_csa_717_right, m_csa_717 and chain A and resi 228 and resn ASP
show sticks, m_csa_717_left or m_csa_717_right
color tv_red, m_csa_717_left
color tv_blue, m_csa_717_right
distance m_csa_717_distance, (m_csa_717 and chain A and resi 56 and resn GLU and name CA), (m_csa_717 and chain A and resi 228 and resn ASP and name CA)
label m_csa_717_distance, "11.314 A"
zoom m_csa_717_left or m_csa_717_right, 8
set dash_width, 3
set label_size, 18
