load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_1EI5.cif", m_csa_782
hide everything
show cartoon, m_csa_782
color gray70, m_csa_782
set cartoon_transparency, 0.8, m_csa_782
select m_csa_782_left, m_csa_782 and chain A and resi 155 and resn ASN
select m_csa_782_right, m_csa_782 and chain A and resi 287 and resn HIS
show sticks, m_csa_782_left or m_csa_782_right
color tv_red, m_csa_782_left
color tv_blue, m_csa_782_right
distance m_csa_782_distance, (m_csa_782 and chain A and resi 155 and resn ASN and name CA), (m_csa_782 and chain A and resi 287 and resn HIS and name CA)
label m_csa_782_distance, "13.300 A"
zoom m_csa_782_left or m_csa_782_right, 8
set dash_width, 3
set label_size, 18
