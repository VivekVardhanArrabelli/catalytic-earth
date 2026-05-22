load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_2F61.cif", m_csa_764
hide everything
show cartoon, m_csa_764
color gray70, m_csa_764
set cartoon_transparency, 0.8, m_csa_764
select m_csa_764_left, m_csa_764 and chain B and resi 370 and resn ASN
select m_csa_764_right, m_csa_764 and chain B and resi 235 and resn GLU
show sticks, m_csa_764_left or m_csa_764_right
color tv_red, m_csa_764_left
color tv_blue, m_csa_764_right
distance m_csa_764_distance, (m_csa_764 and chain B and resi 370 and resn ASN and name CA), (m_csa_764 and chain B and resi 235 and resn GLU and name CA)
label m_csa_764_distance, "18.936 A"
zoom m_csa_764_left or m_csa_764_right, 8
set dash_width, 3
set label_size, 18
