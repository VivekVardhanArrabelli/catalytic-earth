load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_2HW4.cif", m_csa_952
hide everything
show cartoon, m_csa_952
color gray70, m_csa_952
set cartoon_transparency, 0.8, m_csa_952
select m_csa_952_left, m_csa_952 and chain A and resi 115 and resn ALA
select m_csa_952_right, m_csa_952 and chain A and resi 97 and resn ARG
show sticks, m_csa_952_left or m_csa_952_right
color tv_red, m_csa_952_left
color tv_blue, m_csa_952_right
distance m_csa_952_distance, (m_csa_952 and chain A and resi 115 and resn ALA and name CA), (m_csa_952 and chain A and resi 97 and resn ARG and name CA)
label m_csa_952_distance, "13.522 A"
zoom m_csa_952_left or m_csa_952_right, 8
set dash_width, 3
set label_size, 18
