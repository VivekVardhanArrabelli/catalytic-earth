load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_1J00.cif", m_csa_755
hide everything
show cartoon, m_csa_755
color gray70, m_csa_755
set cartoon_transparency, 0.8, m_csa_755
select m_csa_755_left, m_csa_755 and chain A and resi 44 and resn GLY
select m_csa_755_right, m_csa_755 and chain A and resi 154 and resn ASP
show sticks, m_csa_755_left or m_csa_755_right
color tv_red, m_csa_755_left
color tv_blue, m_csa_755_right
distance m_csa_755_distance, (m_csa_755 and chain A and resi 44 and resn GLY and name CA), (m_csa_755 and chain A and resi 154 and resn ASP and name CA)
label m_csa_755_distance, "14.718 A"
zoom m_csa_755_left or m_csa_755_right, 8
set dash_width, 3
set label_size, 18
