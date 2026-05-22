load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_1PD2.cif", m_csa_719
hide everything
show cartoon, m_csa_719
color gray70, m_csa_719
set cartoon_transparency, 0.8, m_csa_719
select m_csa_719_left, m_csa_719 and chain 1 and resi 8 and resn TYR
select m_csa_719_right, m_csa_719 and chain 1 and resi 104 and resn TRP
show sticks, m_csa_719_left or m_csa_719_right
color tv_red, m_csa_719_left
color tv_blue, m_csa_719_right
distance m_csa_719_distance, (m_csa_719 and chain 1 and resi 8 and resn TYR and name CA), (m_csa_719 and chain 1 and resi 104 and resn TRP and name CA)
label m_csa_719_distance, "15.939 A"
zoom m_csa_719_left or m_csa_719_right, 8
set dash_width, 3
set label_size, 18
