load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_4USJ.cif", m_csa_870
hide everything
show cartoon, m_csa_870
color gray70, m_csa_870
set cartoon_transparency, 0.8, m_csa_870
select m_csa_870_left, m_csa_870 and chain A and resi 119 and resn ARG
select m_csa_870_right, m_csa_870 and chain A and resi 237 and resn ASP
show sticks, m_csa_870_left or m_csa_870_right
color tv_red, m_csa_870_left
color tv_blue, m_csa_870_right
distance m_csa_870_distance, (m_csa_870 and chain A and resi 119 and resn ARG and name CA), (m_csa_870 and chain A and resi 237 and resn ASP and name CA)
label m_csa_870_distance, "18.305 A"
zoom m_csa_870_left or m_csa_870_right, 8
set dash_width, 3
set label_size, 18
