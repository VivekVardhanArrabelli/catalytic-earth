load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_1NWW.cif", m_csa_644
hide everything
show cartoon, m_csa_644
color gray70, m_csa_644
set cartoon_transparency, 0.8, m_csa_644
select m_csa_644_left, m_csa_644 and chain A and resi 53 and resn TYR
select m_csa_644_right, m_csa_644 and chain A and resi 99 and resn ARG
show sticks, m_csa_644_left or m_csa_644_right
color tv_red, m_csa_644_left
color tv_blue, m_csa_644_right
distance m_csa_644_distance, (m_csa_644 and chain A and resi 53 and resn TYR and name CA), (m_csa_644 and chain A and resi 99 and resn ARG and name CA)
label m_csa_644_distance, "17.185 A"
zoom m_csa_644_left or m_csa_644_right, 8
set dash_width, 3
set label_size, 18
