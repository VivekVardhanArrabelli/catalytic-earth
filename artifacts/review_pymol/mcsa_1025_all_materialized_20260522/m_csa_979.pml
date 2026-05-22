load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_3MVF.cif", m_csa_979
hide everything
show cartoon, m_csa_979
color gray70, m_csa_979
set cartoon_transparency, 0.8, m_csa_979
select m_csa_979_left, m_csa_979 and chain A and resi 59 and resn HIS
select m_csa_979_right, m_csa_979 and chain A and resi 130 and resn LEU
show sticks, m_csa_979_left or m_csa_979_right
color tv_red, m_csa_979_left
color tv_blue, m_csa_979_right
distance m_csa_979_distance, (m_csa_979 and chain A and resi 59 and resn HIS and name CA), (m_csa_979 and chain A and resi 130 and resn LEU and name CA)
label m_csa_979_distance, "16.400 A"
zoom m_csa_979_left or m_csa_979_right, 8
set dash_width, 3
set label_size, 18
