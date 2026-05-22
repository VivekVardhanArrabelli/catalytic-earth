load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_1BOU.cif", m_csa_672
hide everything
show cartoon, m_csa_672
color gray70, m_csa_672
set cartoon_transparency, 0.8, m_csa_672
select m_csa_672_left, m_csa_672 and chain B and resi 61 and resn HIS
select m_csa_672_right, m_csa_672 and chain B and resi 195 and resn HIS
show sticks, m_csa_672_left or m_csa_672_right
color tv_red, m_csa_672_left
color tv_blue, m_csa_672_right
distance m_csa_672_distance, (m_csa_672 and chain B and resi 61 and resn HIS and name CA), (m_csa_672 and chain B and resi 195 and resn HIS and name CA)
label m_csa_672_distance, "15.297 A"
zoom m_csa_672_left or m_csa_672_right, 8
set dash_width, 3
set label_size, 18
