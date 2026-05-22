load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_1PSD.cif", m_csa_785
hide everything
show cartoon, m_csa_785
color gray70, m_csa_785
set cartoon_transparency, 0.8, m_csa_785
select m_csa_785_left, m_csa_785 and chain A and resi 291 and resn HIS
select m_csa_785_right, m_csa_785 and chain A and resi 268 and resn GLU
show sticks, m_csa_785_left or m_csa_785_right
color tv_red, m_csa_785_left
color tv_blue, m_csa_785_right
distance m_csa_785_distance, (m_csa_785 and chain A and resi 291 and resn HIS and name CA), (m_csa_785 and chain A and resi 268 and resn GLU and name CA)
label m_csa_785_distance, "8.451 A"
zoom m_csa_785_left or m_csa_785_right, 8
set dash_width, 3
set label_size, 18
