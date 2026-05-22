load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_1HQC.cif", m_csa_780
hide everything
show cartoon, m_csa_780
color gray70, m_csa_780
set cartoon_transparency, 0.8, m_csa_780
select m_csa_780_left, m_csa_780 and chain A and resi 97 and resn ASP
select m_csa_780_right, m_csa_780 and chain A and resi 205 and resn ARG
show sticks, m_csa_780_left or m_csa_780_right
color tv_red, m_csa_780_left
color tv_blue, m_csa_780_right
distance m_csa_780_distance, (m_csa_780 and chain A and resi 97 and resn ASP and name CA), (m_csa_780 and chain A and resi 205 and resn ARG and name CA)
label m_csa_780_distance, "15.382 A"
zoom m_csa_780_left or m_csa_780_right, 8
set dash_width, 3
set label_size, 18
