load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_2F9Z.cif", m_csa_729
hide everything
show cartoon, m_csa_729
color gray70, m_csa_729
set cartoon_transparency, 0.8, m_csa_729
select m_csa_729_left, m_csa_729 and chain C and resi 29 and resn CYS
select m_csa_729_right, m_csa_729 and chain C and resi 23 and resn THR
show sticks, m_csa_729_left or m_csa_729_right
color tv_red, m_csa_729_left
color tv_blue, m_csa_729_right
distance m_csa_729_distance, (m_csa_729 and chain C and resi 29 and resn CYS and name CA), (m_csa_729 and chain C and resi 23 and resn THR and name CA)
label m_csa_729_distance, "10.603 A"
zoom m_csa_729_left or m_csa_729_right, 8
set dash_width, 3
set label_size, 18
