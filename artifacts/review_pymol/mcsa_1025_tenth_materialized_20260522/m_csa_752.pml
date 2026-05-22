load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_1VIE.cif", m_csa_752
hide everything
show cartoon, m_csa_752
color gray70, m_csa_752
set cartoon_transparency, 0.8, m_csa_752
select m_csa_752_left, m_csa_752 and chain A and resi 16 and resn LYS
select m_csa_752_right, m_csa_752 and chain A and resi 52 and resn ILE
show sticks, m_csa_752_left or m_csa_752_right
color tv_red, m_csa_752_left
color tv_blue, m_csa_752_right
distance m_csa_752_distance, (m_csa_752 and chain A and resi 16 and resn LYS and name CA), (m_csa_752 and chain A and resi 52 and resn ILE and name CA)
label m_csa_752_distance, "10.730 A"
zoom m_csa_752_left or m_csa_752_right, 8
set dash_width, 3
set label_size, 18
