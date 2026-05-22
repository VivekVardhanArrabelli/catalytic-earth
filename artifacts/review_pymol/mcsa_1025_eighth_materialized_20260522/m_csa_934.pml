load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_3CLA.cif", m_csa_934
hide everything
show cartoon, m_csa_934
color gray70, m_csa_934
set cartoon_transparency, 0.8, m_csa_934
select m_csa_934_left, m_csa_934 and chain A and resi 13 and resn ARG
select m_csa_934_right, m_csa_934 and chain A and resi 168 and resn THR
show sticks, m_csa_934_left or m_csa_934_right
color tv_red, m_csa_934_left
color tv_blue, m_csa_934_right
distance m_csa_934_distance, (m_csa_934 and chain A and resi 13 and resn ARG and name CA), (m_csa_934 and chain A and resi 168 and resn THR and name CA)
label m_csa_934_distance, "26.958 A"
zoom m_csa_934_left or m_csa_934_right, 8
set dash_width, 3
set label_size, 18
