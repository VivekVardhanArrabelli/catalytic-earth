load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_5ODI.cif", m_csa_981
hide everything
show cartoon, m_csa_981
color gray70, m_csa_981
set cartoon_transparency, 0.8, m_csa_981
select m_csa_981_left, m_csa_981 and chain B and resi 193 and resn CYS
select m_csa_981_right, m_csa_981 and chain B and resi 41 and resn CYS
show sticks, m_csa_981_left or m_csa_981_right
color tv_red, m_csa_981_left
color tv_blue, m_csa_981_right
distance m_csa_981_distance, (m_csa_981 and chain B and resi 193 and resn CYS and name CA), (m_csa_981 and chain B and resi 41 and resn CYS and name CA)
label m_csa_981_distance, "22.254 A"
zoom m_csa_981_left or m_csa_981_right, 8
set dash_width, 3
set label_size, 18
