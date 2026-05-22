load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_1C4T.cif", m_csa_704
hide everything
show cartoon, m_csa_704
color gray70, m_csa_704
set cartoon_transparency, 0.8, m_csa_704
select m_csa_704_left, m_csa_704 and chain C and resi 152 and resn THR
select m_csa_704_right, m_csa_704 and chain A and resi 204 and resn HIS
show sticks, m_csa_704_left or m_csa_704_right
color tv_red, m_csa_704_left
color tv_blue, m_csa_704_right
distance m_csa_704_distance, (m_csa_704 and chain C and resi 152 and resn THR and name CA), (m_csa_704 and chain A and resi 204 and resn HIS and name CA)
label m_csa_704_distance, "15.166 A"
zoom m_csa_704_left or m_csa_704_right, 8
set dash_width, 3
set label_size, 18
