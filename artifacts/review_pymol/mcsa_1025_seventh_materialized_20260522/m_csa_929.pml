load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_2OAT.cif", m_csa_929
hide everything
show cartoon, m_csa_929
color gray70, m_csa_929
set cartoon_transparency, 0.8, m_csa_929
select m_csa_929_left, m_csa_929 and chain A and resi 177 and resn PHE
select m_csa_929_right, m_csa_929 and chain A and resi 292 and resn LYS
show sticks, m_csa_929_left or m_csa_929_right
color tv_red, m_csa_929_left
color tv_blue, m_csa_929_right
distance m_csa_929_distance, (m_csa_929 and chain A and resi 177 and resn PHE and name CA), (m_csa_929 and chain A and resi 292 and resn LYS and name CA)
label m_csa_929_distance, "14.202 A"
zoom m_csa_929_left or m_csa_929_right, 8
set dash_width, 3
set label_size, 18
