load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_1PJQ.cif", m_csa_702
hide everything
show cartoon, m_csa_702
color gray70, m_csa_702
set cartoon_transparency, 0.8, m_csa_702
select m_csa_702_left, m_csa_702 and chain A and resi 270 and resn LYS
select m_csa_702_right, m_csa_702 and chain A and resi 382 and resn MET
show sticks, m_csa_702_left or m_csa_702_right
color tv_red, m_csa_702_left
color tv_blue, m_csa_702_right
distance m_csa_702_distance, (m_csa_702 and chain A and resi 270 and resn LYS and name CA), (m_csa_702 and chain A and resi 382 and resn MET and name CA)
label m_csa_702_distance, "16.138 A"
zoom m_csa_702_left or m_csa_702_right, 8
set dash_width, 3
set label_size, 18
