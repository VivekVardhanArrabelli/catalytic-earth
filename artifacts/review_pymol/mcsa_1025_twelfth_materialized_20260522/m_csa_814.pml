load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_1GLO.cif", m_csa_814
hide everything
show cartoon, m_csa_814
color gray70, m_csa_814
set cartoon_transparency, 0.8, m_csa_814
select m_csa_814_left, m_csa_814 and chain A and resi 164 and resn HIS
select m_csa_814_right, m_csa_814 and chain A and resi 19 and resn GLN
show sticks, m_csa_814_left or m_csa_814_right
color tv_red, m_csa_814_left
color tv_blue, m_csa_814_right
distance m_csa_814_distance, (m_csa_814 and chain A and resi 164 and resn HIS and name CA), (m_csa_814 and chain A and resi 19 and resn GLN and name CA)
label m_csa_814_distance, "11.561 A"
zoom m_csa_814_left or m_csa_814_right, 8
set dash_width, 3
set label_size, 18
