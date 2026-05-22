load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_2AYH.cif", m_csa_924
hide everything
show cartoon, m_csa_924
color gray70, m_csa_924
set cartoon_transparency, 0.8, m_csa_924
select m_csa_924_left, m_csa_924 and chain A and resi 105 and resn GLU
select m_csa_924_right, m_csa_924 and chain A and resi 109 and resn GLU
show sticks, m_csa_924_left or m_csa_924_right
color tv_red, m_csa_924_left
color tv_blue, m_csa_924_right
distance m_csa_924_distance, (m_csa_924 and chain A and resi 105 and resn GLU and name CA), (m_csa_924 and chain A and resi 109 and resn GLU and name CA)
label m_csa_924_distance, "12.083 A"
zoom m_csa_924_left or m_csa_924_right, 8
set dash_width, 3
set label_size, 18
