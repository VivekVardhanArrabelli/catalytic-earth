load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_1O9I.cif", m_csa_572
hide everything
show cartoon, m_csa_572
color gray70, m_csa_572
set cartoon_transparency, 0.8, m_csa_572
select m_csa_572_left, m_csa_572 and chain A and resi 69 and resn HIS
select m_csa_572_right, m_csa_572 and chain A and resi 181 and resn HIS
show sticks, m_csa_572_left or m_csa_572_right
color tv_red, m_csa_572_left
color tv_blue, m_csa_572_right
distance m_csa_572_distance, (m_csa_572 and chain A and resi 69 and resn HIS and name CA), (m_csa_572 and chain A and resi 181 and resn HIS and name CA)
label m_csa_572_distance, "12.931 A"
zoom m_csa_572_left or m_csa_572_right, 8
set dash_width, 3
set label_size, 18
