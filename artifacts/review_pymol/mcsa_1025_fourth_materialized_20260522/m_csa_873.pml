load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_1ORO.cif", m_csa_873
hide everything
show cartoon, m_csa_873
color gray70, m_csa_873
set cartoon_transparency, 0.8, m_csa_873
select m_csa_873_left, m_csa_873 and chain A and resi 105 and resn HIS
select m_csa_873_right, m_csa_873 and chain A and resi 103 and resn LYS
show sticks, m_csa_873_left or m_csa_873_right
color tv_red, m_csa_873_left
color tv_blue, m_csa_873_right
distance m_csa_873_distance, (m_csa_873 and chain A and resi 105 and resn HIS and name CA), (m_csa_873 and chain A and resi 103 and resn LYS and name CA)
label m_csa_873_distance, "5.618 A"
zoom m_csa_873_left or m_csa_873_right, 8
set dash_width, 3
set label_size, 18
