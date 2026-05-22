load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_1IMA.cif", m_csa_577
hide everything
show cartoon, m_csa_577
color gray70, m_csa_577
set cartoon_transparency, 0.8, m_csa_577
select m_csa_577_left, m_csa_577 and chain A and resi 70 and resn GLU
select m_csa_577_right, m_csa_577 and chain A and resi 95 and resn THR
show sticks, m_csa_577_left or m_csa_577_right
color tv_red, m_csa_577_left
color tv_blue, m_csa_577_right
distance m_csa_577_distance, (m_csa_577 and chain A and resi 70 and resn GLU and name CA), (m_csa_577 and chain A and resi 95 and resn THR and name CA)
label m_csa_577_distance, "11.644 A"
zoom m_csa_577_left or m_csa_577_right, 8
set dash_width, 3
set label_size, 18
