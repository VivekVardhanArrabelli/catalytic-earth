load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_2A0N.cif", m_csa_753
hide everything
show cartoon, m_csa_753
color gray70, m_csa_753
set cartoon_transparency, 0.8, m_csa_753
select m_csa_753_left, m_csa_753 and chain A and resi 23 and resn ASP
select m_csa_753_right, m_csa_753 and chain A and resi 142 and resn ASP
show sticks, m_csa_753_left or m_csa_753_right
color tv_red, m_csa_753_left
color tv_blue, m_csa_753_right
distance m_csa_753_distance, (m_csa_753 and chain A and resi 23 and resn ASP and name CA), (m_csa_753 and chain A and resi 142 and resn ASP and name CA)
label m_csa_753_distance, "16.043 A"
zoom m_csa_753_left or m_csa_753_right, 8
set dash_width, 3
set label_size, 18
