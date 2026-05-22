load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_1RO7.cif", m_csa_840
hide everything
show cartoon, m_csa_840
color gray70, m_csa_840
set cartoon_transparency, 0.8, m_csa_840
select m_csa_840_left, m_csa_840 and chain A and resi 129 and resn ARG
select m_csa_840_right, m_csa_840 and chain A and resi 162 and resn TYR
show sticks, m_csa_840_left or m_csa_840_right
color tv_red, m_csa_840_left
color tv_blue, m_csa_840_right
distance m_csa_840_distance, (m_csa_840 and chain A and resi 129 and resn ARG and name CA), (m_csa_840 and chain A and resi 162 and resn TYR and name CA)
label m_csa_840_distance, "19.531 A"
zoom m_csa_840_left or m_csa_840_right, 8
set dash_width, 3
set label_size, 18
