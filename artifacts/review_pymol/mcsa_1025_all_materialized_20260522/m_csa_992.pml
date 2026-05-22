load "artifacts/v3_mcsa_pymol_twelfth_materialized_coordinates_20260522/pdb_4QRO.cif", m_csa_992
hide everything
show cartoon, m_csa_992
color gray70, m_csa_992
set cartoon_transparency, 0.8, m_csa_992
select m_csa_992_left, m_csa_992 and chain G and resi 164 and resn HIS
select m_csa_992_right, m_csa_992 and chain G and resi 10 and resn HIS
show sticks, m_csa_992_left or m_csa_992_right
color tv_red, m_csa_992_left
color tv_blue, m_csa_992_right
distance m_csa_992_distance, (m_csa_992 and chain G and resi 164 and resn HIS and name CA), (m_csa_992 and chain G and resi 10 and resn HIS and name CA)
label m_csa_992_distance, "11.197 A"
zoom m_csa_992_left or m_csa_992_right, 8
set dash_width, 3
set label_size, 18
