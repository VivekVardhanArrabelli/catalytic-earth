load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_2TDT.cif", m_csa_932
hide everything
show cartoon, m_csa_932
color gray70, m_csa_932
set cartoon_transparency, 0.8, m_csa_932
select m_csa_932_left, m_csa_932 and chain A and resi 166 and resn GLY
select m_csa_932_right, m_csa_932 and chain A and resi 141 and resn ASP
show sticks, m_csa_932_left or m_csa_932_right
color tv_red, m_csa_932_left
color tv_blue, m_csa_932_right
distance m_csa_932_distance, (m_csa_932 and chain A and resi 166 and resn GLY and name CA), (m_csa_932 and chain A and resi 141 and resn ASP and name CA)
label m_csa_932_distance, "17.475 A"
zoom m_csa_932_left or m_csa_932_right, 8
set dash_width, 3
set label_size, 18
