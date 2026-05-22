load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_5G0I.cif", m_csa_998
hide everything
show cartoon, m_csa_998
color gray70, m_csa_998
set cartoon_transparency, 0.8, m_csa_998
select m_csa_998_left, m_csa_998 and chain A and resi 341 and resn TYR
select m_csa_998_right, m_csa_998 and chain A and resi 206 and resn ASP
show sticks, m_csa_998_left or m_csa_998_right
color tv_red, m_csa_998_left
color tv_blue, m_csa_998_right
distance m_csa_998_distance, (m_csa_998 and chain A and resi 341 and resn TYR and name CA), (m_csa_998 and chain A and resi 206 and resn ASP and name CA)
label m_csa_998_distance, "16.492 A"
zoom m_csa_998_left or m_csa_998_right, 8
set dash_width, 3
set label_size, 18
