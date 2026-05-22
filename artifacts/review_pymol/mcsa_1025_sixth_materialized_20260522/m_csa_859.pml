load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_1NF9.cif", m_csa_859
hide everything
show cartoon, m_csa_859
color gray70, m_csa_859
set cartoon_transparency, 0.8, m_csa_859
select m_csa_859_left, m_csa_859 and chain A and resi 37 and resn HIS
select m_csa_859_right, m_csa_859 and chain A and resi 122 and resn LYS
show sticks, m_csa_859_left or m_csa_859_right
color tv_red, m_csa_859_left
color tv_blue, m_csa_859_right
distance m_csa_859_distance, (m_csa_859 and chain A and resi 37 and resn HIS and name CA), (m_csa_859 and chain A and resi 122 and resn LYS and name CA)
label m_csa_859_distance, "9.053 A"
zoom m_csa_859_left or m_csa_859_right, 8
set dash_width, 3
set label_size, 18
