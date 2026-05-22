load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_1NSF.cif", m_csa_642
hide everything
show cartoon, m_csa_642
color gray70, m_csa_642
set cartoon_transparency, 0.8, m_csa_642
select m_csa_642_left, m_csa_642 and chain A and resi 235 and resn LYS
select m_csa_642_right, m_csa_642 and chain A and resi 158 and resn LYS
show sticks, m_csa_642_left or m_csa_642_right
color tv_red, m_csa_642_left
color tv_blue, m_csa_642_right
distance m_csa_642_distance, (m_csa_642 and chain A and resi 235 and resn LYS and name CA), (m_csa_642 and chain A and resi 158 and resn LYS and name CA)
label m_csa_642_distance, "31.492 A"
zoom m_csa_642_left or m_csa_642_right, 8
set dash_width, 3
set label_size, 18
