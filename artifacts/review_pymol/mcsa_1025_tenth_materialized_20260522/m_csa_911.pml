load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_1SZJ.cif", m_csa_911
hide everything
show cartoon, m_csa_911
color gray70, m_csa_911
set cartoon_transparency, 0.8, m_csa_911
select m_csa_911_left, m_csa_911 and chain G and resi 148 and resn CYS
select m_csa_911_right, m_csa_911 and chain G and resi 175 and resn HIS
show sticks, m_csa_911_left or m_csa_911_right
color tv_red, m_csa_911_left
color tv_blue, m_csa_911_right
distance m_csa_911_distance, (m_csa_911 and chain G and resi 148 and resn CYS and name CA), (m_csa_911 and chain G and resi 175 and resn HIS and name CA)
label m_csa_911_distance, "10.472 A"
zoom m_csa_911_left or m_csa_911_right, 8
set dash_width, 3
set label_size, 18
