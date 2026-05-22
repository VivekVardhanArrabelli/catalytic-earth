load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_1VID.cif", m_csa_915
hide everything
show cartoon, m_csa_915
color gray70, m_csa_915
set cartoon_transparency, 0.8, m_csa_915
select m_csa_915_left, m_csa_915 and chain A and resi 144 and resn LYS
select m_csa_915_right, m_csa_915 and chain A and resi 199 and resn GLU
show sticks, m_csa_915_left or m_csa_915_right
color tv_red, m_csa_915_left
color tv_blue, m_csa_915_right
distance m_csa_915_distance, (m_csa_915 and chain A and resi 144 and resn LYS and name CA), (m_csa_915 and chain A and resi 199 and resn GLU and name CA)
label m_csa_915_distance, "16.122 A"
zoom m_csa_915_left or m_csa_915_right, 8
set dash_width, 3
set label_size, 18
