load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_4H2H.cif", m_csa_940
hide everything
show cartoon, m_csa_940
color gray70, m_csa_940
set cartoon_transparency, 0.8, m_csa_940
select m_csa_940_left, m_csa_940 and chain A and resi 172 and resn LYS
select m_csa_940_right, m_csa_940 and chain A and resi 274 and resn LYS
show sticks, m_csa_940_left or m_csa_940_right
color tv_red, m_csa_940_left
color tv_blue, m_csa_940_right
distance m_csa_940_distance, (m_csa_940 and chain A and resi 172 and resn LYS and name CA), (m_csa_940 and chain A and resi 274 and resn LYS and name CA)
label m_csa_940_distance, "16.619 A"
zoom m_csa_940_left or m_csa_940_right, 8
set dash_width, 3
set label_size, 18
