load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_1DPG.cif", m_csa_843
hide everything
show cartoon, m_csa_843
color gray70, m_csa_843
set cartoon_transparency, 0.8, m_csa_843
select m_csa_843_left, m_csa_843 and chain A and resi 178 and resn HIS
select m_csa_843_right, m_csa_843 and chain A and resi 240 and resn HIS
show sticks, m_csa_843_left or m_csa_843_right
color tv_red, m_csa_843_left
color tv_blue, m_csa_843_right
distance m_csa_843_distance, (m_csa_843 and chain A and resi 178 and resn HIS and name CA), (m_csa_843 and chain A and resi 240 and resn HIS and name CA)
label m_csa_843_distance, "8.109 A"
zoom m_csa_843_left or m_csa_843_right, 8
set dash_width, 3
set label_size, 18
