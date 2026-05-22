load "artifacts/v3_mcsa_pymol_twelfth_materialized_coordinates_20260522/pdb_1DKI.cif", m_csa_598
hide everything
show cartoon, m_csa_598
color gray70, m_csa_598
set cartoon_transparency, 0.8, m_csa_598
select m_csa_598_left, m_csa_598 and chain A and resi 330 and resn TRP
select m_csa_598_right, m_csa_598 and chain A and resi 313 and resn HIS
show sticks, m_csa_598_left or m_csa_598_right
color tv_red, m_csa_598_left
color tv_blue, m_csa_598_right
distance m_csa_598_distance, (m_csa_598 and chain A and resi 330 and resn TRP and name CA), (m_csa_598 and chain A and resi 313 and resn HIS and name CA)
label m_csa_598_distance, "9.593 A"
zoom m_csa_598_left or m_csa_598_right, 8
set dash_width, 3
set label_size, 18
