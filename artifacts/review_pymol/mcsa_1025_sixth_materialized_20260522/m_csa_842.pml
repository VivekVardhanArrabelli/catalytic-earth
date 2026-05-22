load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_1DQR.cif", m_csa_842
hide everything
show cartoon, m_csa_842
color gray70, m_csa_842
set cartoon_transparency, 0.8, m_csa_842
select m_csa_842_left, m_csa_842 and chain A and resi 216 and resn GLU
select m_csa_842_right, m_csa_842 and chain A and resi 357 and resn GLU
show sticks, m_csa_842_left or m_csa_842_right
color tv_red, m_csa_842_left
color tv_blue, m_csa_842_right
distance m_csa_842_distance, (m_csa_842 and chain A and resi 216 and resn GLU and name CA), (m_csa_842 and chain A and resi 357 and resn GLU and name CA)
label m_csa_842_distance, "18.453 A"
zoom m_csa_842_left or m_csa_842_right, 8
set dash_width, 3
set label_size, 18
