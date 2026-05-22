load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_1QIB.cif", m_csa_906
hide everything
show cartoon, m_csa_906
color gray70, m_csa_906
set cartoon_transparency, 0.8, m_csa_906
select m_csa_906_left, m_csa_906 and chain A and resi 125 and resn HIS
select m_csa_906_right, m_csa_906 and chain A and resi 116 and resn GLU
show sticks, m_csa_906_left or m_csa_906_right
color tv_red, m_csa_906_left
color tv_blue, m_csa_906_right
distance m_csa_906_distance, (m_csa_906 and chain A and resi 125 and resn HIS and name CA), (m_csa_906 and chain A and resi 116 and resn GLU and name CA)
label m_csa_906_distance, "10.635 A"
zoom m_csa_906_left or m_csa_906_right, 8
set dash_width, 3
set label_size, 18
