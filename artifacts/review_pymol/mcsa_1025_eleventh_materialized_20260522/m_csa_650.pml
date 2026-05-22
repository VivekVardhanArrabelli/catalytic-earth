load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_1QD6.cif", m_csa_650
hide everything
show cartoon, m_csa_650
color gray70, m_csa_650
set cartoon_transparency, 0.8, m_csa_650
select m_csa_650_left, m_csa_650 and chain C and resi 127 and resn ASN
select m_csa_650_right, m_csa_650 and chain C and resi 118 and resn ARG
show sticks, m_csa_650_left or m_csa_650_right
color tv_red, m_csa_650_left
color tv_blue, m_csa_650_right
distance m_csa_650_distance, (m_csa_650 and chain C and resi 127 and resn ASN and name CA), (m_csa_650 and chain C and resi 118 and resn ARG and name CA)
label m_csa_650_distance, "15.995 A"
zoom m_csa_650_left or m_csa_650_right, 8
set dash_width, 3
set label_size, 18
