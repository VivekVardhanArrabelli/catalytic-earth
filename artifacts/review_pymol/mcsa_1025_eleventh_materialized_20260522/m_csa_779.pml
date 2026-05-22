load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_1GOJ.cif", m_csa_779
hide everything
show cartoon, m_csa_779
color gray70, m_csa_779
set cartoon_transparency, 0.8, m_csa_779
select m_csa_779_left, m_csa_779 and chain A and resi 238 and resn GLY
select m_csa_779_right, m_csa_779 and chain A and resi 96 and resn TYR
show sticks, m_csa_779_left or m_csa_779_right
color tv_red, m_csa_779_left
color tv_blue, m_csa_779_right
distance m_csa_779_distance, (m_csa_779 and chain A and resi 238 and resn GLY and name CA), (m_csa_779 and chain A and resi 96 and resn TYR and name CA)
label m_csa_779_distance, "13.520 A"
zoom m_csa_779_left or m_csa_779_right, 8
set dash_width, 3
set label_size, 18
