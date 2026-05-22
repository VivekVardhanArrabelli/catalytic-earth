load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_8PCH.cif", m_csa_682
hide everything
show cartoon, m_csa_682
color gray70, m_csa_682
set cartoon_transparency, 0.8, m_csa_682
select m_csa_682_left, m_csa_682 and chain A and resi 20 and resn GLN
select m_csa_682_right, m_csa_682 and chain A and resi 166 and resn HIS
show sticks, m_csa_682_left or m_csa_682_right
color tv_red, m_csa_682_left
color tv_blue, m_csa_682_right
distance m_csa_682_distance, (m_csa_682 and chain A and resi 20 and resn GLN and name CA), (m_csa_682 and chain A and resi 166 and resn HIS and name CA)
label m_csa_682_distance, "12.008 A"
zoom m_csa_682_left or m_csa_682_right, 8
set dash_width, 3
set label_size, 18
