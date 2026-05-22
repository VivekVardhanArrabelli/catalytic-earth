load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_1OCL.cif", m_csa_726
hide everything
show cartoon, m_csa_726
color gray70, m_csa_726
set cartoon_transparency, 0.8, m_csa_726
select m_csa_726_left, m_csa_726 and chain A and resi 153 and resn GLY
select m_csa_726_right, m_csa_726 and chain A and resi 62 and resn LYS
show sticks, m_csa_726_left or m_csa_726_right
color tv_red, m_csa_726_left
color tv_blue, m_csa_726_right
distance m_csa_726_distance, (m_csa_726 and chain A and resi 153 and resn GLY and name CA), (m_csa_726 and chain A and resi 62 and resn LYS and name CA)
label m_csa_726_distance, "15.658 A"
zoom m_csa_726_left or m_csa_726_right, 8
set dash_width, 3
set label_size, 18
