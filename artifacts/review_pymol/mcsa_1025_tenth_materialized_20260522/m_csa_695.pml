load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_2BSX.cif", m_csa_695
hide everything
show cartoon, m_csa_695
color gray70, m_csa_695
set cartoon_transparency, 0.8, m_csa_695
select m_csa_695_left, m_csa_695 and chain A and resi 206 and resn ASP
select m_csa_695_right, m_csa_695 and chain A and resi 45 and resn ARG
show sticks, m_csa_695_left or m_csa_695_right
color tv_red, m_csa_695_left
color tv_blue, m_csa_695_right
distance m_csa_695_distance, (m_csa_695 and chain A and resi 206 and resn ASP and name CA), (m_csa_695 and chain A and resi 45 and resn ARG and name CA)
label m_csa_695_distance, "24.796 A"
zoom m_csa_695_left or m_csa_695_right, 8
set dash_width, 3
set label_size, 18
