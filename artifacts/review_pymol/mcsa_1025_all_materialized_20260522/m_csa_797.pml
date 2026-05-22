load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_1RBA.cif", m_csa_797
hide everything
show cartoon, m_csa_797
color gray70, m_csa_797
set cartoon_transparency, 0.8, m_csa_797
select m_csa_797_left, m_csa_797 and chain A and resi 321 and resn HIS
select m_csa_797_right, m_csa_797 and chain A and resi 166 and resn LYS
show sticks, m_csa_797_left or m_csa_797_right
color tv_red, m_csa_797_left
color tv_blue, m_csa_797_right
distance m_csa_797_distance, (m_csa_797 and chain A and resi 321 and resn HIS and name CA), (m_csa_797 and chain A and resi 166 and resn LYS and name CA)
label m_csa_797_distance, "18.008 A"
zoom m_csa_797_left or m_csa_797_right, 8
set dash_width, 3
set label_size, 18
