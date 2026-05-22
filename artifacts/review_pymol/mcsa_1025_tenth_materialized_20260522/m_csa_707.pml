load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_1MT1.cif", m_csa_707
hide everything
show cartoon, m_csa_707
color gray70, m_csa_707
set cartoon_transparency, 0.8, m_csa_707
select m_csa_707_left, m_csa_707 and chain A and resi 47 and resn ASN
select m_csa_707_right, m_csa_707 and chain F and resi 57 and resn GLU
show sticks, m_csa_707_left or m_csa_707_right
color tv_red, m_csa_707_left
color tv_blue, m_csa_707_right
distance m_csa_707_distance, (m_csa_707 and chain A and resi 47 and resn ASN and name CA), (m_csa_707 and chain F and resi 57 and resn GLU and name CA)
label m_csa_707_distance, "14.129 A"
zoom m_csa_707_left or m_csa_707_right, 8
set dash_width, 3
set label_size, 18
