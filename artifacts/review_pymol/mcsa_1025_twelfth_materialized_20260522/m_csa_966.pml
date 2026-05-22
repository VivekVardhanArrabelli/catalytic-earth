load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_4X9E.cif", m_csa_966
hide everything
show cartoon, m_csa_966
color gray70, m_csa_966
set cartoon_transparency, 0.8, m_csa_966
select m_csa_966_left, m_csa_966 and chain A and resi 117 and resn HIS
select m_csa_966_right, m_csa_966 and chain B and resi 442 and resn ARG
show sticks, m_csa_966_left or m_csa_966_right
color tv_red, m_csa_966_left
color tv_blue, m_csa_966_right
distance m_csa_966_distance, (m_csa_966 and chain A and resi 117 and resn HIS and name CA), (m_csa_966 and chain B and resi 442 and resn ARG and name CA)
label m_csa_966_distance, "44.775 A"
zoom m_csa_966_left or m_csa_966_right, 8
set dash_width, 3
set label_size, 18
