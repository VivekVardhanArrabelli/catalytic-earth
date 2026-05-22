load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_1NBF.cif", m_csa_789
hide everything
show cartoon, m_csa_789
color gray70, m_csa_789
set cartoon_transparency, 0.8, m_csa_789
select m_csa_789_left, m_csa_789 and chain A and resi 11 and resn ASN
select m_csa_789_right, m_csa_789 and chain A and resi 257 and resn HIS
show sticks, m_csa_789_left or m_csa_789_right
color tv_red, m_csa_789_left
color tv_blue, m_csa_789_right
distance m_csa_789_distance, (m_csa_789 and chain A and resi 11 and resn ASN and name CA), (m_csa_789 and chain A and resi 257 and resn HIS and name CA)
label m_csa_789_distance, "11.166 A"
zoom m_csa_789_left or m_csa_789_right, 8
set dash_width, 3
set label_size, 18
