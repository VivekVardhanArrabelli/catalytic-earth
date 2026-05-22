load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_2ET1.cif", m_csa_995
hide everything
show cartoon, m_csa_995
color gray70, m_csa_995
set cartoon_transparency, 0.8, m_csa_995
select m_csa_995_left, m_csa_995 and chain A and resi 90 and resn HIS
select m_csa_995_right, m_csa_995 and chain A and resi 149 and resn MET
show sticks, m_csa_995_left or m_csa_995_right
color tv_red, m_csa_995_left
color tv_blue, m_csa_995_right
distance m_csa_995_distance, (m_csa_995 and chain A and resi 90 and resn HIS and name CA), (m_csa_995 and chain A and resi 149 and resn MET and name CA)
label m_csa_995_distance, "16.937 A"
zoom m_csa_995_left or m_csa_995_right, 8
set dash_width, 3
set label_size, 18
