load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_1L1R.cif", m_csa_802
hide everything
show cartoon, m_csa_802
color gray70, m_csa_802
set cartoon_transparency, 0.8, m_csa_802
select m_csa_802_left, m_csa_802 and chain A and resi 63 and resn ARG
select m_csa_802_right, m_csa_802 and chain A and resi 100 and resn GLU
show sticks, m_csa_802_left or m_csa_802_right
color tv_red, m_csa_802_left
color tv_blue, m_csa_802_right
distance m_csa_802_distance, (m_csa_802 and chain A and resi 63 and resn ARG and name CA), (m_csa_802 and chain A and resi 100 and resn GLU and name CA)
label m_csa_802_distance, "14.982 A"
zoom m_csa_802_left or m_csa_802_right, 8
set dash_width, 3
set label_size, 18
