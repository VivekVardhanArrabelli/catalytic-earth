load "artifacts/v3_mcsa_pymol_fifth_materialized_coordinates_20260522/pdb_1B7B.cif", m_csa_669
hide everything
show cartoon, m_csa_669
color gray70, m_csa_669
set cartoon_transparency, 0.8, m_csa_669
select m_csa_669_left, m_csa_669 and chain A and resi 12 and resn ASN
select m_csa_669_right, m_csa_669 and chain A and resi 271 and resn LYS
show sticks, m_csa_669_left or m_csa_669_right
color tv_red, m_csa_669_left
color tv_blue, m_csa_669_right
distance m_csa_669_distance, (m_csa_669 and chain A and resi 12 and resn ASN and name CA), (m_csa_669 and chain A and resi 271 and resn LYS and name CA)
label m_csa_669_distance, "14.892 A"
zoom m_csa_669_left or m_csa_669_right, 8
set dash_width, 3
set label_size, 18
