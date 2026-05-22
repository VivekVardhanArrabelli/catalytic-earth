load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_1RTU.cif", m_csa_908
hide everything
show cartoon, m_csa_908
color gray70, m_csa_908
set cartoon_transparency, 0.8, m_csa_908
select m_csa_908_left, m_csa_908 and chain A and resi 101 and resn HIS
select m_csa_908_right, m_csa_908 and chain A and resi 41 and resn HIS
show sticks, m_csa_908_left or m_csa_908_right
color tv_red, m_csa_908_left
color tv_blue, m_csa_908_right
distance m_csa_908_distance, (m_csa_908 and chain A and resi 101 and resn HIS and name CA), (m_csa_908 and chain A and resi 41 and resn HIS and name CA)
label m_csa_908_distance, "15.200 A"
zoom m_csa_908_left or m_csa_908_right, 8
set dash_width, 3
set label_size, 18
