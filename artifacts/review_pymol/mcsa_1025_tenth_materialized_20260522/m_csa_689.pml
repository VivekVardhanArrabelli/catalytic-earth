load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_1R6W.cif", m_csa_689
hide everything
show cartoon, m_csa_689
color gray70, m_csa_689
set cartoon_transparency, 0.8, m_csa_689
select m_csa_689_left, m_csa_689 and chain A and resi 135 and resn ARG
select m_csa_689_right, m_csa_689 and chain A and resi 237 and resn LYS
show sticks, m_csa_689_left or m_csa_689_right
color tv_red, m_csa_689_left
color tv_blue, m_csa_689_right
distance m_csa_689_distance, (m_csa_689 and chain A and resi 135 and resn ARG and name CA), (m_csa_689 and chain A and resi 237 and resn LYS and name CA)
label m_csa_689_distance, "17.056 A"
zoom m_csa_689_left or m_csa_689_right, 8
set dash_width, 3
set label_size, 18
