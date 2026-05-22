load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_1FWK.cif", m_csa_778
hide everything
show cartoon, m_csa_778
color gray70, m_csa_778
set cartoon_transparency, 0.8, m_csa_778
select m_csa_778_left, m_csa_778 and chain C and resi 179 and resn THR
select m_csa_778_right, m_csa_778 and chain C and resi 126 and resn GLU
show sticks, m_csa_778_left or m_csa_778_right
color tv_red, m_csa_778_left
color tv_blue, m_csa_778_right
distance m_csa_778_distance, (m_csa_778 and chain C and resi 179 and resn THR and name CA), (m_csa_778 and chain C and resi 126 and resn GLU and name CA)
label m_csa_778_distance, "10.841 A"
zoom m_csa_778_left or m_csa_778_right, 8
set dash_width, 3
set label_size, 18
