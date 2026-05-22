load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_1PEG.cif", m_csa_691
hide everything
show cartoon, m_csa_691
color gray70, m_csa_691
set cartoon_transparency, 0.8, m_csa_691
select m_csa_691_left, m_csa_691 and chain A and resi 267 and resn TYR
select m_csa_691_right, m_csa_691 and chain A and resi 162 and resn TYR
show sticks, m_csa_691_left or m_csa_691_right
color tv_red, m_csa_691_left
color tv_blue, m_csa_691_right
distance m_csa_691_distance, (m_csa_691 and chain A and resi 267 and resn TYR and name CA), (m_csa_691 and chain A and resi 162 and resn TYR and name CA)
label m_csa_691_distance, "11.859 A"
zoom m_csa_691_left or m_csa_691_right, 8
set dash_width, 3
set label_size, 18
