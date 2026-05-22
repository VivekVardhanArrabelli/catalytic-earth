load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_1QAM.cif", m_csa_898
hide everything
show cartoon, m_csa_898
color gray70, m_csa_898
set cartoon_transparency, 0.8, m_csa_898
select m_csa_898_left, m_csa_898 and chain A and resi 163 and resn PHE
select m_csa_898_right, m_csa_898 and chain A and resi 59 and resn GLU
show sticks, m_csa_898_left or m_csa_898_right
color tv_red, m_csa_898_left
color tv_blue, m_csa_898_right
distance m_csa_898_distance, (m_csa_898 and chain A and resi 163 and resn PHE and name CA), (m_csa_898 and chain A and resi 59 and resn GLU and name CA)
label m_csa_898_distance, "18.659 A"
zoom m_csa_898_left or m_csa_898_right, 8
set dash_width, 3
set label_size, 18
