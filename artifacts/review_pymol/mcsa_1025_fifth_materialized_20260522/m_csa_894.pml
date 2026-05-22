load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_1TMO.cif", m_csa_894
hide everything
show cartoon, m_csa_894
color gray70, m_csa_894
set cartoon_transparency, 0.8, m_csa_894
select m_csa_894_left, m_csa_894 and chain A and resi 180 and resn SER
select m_csa_894_right, m_csa_894 and chain A and resi 149 and resn TRP
show sticks, m_csa_894_left or m_csa_894_right
color tv_red, m_csa_894_left
color tv_blue, m_csa_894_right
distance m_csa_894_distance, (m_csa_894 and chain A and resi 180 and resn SER and name CA), (m_csa_894 and chain A and resi 149 and resn TRP and name CA)
label m_csa_894_distance, "11.802 A"
zoom m_csa_894_left or m_csa_894_right, 8
set dash_width, 3
set label_size, 18
