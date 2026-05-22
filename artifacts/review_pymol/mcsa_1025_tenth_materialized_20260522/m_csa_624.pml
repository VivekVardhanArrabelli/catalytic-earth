load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_1GCB.cif", m_csa_624
hide everything
show cartoon, m_csa_624
color gray70, m_csa_624
set cartoon_transparency, 0.8, m_csa_624
select m_csa_624_left, m_csa_624 and chain A and resi 67 and resn GLN
select m_csa_624_right, m_csa_624 and chain A and resi 369 and resn HIS
show sticks, m_csa_624_left or m_csa_624_right
color tv_red, m_csa_624_left
color tv_blue, m_csa_624_right
distance m_csa_624_distance, (m_csa_624 and chain A and resi 67 and resn GLN and name CA), (m_csa_624 and chain A and resi 369 and resn HIS and name CA)
label m_csa_624_distance, "11.700 A"
zoom m_csa_624_left or m_csa_624_right, 8
set dash_width, 3
set label_size, 18
