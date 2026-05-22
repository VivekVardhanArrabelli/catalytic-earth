load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_1NLN.cif", m_csa_679
hide everything
show cartoon, m_csa_679
color gray70, m_csa_679
set cartoon_transparency, 0.8, m_csa_679
select m_csa_679_left, m_csa_679 and chain A and resi 54 and resn HIS
select m_csa_679_right, m_csa_679 and chain A and resi 115 and resn GLN
show sticks, m_csa_679_left or m_csa_679_right
color tv_red, m_csa_679_left
color tv_blue, m_csa_679_right
distance m_csa_679_distance, (m_csa_679 and chain A and resi 54 and resn HIS and name CA), (m_csa_679 and chain A and resi 115 and resn GLN and name CA)
label m_csa_679_distance, "11.709 A"
zoom m_csa_679_left or m_csa_679_right, 8
set dash_width, 3
set label_size, 18
