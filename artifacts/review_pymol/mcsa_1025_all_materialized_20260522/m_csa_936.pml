load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_3PCA.cif", m_csa_936
hide everything
show cartoon, m_csa_936
color gray70, m_csa_936
set cartoon_transparency, 0.8, m_csa_936
select m_csa_936_left, m_csa_936 and chain M and resi 147 and resn TYR
select m_csa_936_right, m_csa_936 and chain M and resi 162 and resn HIS
show sticks, m_csa_936_left or m_csa_936_right
color tv_red, m_csa_936_left
color tv_blue, m_csa_936_right
distance m_csa_936_distance, (m_csa_936 and chain M and resi 147 and resn TYR and name CA), (m_csa_936 and chain M and resi 162 and resn HIS and name CA)
label m_csa_936_distance, "13.340 A"
zoom m_csa_936_left or m_csa_936_right, 8
set dash_width, 3
set label_size, 18
