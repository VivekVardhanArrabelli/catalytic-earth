load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_2BIF.cif", m_csa_810
hide everything
show cartoon, m_csa_810
color gray70, m_csa_810
set cartoon_transparency, 0.8, m_csa_810
select m_csa_810_left, m_csa_810 and chain A and resi 263 and resn ASN
select m_csa_810_right, m_csa_810 and chain A and resi 326 and resn GLU
show sticks, m_csa_810_left or m_csa_810_right
color tv_red, m_csa_810_left
color tv_blue, m_csa_810_right
distance m_csa_810_distance, (m_csa_810 and chain A and resi 263 and resn ASN and name CA), (m_csa_810 and chain A and resi 326 and resn GLU and name CA)
label m_csa_810_distance, "13.239 A"
zoom m_csa_810_left or m_csa_810_right, 8
set dash_width, 3
set label_size, 18
