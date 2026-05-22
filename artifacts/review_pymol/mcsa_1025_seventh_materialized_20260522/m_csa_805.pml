load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_1X9Y.cif", m_csa_805
hide everything
show cartoon, m_csa_805
color gray70, m_csa_805
set cartoon_transparency, 0.8, m_csa_805
select m_csa_805_left, m_csa_805 and chain A and resi 203 and resn GLN
select m_csa_805_right, m_csa_805 and chain A and resi 306 and resn HIS
show sticks, m_csa_805_left or m_csa_805_right
color tv_red, m_csa_805_left
color tv_blue, m_csa_805_right
distance m_csa_805_distance, (m_csa_805 and chain A and resi 203 and resn GLN and name CA), (m_csa_805 and chain A and resi 306 and resn HIS and name CA)
label m_csa_805_distance, "11.614 A"
zoom m_csa_805_left or m_csa_805_right, 8
set dash_width, 3
set label_size, 18
