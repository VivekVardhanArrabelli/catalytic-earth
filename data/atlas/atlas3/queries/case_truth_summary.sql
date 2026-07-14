SELECT
    c.case_id,
    c.label,
    c.ec_number,
    (SELECT MAX(r.evidence_tier) FROM records AS r WHERE r.case_id = c.case_id) AS highest_tier,
    (SELECT r.status FROM records AS r WHERE r.case_id = c.case_id AND r.object_type = 'source_mechanism') AS source_mechanism_status,
    (SELECT r.status FROM records AS r WHERE r.case_id = c.case_id AND r.object_type = 'mechanism_hypothesis') AS hypothesis_status,
    (SELECT COUNT(DISTINCT e.evidence_id) FROM evidence AS e WHERE e.case_id = c.case_id AND e.applicability = 'direct') AS direct_evidence_handles,
    (SELECT GROUP_CONCAT(ordered.evidence_id, ';') FROM (SELECT DISTINCT e.evidence_id FROM evidence AS e WHERE e.case_id = c.case_id AND e.applicability = 'direct' ORDER BY e.evidence_id) AS ordered) AS direct_source_handles,
    (SELECT COUNT(DISTINCT e.evidence_id) FROM evidence AS e WHERE e.case_id = c.case_id AND e.applicability = 'counterexample_same_ec') AS counterexample_evidence_handles,
    (SELECT GROUP_CONCAT(ordered.evidence_id, ';') FROM (SELECT DISTINCT e.evidence_id FROM evidence AS e WHERE e.case_id = c.case_id AND e.applicability = 'counterexample_same_ec' ORDER BY e.evidence_id) AS ordered) AS counterexample_source_handles,
    (SELECT r.step_count FROM records AS r WHERE r.case_id = c.case_id AND r.object_type = 'mechanism_hypothesis') AS hypothesis_steps,
    (SELECT r.site_count FROM records AS r WHERE r.case_id = c.case_id AND r.object_type = 'mechanism_hypothesis') AS grounded_sites,
    (SELECT COUNT(*) FROM uncertainties AS u WHERE u.case_id = c.case_id AND u.status = 'open') AS open_uncertainties,
    (SELECT COUNT(*) FROM counterevidence AS x WHERE x.case_id = c.case_id) AS counterevidence_items,
    c.assay_candidate,
    c.key_abstention
FROM cases AS c
ORDER BY c.case_id;
