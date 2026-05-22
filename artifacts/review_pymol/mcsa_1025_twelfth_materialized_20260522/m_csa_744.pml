load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_1AM2.cif", m_csa_744
hide everything
show cartoon, m_csa_744
color gray70, m_csa_744
set cartoon_transparency, 0.8, m_csa_744
select m_csa_744_left, m_csa_744 and chain A and resi 183 and resn VAL
select m_csa_744_right, m_csa_744 and chain A and resi 73 and resn THR
show sticks, m_csa_744_left or m_csa_744_right
color tv_red, m_csa_744_left
color tv_blue, m_csa_744_right
distance m_csa_744_distance, (m_csa_744 and chain A and resi 183 and resn VAL and name CA), (m_csa_744 and chain A and resi 73 and resn THR and name CA)
label m_csa_744_distance, "18.454 A"
zoom m_csa_744_left or m_csa_744_right, 8
set dash_width, 3
set label_size, 18
