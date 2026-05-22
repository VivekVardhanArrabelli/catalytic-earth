load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_1KDG.cif", m_csa_673
hide everything
show cartoon, m_csa_673
color gray70, m_csa_673
set cartoon_transparency, 0.8, m_csa_673
select m_csa_673_left, m_csa_673 and chain A and resi 480 and resn HIS
select m_csa_673_right, m_csa_673 and chain A and resi 400 and resn TYR
show sticks, m_csa_673_left or m_csa_673_right
color tv_red, m_csa_673_left
color tv_blue, m_csa_673_right
distance m_csa_673_distance, (m_csa_673 and chain A and resi 480 and resn HIS and name CA), (m_csa_673 and chain A and resi 400 and resn TYR and name CA)
label m_csa_673_distance, "11.125 A"
zoom m_csa_673_left or m_csa_673_right, 8
set dash_width, 3
set label_size, 18
