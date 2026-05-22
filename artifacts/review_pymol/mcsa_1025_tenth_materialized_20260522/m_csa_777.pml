load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_1AAM.cif", m_csa_777
hide everything
show cartoon, m_csa_777
color gray70, m_csa_777
set cartoon_transparency, 0.8, m_csa_777
select m_csa_777_left, m_csa_777 and chain A and resi 211 and resn ASP
select m_csa_777_right, m_csa_777 and chain A and resi 130 and resn TRP
show sticks, m_csa_777_left or m_csa_777_right
color tv_red, m_csa_777_left
color tv_blue, m_csa_777_right
distance m_csa_777_distance, (m_csa_777 and chain A and resi 211 and resn ASP and name CA), (m_csa_777 and chain A and resi 130 and resn TRP and name CA)
label m_csa_777_distance, "9.998 A"
zoom m_csa_777_left or m_csa_777_right, 8
set dash_width, 3
set label_size, 18
