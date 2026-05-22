load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_4NJK.cif", m_csa_943
hide everything
show cartoon, m_csa_943
color gray70, m_csa_943
set cartoon_transparency, 0.8, m_csa_943
select m_csa_943_left, m_csa_943 and chain A and resi 51 and resn CYS
select m_csa_943_right, m_csa_943 and chain A and resi 224 and resn HIS
show sticks, m_csa_943_left or m_csa_943_right
color tv_red, m_csa_943_left
color tv_blue, m_csa_943_right
distance m_csa_943_distance, (m_csa_943 and chain A and resi 51 and resn CYS and name CA), (m_csa_943 and chain A and resi 224 and resn HIS and name CA)
label m_csa_943_distance, "22.193 A"
zoom m_csa_943_left or m_csa_943_right, 8
set dash_width, 3
set label_size, 18
