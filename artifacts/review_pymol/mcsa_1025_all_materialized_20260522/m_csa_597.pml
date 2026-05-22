load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_1UCH.cif", m_csa_597
hide everything
show cartoon, m_csa_597
color gray70, m_csa_597
set cartoon_transparency, 0.8, m_csa_597
select m_csa_597_left, m_csa_597 and chain A and resi 89 and resn GLN
select m_csa_597_right, m_csa_597 and chain A and resi 169 and resn HIS
show sticks, m_csa_597_left or m_csa_597_right
color tv_red, m_csa_597_left
color tv_blue, m_csa_597_right
distance m_csa_597_distance, (m_csa_597 and chain A and resi 89 and resn GLN and name CA), (m_csa_597 and chain A and resi 169 and resn HIS and name CA)
label m_csa_597_distance, "11.073 A"
zoom m_csa_597_left or m_csa_597_right, 8
set dash_width, 3
set label_size, 18
