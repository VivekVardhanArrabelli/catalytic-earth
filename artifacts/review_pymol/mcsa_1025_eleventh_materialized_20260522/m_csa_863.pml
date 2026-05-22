load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_1NHX.cif", m_csa_863
hide everything
show cartoon, m_csa_863
color gray70, m_csa_863
set cartoon_transparency, 0.8, m_csa_863
select m_csa_863_left, m_csa_863 and chain A and resi 238 and resn TYR
select m_csa_863_right, m_csa_863 and chain A and resi 291 and resn CYS
show sticks, m_csa_863_left or m_csa_863_right
color tv_red, m_csa_863_left
color tv_blue, m_csa_863_right
distance m_csa_863_distance, (m_csa_863 and chain A and resi 238 and resn TYR and name CA), (m_csa_863 and chain A and resi 291 and resn CYS and name CA)
label m_csa_863_distance, "21.633 A"
zoom m_csa_863_left or m_csa_863_right, 8
set dash_width, 3
set label_size, 18
