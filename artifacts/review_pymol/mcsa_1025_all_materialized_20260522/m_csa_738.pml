load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_1O98.cif", m_csa_738
hide everything
show cartoon, m_csa_738
color gray70, m_csa_738
set cartoon_transparency, 0.8, m_csa_738
select m_csa_738_left, m_csa_738 and chain A and resi 261 and resn ARG
select m_csa_738_right, m_csa_738 and chain A and resi 407 and resn HIS
show sticks, m_csa_738_left or m_csa_738_right
color tv_red, m_csa_738_left
color tv_blue, m_csa_738_right
distance m_csa_738_distance, (m_csa_738 and chain A and resi 261 and resn ARG and name CA), (m_csa_738 and chain A and resi 407 and resn HIS and name CA)
label m_csa_738_distance, "17.955 A"
zoom m_csa_738_left or m_csa_738_right, 8
set dash_width, 3
set label_size, 18
