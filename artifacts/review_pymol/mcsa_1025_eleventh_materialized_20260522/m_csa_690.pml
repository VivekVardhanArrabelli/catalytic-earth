load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_1OGO.cif", m_csa_690
hide everything
show cartoon, m_csa_690
color gray70, m_csa_690
set cartoon_transparency, 0.8, m_csa_690
select m_csa_690_left, m_csa_690 and chain X and resi 376 and resn ASP
select m_csa_690_right, m_csa_690 and chain X and resi 395 and resn ASP
show sticks, m_csa_690_left or m_csa_690_right
color tv_red, m_csa_690_left
color tv_blue, m_csa_690_right
distance m_csa_690_distance, (m_csa_690 and chain X and resi 376 and resn ASP and name CA), (m_csa_690 and chain X and resi 395 and resn ASP and name CA)
label m_csa_690_distance, "4.603 A"
zoom m_csa_690_left or m_csa_690_right, 8
set dash_width, 3
set label_size, 18
