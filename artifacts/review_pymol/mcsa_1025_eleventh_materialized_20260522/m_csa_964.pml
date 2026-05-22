load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_1G2I.cif", m_csa_964
hide everything
show cartoon, m_csa_964
color gray70, m_csa_964
set cartoon_transparency, 0.8, m_csa_964
select m_csa_964_left, m_csa_964 and chain C and resi 74 and resn GLU
select m_csa_964_right, m_csa_964 and chain A and resi 70 and resn GLY
show sticks, m_csa_964_left or m_csa_964_right
color tv_red, m_csa_964_left
color tv_blue, m_csa_964_right
distance m_csa_964_distance, (m_csa_964 and chain C and resi 74 and resn GLU and name CA), (m_csa_964 and chain A and resi 70 and resn GLY and name CA)
label m_csa_964_distance, "12.931 A"
zoom m_csa_964_left or m_csa_964_right, 8
set dash_width, 3
set label_size, 18
