load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_2NMT.cif", m_csa_928
hide everything
show cartoon, m_csa_928
color gray70, m_csa_928
set cartoon_transparency, 0.8, m_csa_928
select m_csa_928_left, m_csa_928 and chain A and resi 422 and resn LEU
select m_csa_928_right, m_csa_928 and chain A and resi 138 and resn LEU
show sticks, m_csa_928_left or m_csa_928_right
color tv_red, m_csa_928_left
color tv_blue, m_csa_928_right
distance m_csa_928_distance, (m_csa_928 and chain A and resi 422 and resn LEU and name CA), (m_csa_928 and chain A and resi 138 and resn LEU and name CA)
label m_csa_928_distance, "12.802 A"
zoom m_csa_928_left or m_csa_928_right, 8
set dash_width, 3
set label_size, 18
