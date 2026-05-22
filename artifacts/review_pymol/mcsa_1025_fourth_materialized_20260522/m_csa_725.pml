load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_2ACU.cif", m_csa_725
hide everything
show cartoon, m_csa_725
color gray70, m_csa_725
set cartoon_transparency, 0.8, m_csa_725
select m_csa_725_left, m_csa_725 and chain A and resi 110 and resn HIS
select m_csa_725_right, m_csa_725 and chain A and resi 43 and resn ASP
show sticks, m_csa_725_left or m_csa_725_right
color tv_red, m_csa_725_left
color tv_blue, m_csa_725_right
distance m_csa_725_distance, (m_csa_725 and chain A and resi 110 and resn HIS and name CA), (m_csa_725 and chain A and resi 43 and resn ASP and name CA)
label m_csa_725_distance, "11.803 A"
zoom m_csa_725_left or m_csa_725_right, 8
set dash_width, 3
set label_size, 18
