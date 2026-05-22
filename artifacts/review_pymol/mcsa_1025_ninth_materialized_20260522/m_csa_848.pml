load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_1ELU.cif", m_csa_848
hide everything
show cartoon, m_csa_848
color gray70, m_csa_848
set cartoon_transparency, 0.8, m_csa_848
select m_csa_848_left, m_csa_848 and chain A and resi 357 and resn ARG
select m_csa_848_right, m_csa_848 and chain A and resi 194 and resn ASP
show sticks, m_csa_848_left or m_csa_848_right
color tv_red, m_csa_848_left
color tv_blue, m_csa_848_right
distance m_csa_848_distance, (m_csa_848 and chain A and resi 357 and resn ARG and name CA), (m_csa_848 and chain A and resi 194 and resn ASP and name CA)
label m_csa_848_distance, "19.418 A"
zoom m_csa_848_left or m_csa_848_right, 8
set dash_width, 3
set label_size, 18
