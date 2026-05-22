load "artifacts/v3_mcsa_pymol_twelfth_materialized_coordinates_20260522/pdb_5MY0.cif", m_csa_985
hide everything
show cartoon, m_csa_985
color gray70, m_csa_985
set cartoon_transparency, 0.8, m_csa_985
select m_csa_985_left, m_csa_985 and chain C and resi 683 and resn HIS
select m_csa_985_right, m_csa_985 and chain C and resi 499 and resn MET
show sticks, m_csa_985_left or m_csa_985_right
color tv_red, m_csa_985_left
color tv_blue, m_csa_985_right
distance m_csa_985_distance, (m_csa_985 and chain C and resi 683 and resn HIS and name CA), (m_csa_985 and chain C and resi 499 and resn MET and name CA)
label m_csa_985_distance, "12.520 A"
zoom m_csa_985_left or m_csa_985_right, 8
set dash_width, 3
set label_size, 18
