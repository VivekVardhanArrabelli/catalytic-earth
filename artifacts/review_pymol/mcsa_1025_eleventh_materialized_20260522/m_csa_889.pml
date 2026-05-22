load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_2PGD.cif", m_csa_889
hide everything
show cartoon, m_csa_889
color gray70, m_csa_889
set cartoon_transparency, 0.8, m_csa_889
select m_csa_889_left, m_csa_889 and chain A and resi 128 and resn SER
select m_csa_889_right, m_csa_889 and chain A and resi 190 and resn GLU
show sticks, m_csa_889_left or m_csa_889_right
color tv_red, m_csa_889_left
color tv_blue, m_csa_889_right
distance m_csa_889_distance, (m_csa_889 and chain A and resi 128 and resn SER and name CA), (m_csa_889 and chain A and resi 190 and resn GLU and name CA)
label m_csa_889_distance, "11.269 A"
zoom m_csa_889_left or m_csa_889_right, 8
set dash_width, 3
set label_size, 18
