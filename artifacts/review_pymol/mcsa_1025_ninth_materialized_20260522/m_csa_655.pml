load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_1P7M.cif", m_csa_655
hide everything
show cartoon, m_csa_655
color gray70, m_csa_655
set cartoon_transparency, 0.8, m_csa_655
select m_csa_655_left, m_csa_655 and chain A and resi 16 and resn TYR
select m_csa_655_right, m_csa_655 and chain A and resi 38 and resn GLU
show sticks, m_csa_655_left or m_csa_655_right
color tv_red, m_csa_655_left
color tv_blue, m_csa_655_right
distance m_csa_655_distance, (m_csa_655 and chain A and resi 16 and resn TYR and name CA), (m_csa_655 and chain A and resi 38 and resn GLU and name CA)
label m_csa_655_distance, "13.393 A"
zoom m_csa_655_left or m_csa_655_right, 8
set dash_width, 3
set label_size, 18
