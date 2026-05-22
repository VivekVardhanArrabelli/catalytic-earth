load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_1EU1.cif", m_csa_701
hide everything
show cartoon, m_csa_701
color gray70, m_csa_701
set cartoon_transparency, 0.8, m_csa_701
select m_csa_701_left, m_csa_701 and chain A and resi 114 and resn TYR
select m_csa_701_right, m_csa_701 and chain A and resi 116 and resn TRP
show sticks, m_csa_701_left or m_csa_701_right
color tv_red, m_csa_701_left
color tv_blue, m_csa_701_right
distance m_csa_701_distance, (m_csa_701 and chain A and resi 114 and resn TYR and name CA), (m_csa_701 and chain A and resi 116 and resn TRP and name CA)
label m_csa_701_distance, "7.386 A"
zoom m_csa_701_left or m_csa_701_right, 8
set dash_width, 3
set label_size, 18
