load "artifacts/v3_mcsa_pymol_twelfth_materialized_coordinates_20260522/pdb_1MHY.cif", m_csa_600
hide everything
show cartoon, m_csa_600
color gray70, m_csa_600
set cartoon_transparency, 0.8, m_csa_600
select m_csa_600_left, m_csa_600 and chain D and resi 142 and resn HIS
select m_csa_600_right, m_csa_600 and chain D and resi 204 and resn GLU
show sticks, m_csa_600_left or m_csa_600_right
color tv_red, m_csa_600_left
color tv_blue, m_csa_600_right
distance m_csa_600_distance, (m_csa_600 and chain D and resi 142 and resn HIS and name CA), (m_csa_600 and chain D and resi 204 and resn GLU and name CA)
label m_csa_600_distance, "13.073 A"
zoom m_csa_600_left or m_csa_600_right, 8
set dash_width, 3
set label_size, 18
