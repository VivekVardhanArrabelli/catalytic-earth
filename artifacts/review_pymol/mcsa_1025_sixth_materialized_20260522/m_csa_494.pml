load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_1DIO.cif", m_csa_494
hide everything
show cartoon, m_csa_494
color gray70, m_csa_494
set cartoon_transparency, 0.8, m_csa_494
select m_csa_494_left, m_csa_494 and chain A and resi 296 and resn GLN
select m_csa_494_right, m_csa_494 and chain A and resi 143 and resn HIS
show sticks, m_csa_494_left or m_csa_494_right
color tv_red, m_csa_494_left
color tv_blue, m_csa_494_right
distance m_csa_494_distance, (m_csa_494 and chain A and resi 296 and resn GLN and name CA), (m_csa_494 and chain A and resi 143 and resn HIS and name CA)
label m_csa_494_distance, "13.781 A"
zoom m_csa_494_left or m_csa_494_right, 8
set dash_width, 3
set label_size, 18
