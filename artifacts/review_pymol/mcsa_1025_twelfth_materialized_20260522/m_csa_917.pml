load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_1XGM.cif", m_csa_917
hide everything
show cartoon, m_csa_917
color gray70, m_csa_917
set cartoon_transparency, 0.8, m_csa_917
select m_csa_917_left, m_csa_917 and chain A and resi 82 and resn ASP
select m_csa_917_right, m_csa_917 and chain A and resi 161 and resn HIS
show sticks, m_csa_917_left or m_csa_917_right
color tv_red, m_csa_917_left
color tv_blue, m_csa_917_right
distance m_csa_917_distance, (m_csa_917 and chain A and resi 82 and resn ASP and name CA), (m_csa_917 and chain A and resi 161 and resn HIS and name CA)
label m_csa_917_distance, "14.412 A"
zoom m_csa_917_left or m_csa_917_right, 8
set dash_width, 3
set label_size, 18
