load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_1HRK.cif", m_csa_578
hide everything
show cartoon, m_csa_578
color gray70, m_csa_578
set cartoon_transparency, 0.8, m_csa_578
select m_csa_578_left, m_csa_578 and chain A and resi 28 and resn LEU
select m_csa_578_right, m_csa_578 and chain A and resi 279 and resn GLU
show sticks, m_csa_578_left or m_csa_578_right
color tv_red, m_csa_578_left
color tv_blue, m_csa_578_right
distance m_csa_578_distance, (m_csa_578 and chain A and resi 28 and resn LEU and name CA), (m_csa_578 and chain A and resi 279 and resn GLU and name CA)
label m_csa_578_distance, "24.503 A"
zoom m_csa_578_left or m_csa_578_right, 8
set dash_width, 3
set label_size, 18
