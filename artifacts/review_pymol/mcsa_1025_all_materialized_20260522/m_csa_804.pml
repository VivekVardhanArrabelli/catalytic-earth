load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_1GPJ.cif", m_csa_804
hide everything
show cartoon, m_csa_804
color gray70, m_csa_804
set cartoon_transparency, 0.8, m_csa_804
select m_csa_804_left, m_csa_804 and chain A and resi 48 and resn SER
select m_csa_804_right, m_csa_804 and chain A and resi 84 and resn HIS
show sticks, m_csa_804_left or m_csa_804_right
color tv_red, m_csa_804_left
color tv_blue, m_csa_804_right
distance m_csa_804_distance, (m_csa_804 and chain A and resi 48 and resn SER and name CA), (m_csa_804 and chain A and resi 84 and resn HIS and name CA)
label m_csa_804_distance, "17.423 A"
zoom m_csa_804_left or m_csa_804_right, 8
set dash_width, 3
set label_size, 18
