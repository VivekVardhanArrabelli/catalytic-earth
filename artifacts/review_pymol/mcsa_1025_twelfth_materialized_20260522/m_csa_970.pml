load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_3VMT.cif", m_csa_970
hide everything
show cartoon, m_csa_970
color gray70, m_csa_970
set cartoon_transparency, 0.8, m_csa_970
select m_csa_970_left, m_csa_970 and chain A and resi 94 and resn GLU
select m_csa_970_right, m_csa_970 and chain A and resi 130 and resn GLN
show sticks, m_csa_970_left or m_csa_970_right
color tv_red, m_csa_970_left
color tv_blue, m_csa_970_right
distance m_csa_970_distance, (m_csa_970 and chain A and resi 94 and resn GLU and name CA), (m_csa_970 and chain A and resi 130 and resn GLN and name CA)
label m_csa_970_distance, "11.169 A"
zoom m_csa_970_left or m_csa_970_right, 8
set dash_width, 3
set label_size, 18
