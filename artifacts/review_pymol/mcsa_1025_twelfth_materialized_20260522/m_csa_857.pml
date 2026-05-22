load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_1QB4.cif", m_csa_857
hide everything
show cartoon, m_csa_857
color gray70, m_csa_857
set cartoon_transparency, 0.8, m_csa_857
select m_csa_857_left, m_csa_857 and chain A and resi 506 and resn GLU
select m_csa_857_right, m_csa_857 and chain A and resi 138 and resn HIS
show sticks, m_csa_857_left or m_csa_857_right
color tv_red, m_csa_857_left
color tv_blue, m_csa_857_right
distance m_csa_857_distance, (m_csa_857 and chain A and resi 506 and resn GLU and name CA), (m_csa_857 and chain A and resi 138 and resn HIS and name CA)
label m_csa_857_distance, "21.017 A"
zoom m_csa_857_left or m_csa_857_right, 8
set dash_width, 3
set label_size, 18
