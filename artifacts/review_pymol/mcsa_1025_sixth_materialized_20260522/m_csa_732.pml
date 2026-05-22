load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_1XS1.cif", m_csa_732
hide everything
show cartoon, m_csa_732
color gray70, m_csa_732
set cartoon_transparency, 0.8, m_csa_732
select m_csa_732_left, m_csa_732 and chain A and resi 126 and resn ARG
select m_csa_732_right, m_csa_732 and chain C and resi 115 and resn ARG
show sticks, m_csa_732_left or m_csa_732_right
color tv_red, m_csa_732_left
color tv_blue, m_csa_732_right
distance m_csa_732_distance, (m_csa_732 and chain A and resi 126 and resn ARG and name CA), (m_csa_732 and chain C and resi 115 and resn ARG and name CA)
label m_csa_732_distance, "13.724 A"
zoom m_csa_732_left or m_csa_732_right, 8
set dash_width, 3
set label_size, 18
