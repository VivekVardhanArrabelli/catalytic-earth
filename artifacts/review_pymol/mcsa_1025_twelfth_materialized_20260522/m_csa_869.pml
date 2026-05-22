load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_1OG1.cif", m_csa_869
hide everything
show cartoon, m_csa_869
color gray70, m_csa_869
set cartoon_transparency, 0.8, m_csa_869
select m_csa_869_left, m_csa_869 and chain A and resi 159 and resn GLU
select m_csa_869_right, m_csa_869 and chain A and resi 189 and resn GLU
show sticks, m_csa_869_left or m_csa_869_right
color tv_red, m_csa_869_left
color tv_blue, m_csa_869_right
distance m_csa_869_distance, (m_csa_869 and chain A and resi 159 and resn GLU and name CA), (m_csa_869 and chain A and resi 189 and resn GLU and name CA)
label m_csa_869_distance, "13.619 A"
zoom m_csa_869_left or m_csa_869_right, 8
set dash_width, 3
set label_size, 18
