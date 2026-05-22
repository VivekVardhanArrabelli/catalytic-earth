load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_2E2H.cif", m_csa_788
hide everything
show cartoon, m_csa_788
color gray70, m_csa_788
set cartoon_transparency, 0.8, m_csa_788
select m_csa_788_left, m_csa_788 and chain A and resi 1085 and resn HIS
select m_csa_788_right, m_csa_788 and chain A and resi 485 and resn ASP
show sticks, m_csa_788_left or m_csa_788_right
color tv_red, m_csa_788_left
color tv_blue, m_csa_788_right
distance m_csa_788_distance, (m_csa_788 and chain A and resi 1085 and resn HIS and name CA), (m_csa_788 and chain A and resi 485 and resn ASP and name CA)
label m_csa_788_distance, "17.460 A"
zoom m_csa_788_left or m_csa_788_right, 8
set dash_width, 3
set label_size, 18
