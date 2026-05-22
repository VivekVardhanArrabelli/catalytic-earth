load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_1IU4.cif", m_csa_761
hide everything
show cartoon, m_csa_761
color gray70, m_csa_761
set cartoon_transparency, 0.8, m_csa_761
select m_csa_761_left, m_csa_761 and chain A and resi 255 and resn ASP
select m_csa_761_right, m_csa_761 and chain A and resi 272 and resn TRP
show sticks, m_csa_761_left or m_csa_761_right
color tv_red, m_csa_761_left
color tv_blue, m_csa_761_right
distance m_csa_761_distance, (m_csa_761 and chain A and resi 255 and resn ASP and name CA), (m_csa_761 and chain A and resi 272 and resn TRP and name CA)
label m_csa_761_distance, "11.297 A"
zoom m_csa_761_left or m_csa_761_right, 8
set dash_width, 3
set label_size, 18
