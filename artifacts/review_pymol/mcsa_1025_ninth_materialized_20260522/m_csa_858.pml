load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_1MRQ.cif", m_csa_858
hide everything
show cartoon, m_csa_858
color gray70, m_csa_858
set cartoon_transparency, 0.8, m_csa_858
select m_csa_858_left, m_csa_858 and chain A and resi 50 and resn ASP
select m_csa_858_right, m_csa_858 and chain A and resi 117 and resn HIS
show sticks, m_csa_858_left or m_csa_858_right
color tv_red, m_csa_858_left
color tv_blue, m_csa_858_right
distance m_csa_858_distance, (m_csa_858 and chain A and resi 50 and resn ASP and name CA), (m_csa_858 and chain A and resi 117 and resn HIS and name CA)
label m_csa_858_distance, "11.802 A"
zoom m_csa_858_left or m_csa_858_right, 8
set dash_width, 3
set label_size, 18
