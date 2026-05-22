load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_1VQ1.cif", m_csa_703
hide everything
show cartoon, m_csa_703
color gray70, m_csa_703
set cartoon_transparency, 0.8, m_csa_703
select m_csa_703_left, m_csa_703 and chain A and resi 112 and resn PHE
select m_csa_703_right, m_csa_703 and chain A and resi 210 and resn PRO
show sticks, m_csa_703_left or m_csa_703_right
color tv_red, m_csa_703_left
color tv_blue, m_csa_703_right
distance m_csa_703_distance, (m_csa_703 and chain A and resi 112 and resn PHE and name CA), (m_csa_703 and chain A and resi 210 and resn PRO and name CA)
label m_csa_703_distance, "10.693 A"
zoom m_csa_703_left or m_csa_703_right, 8
set dash_width, 3
set label_size, 18
