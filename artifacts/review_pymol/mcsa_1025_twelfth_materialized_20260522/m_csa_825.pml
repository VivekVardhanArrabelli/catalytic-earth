load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_1AHB.cif", m_csa_825
hide everything
show cartoon, m_csa_825
color gray70, m_csa_825
set cartoon_transparency, 0.8, m_csa_825
select m_csa_825_left, m_csa_825 and chain A and resi 71 and resn ILE
select m_csa_825_right, m_csa_825 and chain A and resi 163 and resn ARG
show sticks, m_csa_825_left or m_csa_825_right
color tv_red, m_csa_825_left
color tv_blue, m_csa_825_right
distance m_csa_825_distance, (m_csa_825 and chain A and resi 71 and resn ILE and name CA), (m_csa_825 and chain A and resi 163 and resn ARG and name CA)
label m_csa_825_distance, "13.102 A"
zoom m_csa_825_left or m_csa_825_right, 8
set dash_width, 3
set label_size, 18
