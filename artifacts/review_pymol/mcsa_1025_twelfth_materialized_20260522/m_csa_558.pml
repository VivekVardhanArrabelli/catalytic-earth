load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_1D2T.cif", m_csa_558
hide everything
show cartoon, m_csa_558
color gray70, m_csa_558
set cartoon_transparency, 0.8, m_csa_558
select m_csa_558_left, m_csa_558 and chain A and resi 150 and resn HIS
select m_csa_558_right, m_csa_558 and chain A and resi 193 and resn ASP
show sticks, m_csa_558_left or m_csa_558_right
color tv_red, m_csa_558_left
color tv_blue, m_csa_558_right
distance m_csa_558_distance, (m_csa_558 and chain A and resi 150 and resn HIS and name CA), (m_csa_558 and chain A and resi 193 and resn ASP and name CA)
label m_csa_558_distance, "10.252 A"
zoom m_csa_558_left or m_csa_558_right, 8
set dash_width, 3
set label_size, 18
