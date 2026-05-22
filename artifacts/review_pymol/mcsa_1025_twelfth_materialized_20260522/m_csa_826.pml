load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_1UN1.cif", m_csa_826
hide everything
show cartoon, m_csa_826
color gray70, m_csa_826
set cartoon_transparency, 0.8, m_csa_826
select m_csa_826_left, m_csa_826 and chain B and resi 91 and resn GLU
select m_csa_826_right, m_csa_826 and chain B and resi 95 and resn GLU
show sticks, m_csa_826_left or m_csa_826_right
color tv_red, m_csa_826_left
color tv_blue, m_csa_826_right
distance m_csa_826_distance, (m_csa_826 and chain B and resi 91 and resn GLU and name CA), (m_csa_826 and chain B and resi 95 and resn GLU and name CA)
label m_csa_826_distance, "12.264 A"
zoom m_csa_826_left or m_csa_826_right, 8
set dash_width, 3
set label_size, 18
