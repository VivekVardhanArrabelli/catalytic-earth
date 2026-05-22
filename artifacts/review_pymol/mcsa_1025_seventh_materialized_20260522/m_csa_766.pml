load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_1S3I.cif", m_csa_766
hide everything
show cartoon, m_csa_766
color gray70, m_csa_766
set cartoon_transparency, 0.8, m_csa_766
select m_csa_766_left, m_csa_766 and chain A and resi 106 and resn HIS
select m_csa_766_right, m_csa_766 and chain A and resi 142 and resn ASP
show sticks, m_csa_766_left or m_csa_766_right
color tv_red, m_csa_766_left
color tv_blue, m_csa_766_right
distance m_csa_766_distance, (m_csa_766 and chain A and resi 106 and resn HIS and name CA), (m_csa_766 and chain A and resi 142 and resn ASP and name CA)
label m_csa_766_distance, "8.024 A"
zoom m_csa_766_left or m_csa_766_right, 8
set dash_width, 3
set label_size, 18
