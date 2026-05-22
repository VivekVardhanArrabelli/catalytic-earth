load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_1URO.cif", m_csa_914
hide everything
show cartoon, m_csa_914
color gray70, m_csa_914
set cartoon_transparency, 0.8, m_csa_914
select m_csa_914_left, m_csa_914 and chain A and resi 50 and resn ARG
select m_csa_914_right, m_csa_914 and chain A and resi 164 and resn TYR
show sticks, m_csa_914_left or m_csa_914_right
color tv_red, m_csa_914_left
color tv_blue, m_csa_914_right
distance m_csa_914_distance, (m_csa_914 and chain A and resi 50 and resn ARG and name CA), (m_csa_914 and chain A and resi 164 and resn TYR and name CA)
label m_csa_914_distance, "22.777 A"
zoom m_csa_914_left or m_csa_914_right, 8
set dash_width, 3
set label_size, 18
