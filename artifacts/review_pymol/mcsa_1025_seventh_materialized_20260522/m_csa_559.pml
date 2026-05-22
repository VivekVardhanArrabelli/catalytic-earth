load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_1JS4.cif", m_csa_559
hide everything
show cartoon, m_csa_559
color gray70, m_csa_559
set cartoon_transparency, 0.8, m_csa_559
select m_csa_559_left, m_csa_559 and chain A and resi 424 and resn GLU
select m_csa_559_right, m_csa_559 and chain A and resi 206 and resn TYR
show sticks, m_csa_559_left or m_csa_559_right
color tv_red, m_csa_559_left
color tv_blue, m_csa_559_right
distance m_csa_559_distance, (m_csa_559 and chain A and resi 424 and resn GLU and name CA), (m_csa_559 and chain A and resi 206 and resn TYR and name CA)
label m_csa_559_distance, "14.997 A"
zoom m_csa_559_left or m_csa_559_right, 8
set dash_width, 3
set label_size, 18
