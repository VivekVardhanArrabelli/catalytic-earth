load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_206L.cif", m_csa_921
hide everything
show cartoon, m_csa_921
color gray70, m_csa_921
set cartoon_transparency, 0.8, m_csa_921
select m_csa_921_left, m_csa_921 and chain A and resi 20 and resn ASP
select m_csa_921_right, m_csa_921 and chain A and resi 11 and resn GLU
show sticks, m_csa_921_left or m_csa_921_right
color tv_red, m_csa_921_left
color tv_blue, m_csa_921_right
distance m_csa_921_distance, (m_csa_921 and chain A and resi 20 and resn ASP and name CA), (m_csa_921 and chain A and resi 11 and resn GLU and name CA)
label m_csa_921_distance, "9.336 A"
zoom m_csa_921_left or m_csa_921_right, 8
set dash_width, 3
set label_size, 18
