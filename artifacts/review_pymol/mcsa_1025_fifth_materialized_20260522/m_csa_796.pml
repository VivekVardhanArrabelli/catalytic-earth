load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_1FA0.cif", m_csa_796
hide everything
show cartoon, m_csa_796
color gray70, m_csa_796
set cartoon_transparency, 0.8, m_csa_796
select m_csa_796_left, m_csa_796 and chain A and resi 224 and resn TYR
select m_csa_796_right, m_csa_796 and chain A and resi 154 and resn ASP
show sticks, m_csa_796_left or m_csa_796_right
color tv_red, m_csa_796_left
color tv_blue, m_csa_796_right
distance m_csa_796_distance, (m_csa_796 and chain A and resi 224 and resn TYR and name CA), (m_csa_796 and chain A and resi 154 and resn ASP and name CA)
label m_csa_796_distance, "20.825 A"
zoom m_csa_796_left or m_csa_796_right, 8
set dash_width, 3
set label_size, 18
