load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_1OTG.cif", m_csa_874
hide everything
show cartoon, m_csa_874
color gray70, m_csa_874
set cartoon_transparency, 0.8, m_csa_874
select m_csa_874_left, m_csa_874 and chain A and resi 71 and resn ARG
select m_csa_874_right, m_csa_874 and chain A and resi 40 and resn ARG
show sticks, m_csa_874_left or m_csa_874_right
color tv_red, m_csa_874_left
color tv_blue, m_csa_874_right
distance m_csa_874_distance, (m_csa_874 and chain A and resi 71 and resn ARG and name CA), (m_csa_874 and chain A and resi 40 and resn ARG and name CA)
label m_csa_874_distance, "18.263 A"
zoom m_csa_874_left or m_csa_874_right, 8
set dash_width, 3
set label_size, 18
