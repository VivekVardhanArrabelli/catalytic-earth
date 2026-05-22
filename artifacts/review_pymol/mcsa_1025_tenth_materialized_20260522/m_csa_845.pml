load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_1DW9.cif", m_csa_845
hide everything
show cartoon, m_csa_845
color gray70, m_csa_845
set cartoon_transparency, 0.8, m_csa_845
select m_csa_845_left, m_csa_845 and chain D and resi 99 and resn GLU
select m_csa_845_right, m_csa_845 and chain A and resi 122 and resn SER
show sticks, m_csa_845_left or m_csa_845_right
color tv_red, m_csa_845_left
color tv_blue, m_csa_845_right
distance m_csa_845_distance, (m_csa_845 and chain D and resi 99 and resn GLU and name CA), (m_csa_845 and chain A and resi 122 and resn SER and name CA)
label m_csa_845_distance, "9.728 A"
zoom m_csa_845_left or m_csa_845_right, 8
set dash_width, 3
set label_size, 18
