load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_1W27.cif", m_csa_708
hide everything
show cartoon, m_csa_708
color gray70, m_csa_708
set cartoon_transparency, 0.8, m_csa_708
select m_csa_708_left, m_csa_708 and chain A and resi 110 and resn TYR
select m_csa_708_right, m_csa_708 and chain A and resi 349 and resn ASP
show sticks, m_csa_708_left or m_csa_708_right
color tv_red, m_csa_708_left
color tv_blue, m_csa_708_right
distance m_csa_708_distance, (m_csa_708 and chain A and resi 110 and resn TYR and name CA), (m_csa_708 and chain A and resi 349 and resn ASP and name CA)
label m_csa_708_distance, "74.887 A"
zoom m_csa_708_left or m_csa_708_right, 8
set dash_width, 3
set label_size, 18
