load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_1K30.cif", m_csa_783
hide everything
show cartoon, m_csa_783
color gray70, m_csa_783
set cartoon_transparency, 0.8, m_csa_783
select m_csa_783_left, m_csa_783 and chain A and resi 139 and resn HIS
select m_csa_783_right, m_csa_783 and chain A and resi 144 and resn ASP
show sticks, m_csa_783_left or m_csa_783_right
color tv_red, m_csa_783_left
color tv_blue, m_csa_783_right
distance m_csa_783_distance, (m_csa_783 and chain A and resi 139 and resn HIS and name CA), (m_csa_783 and chain A and resi 144 and resn ASP and name CA)
label m_csa_783_distance, "6.955 A"
zoom m_csa_783_left or m_csa_783_right, 8
set dash_width, 3
set label_size, 18
