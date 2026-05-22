load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_1DUP.cif", m_csa_844
hide everything
show cartoon, m_csa_844
color gray70, m_csa_844
set cartoon_transparency, 0.8, m_csa_844
select m_csa_844_left, m_csa_844 and chain A and resi 73 and resn GLY
select m_csa_844_right, m_csa_844 and chain A and resi 90 and resn ASP
show sticks, m_csa_844_left or m_csa_844_right
color tv_red, m_csa_844_left
color tv_blue, m_csa_844_right
distance m_csa_844_distance, (m_csa_844 and chain A and resi 73 and resn GLY and name CA), (m_csa_844 and chain A and resi 90 and resn ASP and name CA)
label m_csa_844_distance, "26.739 A"
zoom m_csa_844_left or m_csa_844_right, 8
set dash_width, 3
set label_size, 18
