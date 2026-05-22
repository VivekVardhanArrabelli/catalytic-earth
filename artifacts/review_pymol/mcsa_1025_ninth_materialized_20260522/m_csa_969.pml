load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_4DGK.cif", m_csa_969
hide everything
show cartoon, m_csa_969
color gray70, m_csa_969
set cartoon_transparency, 0.8, m_csa_969
select m_csa_969_left, m_csa_969 and chain A and resi 152 and resn ARG
select m_csa_969_right, m_csa_969 and chain A and resi 31 and resn GLU
show sticks, m_csa_969_left or m_csa_969_right
color tv_red, m_csa_969_left
color tv_blue, m_csa_969_right
distance m_csa_969_distance, (m_csa_969 and chain A and resi 152 and resn ARG and name CA), (m_csa_969 and chain A and resi 31 and resn GLU and name CA)
label m_csa_969_distance, "28.855 A"
zoom m_csa_969_left or m_csa_969_right, 8
set dash_width, 3
set label_size, 18
