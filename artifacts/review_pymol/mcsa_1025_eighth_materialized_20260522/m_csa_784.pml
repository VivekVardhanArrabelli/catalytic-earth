load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_1W0H.cif", m_csa_784
hide everything
show cartoon, m_csa_784
color gray70, m_csa_784
set cartoon_transparency, 0.8, m_csa_784
select m_csa_784_left, m_csa_784 and chain A and resi 116 and resn ASP
select m_csa_784_right, m_csa_784 and chain A and resi 175 and resn HIS
show sticks, m_csa_784_left or m_csa_784_right
color tv_red, m_csa_784_left
color tv_blue, m_csa_784_right
distance m_csa_784_distance, (m_csa_784 and chain A and resi 116 and resn ASP and name CA), (m_csa_784 and chain A and resi 175 and resn HIS and name CA)
label m_csa_784_distance, "11.073 A"
zoom m_csa_784_left or m_csa_784_right, 8
set dash_width, 3
set label_size, 18
