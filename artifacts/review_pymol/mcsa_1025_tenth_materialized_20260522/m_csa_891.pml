load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_1YBV.cif", m_csa_891
hide everything
show cartoon, m_csa_891
color gray70, m_csa_891
set cartoon_transparency, 0.8, m_csa_891
select m_csa_891_left, m_csa_891 and chain A and resi 223 and resn TYR
select m_csa_891_right, m_csa_891 and chain A and resi 182 and resn LYS
show sticks, m_csa_891_left or m_csa_891_right
color tv_red, m_csa_891_left
color tv_blue, m_csa_891_right
distance m_csa_891_distance, (m_csa_891 and chain A and resi 223 and resn TYR and name CA), (m_csa_891 and chain A and resi 182 and resn LYS and name CA)
label m_csa_891_distance, "16.275 A"
zoom m_csa_891_left or m_csa_891_right, 8
set dash_width, 3
set label_size, 18
