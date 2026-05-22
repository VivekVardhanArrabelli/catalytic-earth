load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_4MHX.cif", m_csa_951
hide everything
show cartoon, m_csa_951
color gray70, m_csa_951
set cartoon_transparency, 0.8, m_csa_951
select m_csa_951_left, m_csa_951 and chain A and resi 282 and resn ARG
select m_csa_951_right, m_csa_951 and chain A and resi 123 and resn LYS
show sticks, m_csa_951_left or m_csa_951_right
color tv_red, m_csa_951_left
color tv_blue, m_csa_951_right
distance m_csa_951_distance, (m_csa_951 and chain A and resi 282 and resn ARG and name CA), (m_csa_951 and chain A and resi 123 and resn LYS and name CA)
label m_csa_951_distance, "17.326 A"
zoom m_csa_951_left or m_csa_951_right, 8
set dash_width, 3
set label_size, 18
