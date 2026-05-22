load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_1QAZ.cif", m_csa_684
hide everything
show cartoon, m_csa_684
color gray70, m_csa_684
set cartoon_transparency, 0.8, m_csa_684
select m_csa_684_left, m_csa_684 and chain A and resi 65 and resn TYR
select m_csa_684_right, m_csa_684 and chain A and resi 188 and resn ASN
show sticks, m_csa_684_left or m_csa_684_right
color tv_red, m_csa_684_left
color tv_blue, m_csa_684_right
distance m_csa_684_distance, (m_csa_684 and chain A and resi 65 and resn TYR and name CA), (m_csa_684 and chain A and resi 188 and resn ASN and name CA)
label m_csa_684_distance, "24.170 A"
zoom m_csa_684_left or m_csa_684_right, 8
set dash_width, 3
set label_size, 18
