load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_1RK2.cif", m_csa_663
hide everything
show cartoon, m_csa_663
color gray70, m_csa_663
set cartoon_transparency, 0.8, m_csa_663
select m_csa_663_left, m_csa_663 and chain A and resi 253 and resn ALA
select m_csa_663_right, m_csa_663 and chain A and resi 255 and resn ASP
show sticks, m_csa_663_left or m_csa_663_right
color tv_red, m_csa_663_left
color tv_blue, m_csa_663_right
distance m_csa_663_distance, (m_csa_663 and chain A and resi 253 and resn ALA and name CA), (m_csa_663 and chain A and resi 255 and resn ASP and name CA)
label m_csa_663_distance, "5.497 A"
zoom m_csa_663_left or m_csa_663_right, 8
set dash_width, 3
set label_size, 18
