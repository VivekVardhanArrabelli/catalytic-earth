load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_1L1D.cif", m_csa_715
hide everything
show cartoon, m_csa_715
color gray70, m_csa_715
set cartoon_transparency, 0.8, m_csa_715
select m_csa_715_left, m_csa_715 and chain B and resi 107 and resn HIS
select m_csa_715_right, m_csa_715 and chain B and resi 114 and resn ASP
show sticks, m_csa_715_left or m_csa_715_right
color tv_red, m_csa_715_left
color tv_blue, m_csa_715_right
distance m_csa_715_distance, (m_csa_715 and chain B and resi 107 and resn HIS and name CA), (m_csa_715 and chain B and resi 114 and resn ASP and name CA)
label m_csa_715_distance, "20.847 A"
zoom m_csa_715_left or m_csa_715_right, 8
set dash_width, 3
set label_size, 18
