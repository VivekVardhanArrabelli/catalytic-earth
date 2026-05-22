load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_1YVE.cif", m_csa_890
hide everything
show cartoon, m_csa_890
color gray70, m_csa_890
set cartoon_transparency, 0.8, m_csa_890
select m_csa_890_left, m_csa_890 and chain K and resi 248 and resn GLU
select m_csa_890_right, m_csa_890 and chain K and resi 181 and resn LYS
show sticks, m_csa_890_left or m_csa_890_right
color tv_red, m_csa_890_left
color tv_blue, m_csa_890_right
distance m_csa_890_distance, (m_csa_890 and chain K and resi 248 and resn GLU and name CA), (m_csa_890 and chain K and resi 181 and resn LYS and name CA)
label m_csa_890_distance, "10.269 A"
zoom m_csa_890_left or m_csa_890_right, 8
set dash_width, 3
set label_size, 18
