load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_5VSM.cif", m_csa_965
hide everything
show cartoon, m_csa_965
color gray70, m_csa_965
set cartoon_transparency, 0.8, m_csa_965
select m_csa_965_left, m_csa_965 and chain A and resi 40 and resn CYS
select m_csa_965_right, m_csa_965 and chain A and resi 47 and resn CYS
show sticks, m_csa_965_left or m_csa_965_right
color tv_red, m_csa_965_left
color tv_blue, m_csa_965_right
distance m_csa_965_distance, (m_csa_965 and chain A and resi 40 and resn CYS and name CA), (m_csa_965 and chain A and resi 47 and resn CYS and name CA)
label m_csa_965_distance, "10.325 A"
zoom m_csa_965_left or m_csa_965_right, 8
set dash_width, 3
set label_size, 18
