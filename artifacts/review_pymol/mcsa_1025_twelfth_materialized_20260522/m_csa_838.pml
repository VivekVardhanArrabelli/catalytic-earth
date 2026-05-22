load "artifacts/v3_mcsa_pymol_twelfth_materialized_coordinates_20260522/pdb_1ZNV.cif", m_csa_838
hide everything
show cartoon, m_csa_838
color gray70, m_csa_838
set cartoon_transparency, 0.8, m_csa_838
select m_csa_838_left, m_csa_838 and chain B and resi 131 and resn HIS
select m_csa_838_right, m_csa_838 and chain B and resi 103 and resn GLU
show sticks, m_csa_838_left or m_csa_838_right
color tv_red, m_csa_838_left
color tv_blue, m_csa_838_right
distance m_csa_838_distance, (m_csa_838 and chain B and resi 131 and resn HIS and name CA), (m_csa_838 and chain B and resi 103 and resn GLU and name CA)
label m_csa_838_distance, "10.544 A"
zoom m_csa_838_left or m_csa_838_right, 8
set dash_width, 3
set label_size, 18
