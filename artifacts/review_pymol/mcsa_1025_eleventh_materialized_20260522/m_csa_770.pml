load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_1FOA.cif", m_csa_770
hide everything
show cartoon, m_csa_770
color gray70, m_csa_770
set cartoon_transparency, 0.8, m_csa_770
select m_csa_770_left, m_csa_770 and chain A and resi 114 and resn ASP
select m_csa_770_right, m_csa_770 and chain A and resi 192 and resn ASP
show sticks, m_csa_770_left or m_csa_770_right
color tv_red, m_csa_770_left
color tv_blue, m_csa_770_right
distance m_csa_770_distance, (m_csa_770 and chain A and resi 114 and resn ASP and name CA), (m_csa_770 and chain A and resi 192 and resn ASP and name CA)
label m_csa_770_distance, "16.305 A"
zoom m_csa_770_left or m_csa_770_right, 8
set dash_width, 3
set label_size, 18
