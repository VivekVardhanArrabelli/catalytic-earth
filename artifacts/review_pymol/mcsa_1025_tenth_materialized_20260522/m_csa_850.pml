load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_1EUY.cif", m_csa_850
hide everything
show cartoon, m_csa_850
color gray70, m_csa_850
set cartoon_transparency, 0.8, m_csa_850
select m_csa_850_left, m_csa_850 and chain A and resi 35 and resn GLU
select m_csa_850_right, m_csa_850 and chain A and resi 261 and resn ARG
show sticks, m_csa_850_left or m_csa_850_right
color tv_red, m_csa_850_left
color tv_blue, m_csa_850_right
distance m_csa_850_distance, (m_csa_850 and chain A and resi 35 and resn GLU and name CA), (m_csa_850 and chain A and resi 261 and resn ARG and name CA)
label m_csa_850_distance, "16.088 A"
zoom m_csa_850_left or m_csa_850_right, 8
set dash_width, 3
set label_size, 18
