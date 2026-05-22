load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_5CNV.cif", m_csa_918
hide everything
show cartoon, m_csa_918
color gray70, m_csa_918
set cartoon_transparency, 0.8, m_csa_918
select m_csa_918_left, m_csa_918 and chain G and resi 115 and resn GLU
select m_csa_918_right, m_csa_918 and chain A and resi 462 and resn CYS
show sticks, m_csa_918_left or m_csa_918_right
color tv_red, m_csa_918_left
color tv_blue, m_csa_918_right
distance m_csa_918_distance, (m_csa_918 and chain G and resi 115 and resn GLU and name CA), (m_csa_918 and chain A and resi 462 and resn CYS and name CA)
label m_csa_918_distance, "77.359 A"
zoom m_csa_918_left or m_csa_918_right, 8
set dash_width, 3
set label_size, 18
