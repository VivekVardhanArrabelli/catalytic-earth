load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_1QFN.cif", m_csa_792
hide everything
show cartoon, m_csa_792
color gray70, m_csa_792
set cartoon_transparency, 0.8, m_csa_792
select m_csa_792_left, m_csa_792 and chain A and resi 72 and resn TYR
select m_csa_792_right, m_csa_792 and chain A and resi 10 and resn GLY
show sticks, m_csa_792_left or m_csa_792_right
color tv_red, m_csa_792_left
color tv_blue, m_csa_792_right
distance m_csa_792_distance, (m_csa_792 and chain A and resi 72 and resn TYR and name CA), (m_csa_792 and chain A and resi 10 and resn GLY and name CA)
label m_csa_792_distance, "15.374 A"
zoom m_csa_792_left or m_csa_792_right, 8
set dash_width, 3
set label_size, 18
