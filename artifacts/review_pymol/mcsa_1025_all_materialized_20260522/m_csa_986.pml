load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_4V2K.cif", m_csa_986
hide everything
show cartoon, m_csa_986
color gray70, m_csa_986
set cartoon_transparency, 0.8, m_csa_986
select m_csa_986_left, m_csa_986 and chain A and resi 100 and resn SER
select m_csa_986_right, m_csa_986 and chain A and resi 82 and resn ARG
show sticks, m_csa_986_left or m_csa_986_right
color tv_red, m_csa_986_left
color tv_blue, m_csa_986_right
distance m_csa_986_distance, (m_csa_986 and chain A and resi 100 and resn SER and name CA), (m_csa_986 and chain A and resi 82 and resn ARG and name CA)
label m_csa_986_distance, "14.828 A"
zoom m_csa_986_left or m_csa_986_right, 8
set dash_width, 3
set label_size, 18
