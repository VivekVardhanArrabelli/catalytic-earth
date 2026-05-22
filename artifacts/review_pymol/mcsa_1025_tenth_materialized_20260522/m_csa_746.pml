load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_1QOL.cif", m_csa_746
hide everything
show cartoon, m_csa_746
color gray70, m_csa_746
set cartoon_transparency, 0.8, m_csa_746
select m_csa_746_left, m_csa_746 and chain B and resi 18 and resn ASN
select m_csa_746_right, m_csa_746 and chain B and resi 120 and resn HIS
show sticks, m_csa_746_left or m_csa_746_right
color tv_red, m_csa_746_left
color tv_blue, m_csa_746_right
distance m_csa_746_distance, (m_csa_746 and chain B and resi 18 and resn ASN and name CA), (m_csa_746 and chain B and resi 120 and resn HIS and name CA)
label m_csa_746_distance, "11.452 A"
zoom m_csa_746_left or m_csa_746_right, 8
set dash_width, 3
set label_size, 18
