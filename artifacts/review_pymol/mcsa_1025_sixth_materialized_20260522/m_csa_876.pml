load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_1P3D.cif", m_csa_876
hide everything
show cartoon, m_csa_876
color gray70, m_csa_876
set cartoon_transparency, 0.8, m_csa_876
select m_csa_876_left, m_csa_876 and chain A and resi 130 and resn THR
select m_csa_876_right, m_csa_876 and chain A and resi 173 and resn GLU
show sticks, m_csa_876_left or m_csa_876_right
color tv_red, m_csa_876_left
color tv_blue, m_csa_876_right
distance m_csa_876_distance, (m_csa_876 and chain A and resi 130 and resn THR and name CA), (m_csa_876 and chain A and resi 173 and resn GLU and name CA)
label m_csa_876_distance, "6.263 A"
zoom m_csa_876_left or m_csa_876_right, 8
set dash_width, 3
set label_size, 18
