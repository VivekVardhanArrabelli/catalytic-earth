SELECT
  rm.case_id AS case_id,
  (
    SELECT group_concat(value, ' || ')
    FROM (
      SELECT f.fold_classification_id AS value
      FROM folds AS f
      WHERE f.case_id = rm.case_id
      ORDER BY f.fold_classification_id
    )
  ) AS fold_classification_ids,
  (
    SELECT group_concat(value, ' || ')
    FROM (
      SELECT
        s.site_id || ' roles=[' ||
        CASE WHEN s.roles = '' THEN 'source role not assigned' ELSE replace(s.roles, '|', ', ') END ||
        '] mappings=[' || s.mappings || ']' AS value
      FROM sites AS s
      WHERE s.record_id = c.hypothesis_record_id
      ORDER BY s.sequence_position, s.site_id
    )
  ) AS catalytic_site_roles,
  COALESCE(
    (
      SELECT group_concat(value, ' || ')
      FROM (
        SELECT
          ms.proposal_id || '/order-' || ms.step_order || ': ' || ms.summary ||
          ' [sites=' || ms.catalyst_site_ids ||
          '; inferred=' || ms.is_inferred ||
          '; source_flows=' || ms.electron_flow_count || ']' AS value
        FROM mechanism_steps AS ms
        WHERE ms.record_id = c.hypothesis_record_id
        ORDER BY ms.proposal_id, ms.step_order
      )
    ),
    (
      SELECT 'ABSTAIN: ' || da.reason || ' [unsupported=' || da.unsupported_fields || ']'
      FROM detail_abstentions AS da
      WHERE da.record_id = c.hypothesis_record_id
    )
  ) AS mechanism_steps_or_abstention,
  (
    SELECT group_concat(value, ' || ')
    FROM (
      SELECT
        'structure:' || st.pdb_id || '[' || st.applicability ||
        '; flags=' || st.context_flags || '; limit=' || st.limitation || ']' AS value
      FROM structures AS st
      WHERE st.record_id = c.hypothesis_record_id
      UNION ALL
      SELECT
        'evidence:' || ev.evidence_id || '[' || ev.applicability ||
        '; role=' || ev.evidence_role || ']' AS value
      FROM evidence AS ev
      WHERE ev.record_id = c.hypothesis_record_id
      ORDER BY value
    )
  ) AS source_applicability,
  (
    SELECT group_concat(value, ' || ')
    FROM (
      SELECT
        ce.counterevidence_id || ': ' || ce.summary ||
        ' [effect=' || ce.effect || '; disposition=' || ce.disposition || ']' AS value
      FROM counterevidence AS ce
      WHERE ce.record_id = c.hypothesis_record_id
      ORDER BY ce.counterevidence_id
    )
  ) AS counterevidence,
  (
    SELECT group_concat(value, ' || ')
    FROM (
      SELECT
        u.uncertainty_id || ': ' || u.summary || ' [abstention=' || u.abstention || ']' AS value
      FROM uncertainties AS u
      WHERE u.record_id = c.hypothesis_record_id
      ORDER BY u.uncertainty_id
    )
  ) AS uncertainty,
  (
    SELECT
      'selection=' || p.selection_sha256 ||
      '; source_snapshot_set=' || p.source_snapshot_set_sha256 ||
      '; compilation_spec=' || p.compilation_spec_sha256 ||
      '; compiler=' || p.compiler_version
    FROM provenance AS p
    WHERE p.record_id = c.hypothesis_record_id
  ) AS provenance,
  r.source_status ||
    CASE WHEN r.source_record_id IS NULL THEN '; record=NULL' ELSE '; record=' || r.source_record_id END ||
    '; query=' || r.source_query ||
    CASE WHEN r.equation IS NULL THEN '; equation=NULL' ELSE '; equation=' || r.equation END
    AS reaction_or_source_gap,
  (
    SELECT group_concat(value, ' || ')
    FROM (
      SELECT rf.feature_id || ': ' || rf.label AS value
      FROM relationship_features AS rf
      WHERE rf.group_id = rm.group_id AND rf.feature_kind = 'shared'
      ORDER BY rf.feature_id
    )
  ) AS shared_strategy,
  (
    SELECT group_concat(value, ' || ')
    FROM (
      SELECT
        rf.feature_id || ': ' || rf.label || ' [sites=' || rf.site_ids ||
        '; evidence=' || rf.evidence_keys || ']' AS value
      FROM relationship_features AS rf
      WHERE rf.group_id = rm.group_id
        AND rf.feature_kind = 'member_distinction'
        AND rf.case_id = rm.case_id
      ORDER BY rf.feature_id
    )
  ) AS member_deviations,
  rel.comparison_boundary AS transfer_boundary
FROM relationship_members AS rm
JOIN relationships AS rel ON rel.group_id = rm.group_id
JOIN cases AS c ON c.case_id = rm.case_id
JOIN reactions AS r ON r.case_id = rm.case_id
WHERE rm.group_id = 'atlas10.relationship.convergent-serine-proteases'
ORDER BY rm.case_id;
