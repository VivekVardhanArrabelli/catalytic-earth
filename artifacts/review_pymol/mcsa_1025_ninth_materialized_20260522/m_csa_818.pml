load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_1QTN.cif", m_csa_818
hide everything
show cartoon, m_csa_818
color gray70, m_csa_818
set cartoon_transparency, 0.8, m_csa_818
select m_csa_818_left, m_csa_818 and chain A and resi 150 and resn CYS
select m_csa_818_right, m_csa_818 and chain A and resi 48 and resn ARG
show sticks, m_csa_818_left or m_csa_818_right
color tv_red, m_csa_818_left
color tv_blue, m_csa_818_right
distance m_csa_818_distance, (m_csa_818 and chain A and resi 150 and resn CYS and name CA), (m_csa_818 and chain A and resi 48 and resn ARG and name CA)
label m_csa_818_distance, "12.453 A"
zoom m_csa_818_left or m_csa_818_right, 8
set dash_width, 3
set label_size, 18
