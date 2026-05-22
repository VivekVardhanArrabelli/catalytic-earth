load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_1I78.cif", m_csa_821
hide everything
show cartoon, m_csa_821
color gray70, m_csa_821
set cartoon_transparency, 0.8, m_csa_821
select m_csa_821_left, m_csa_821 and chain A and resi 210 and resn ASP
select m_csa_821_right, m_csa_821 and chain A and resi 85 and resn ASP
show sticks, m_csa_821_left or m_csa_821_right
color tv_red, m_csa_821_left
color tv_blue, m_csa_821_right
distance m_csa_821_distance, (m_csa_821 and chain A and resi 210 and resn ASP and name CA), (m_csa_821 and chain A and resi 85 and resn ASP and name CA)
label m_csa_821_distance, "16.036 A"
zoom m_csa_821_left or m_csa_821_right, 8
set dash_width, 3
set label_size, 18
