load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_3UFJ.cif", m_csa_834
hide everything
show cartoon, m_csa_834
color gray70, m_csa_834
set cartoon_transparency, 0.8, m_csa_834
select m_csa_834_left, m_csa_834 and chain A and resi 36 and resn ASN
select m_csa_834_right, m_csa_834 and chain A and resi 47 and resn HIS
show sticks, m_csa_834_left or m_csa_834_right
color tv_red, m_csa_834_left
color tv_blue, m_csa_834_right
distance m_csa_834_distance, (m_csa_834 and chain A and resi 36 and resn ASN and name CA), (m_csa_834 and chain A and resi 47 and resn HIS and name CA)
label m_csa_834_distance, "10.153 A"
zoom m_csa_834_left or m_csa_834_right, 8
set dash_width, 3
set label_size, 18
