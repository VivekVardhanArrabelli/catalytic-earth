load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_1K4L.cif", m_csa_683
hide everything
show cartoon, m_csa_683
color gray70, m_csa_683
set cartoon_transparency, 0.8, m_csa_683
select m_csa_683_left, m_csa_683 and chain A and resi 37 and resn GLU
select m_csa_683_right, m_csa_683 and chain A and resi 99 and resn ASP
show sticks, m_csa_683_left or m_csa_683_right
color tv_red, m_csa_683_left
color tv_blue, m_csa_683_right
distance m_csa_683_distance, (m_csa_683 and chain A and resi 37 and resn GLU and name CA), (m_csa_683 and chain A and resi 99 and resn ASP and name CA)
label m_csa_683_distance, "27.806 A"
zoom m_csa_683_left or m_csa_683_right, 8
set dash_width, 3
set label_size, 18
