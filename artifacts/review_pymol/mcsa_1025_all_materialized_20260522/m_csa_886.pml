load "artifacts/v3_mcsa_pymol_twelfth_materialized_coordinates_20260522/pdb_1TDJ.cif", m_csa_886
hide everything
show cartoon, m_csa_886
color gray70, m_csa_886
set cartoon_transparency, 0.8, m_csa_886
select m_csa_886_left, m_csa_886 and chain A and resi 62 and resn LYS
select m_csa_886_right, m_csa_886 and chain A and resi 315 and resn SER
show sticks, m_csa_886_left or m_csa_886_right
color tv_red, m_csa_886_left
color tv_blue, m_csa_886_right
distance m_csa_886_distance, (m_csa_886 and chain A and resi 62 and resn LYS and name CA), (m_csa_886 and chain A and resi 315 and resn SER and name CA)
label m_csa_886_distance, "8.797 A"
zoom m_csa_886_left or m_csa_886_right, 8
set dash_width, 3
set label_size, 18
