load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_1EUU.cif", m_csa_835
hide everything
show cartoon, m_csa_835
color gray70, m_csa_835
set cartoon_transparency, 0.8, m_csa_835
select m_csa_835_left, m_csa_835 and chain A and resi 50 and resn ASP
select m_csa_835_right, m_csa_835 and chain A and resi 218 and resn GLU
show sticks, m_csa_835_left or m_csa_835_right
color tv_red, m_csa_835_left
color tv_blue, m_csa_835_right
distance m_csa_835_distance, (m_csa_835 and chain A and resi 50 and resn ASP and name CA), (m_csa_835 and chain A and resi 218 and resn GLU and name CA)
label m_csa_835_distance, "14.602 A"
zoom m_csa_835_left or m_csa_835_right, 8
set dash_width, 3
set label_size, 18
