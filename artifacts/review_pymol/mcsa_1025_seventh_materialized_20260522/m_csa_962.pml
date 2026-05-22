load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_3D47.cif", m_csa_962
hide everything
show cartoon, m_csa_962
color gray70, m_csa_962
set cartoon_transparency, 0.8, m_csa_962
select m_csa_962_left, m_csa_962 and chain A and resi 226 and resn ASP
select m_csa_962_right, m_csa_962 and chain A and resi 302 and resn ASP
show sticks, m_csa_962_left or m_csa_962_right
color tv_red, m_csa_962_left
color tv_blue, m_csa_962_right
distance m_csa_962_distance, (m_csa_962 and chain A and resi 226 and resn ASP and name CA), (m_csa_962 and chain A and resi 302 and resn ASP and name CA)
label m_csa_962_distance, "14.700 A"
zoom m_csa_962_left or m_csa_962_right, 8
set dash_width, 3
set label_size, 18
