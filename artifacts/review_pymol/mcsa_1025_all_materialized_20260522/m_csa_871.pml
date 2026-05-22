load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_1OKG.cif", m_csa_871
hide everything
show cartoon, m_csa_871
color gray70, m_csa_871
set cartoon_transparency, 0.8, m_csa_871
select m_csa_871_left, m_csa_871 and chain A and resi 61 and resn ASP
select m_csa_871_right, m_csa_871 and chain A and resi 255 and resn SER
show sticks, m_csa_871_left or m_csa_871_right
color tv_red, m_csa_871_left
color tv_blue, m_csa_871_right
distance m_csa_871_distance, (m_csa_871 and chain A and resi 61 and resn ASP and name CA), (m_csa_871 and chain A and resi 255 and resn SER and name CA)
label m_csa_871_distance, "11.147 A"
zoom m_csa_871_left or m_csa_871_right, 8
set dash_width, 3
set label_size, 18
