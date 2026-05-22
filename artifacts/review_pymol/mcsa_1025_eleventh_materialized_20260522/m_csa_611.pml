load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_1USH.cif", m_csa_611
hide everything
show cartoon, m_csa_611
color gray70, m_csa_611
set cartoon_transparency, 0.8, m_csa_611
select m_csa_611_left, m_csa_611 and chain A and resi 375 and resn ARG
select m_csa_611_right, m_csa_611 and chain A and resi 217 and resn HIS
show sticks, m_csa_611_left or m_csa_611_right
color tv_red, m_csa_611_left
color tv_blue, m_csa_611_right
distance m_csa_611_distance, (m_csa_611 and chain A and resi 375 and resn ARG and name CA), (m_csa_611 and chain A and resi 217 and resn HIS and name CA)
label m_csa_611_distance, "40.164 A"
zoom m_csa_611_left or m_csa_611_right, 8
set dash_width, 3
set label_size, 18
