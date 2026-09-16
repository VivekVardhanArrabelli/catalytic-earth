/* Catalytic Earth Mechanism Workbench — frontend.
 *
 * Every scientific value rendered here is read from a live query response.
 * Nothing scientific is hard-coded in this file: no measured numbers, no
 * residue assignments, no site mappings, no evidence text.
 */
"use strict";

const SVG_NS = "http://www.w3.org/2000/svg";

const state = {
  mcsaId: null,
  view: null,        // transformation_view
  sites: null,       // sites_view
  evidence: null,    // evidence_view
  external: null,    // external_sources_view
  step: 0,           // 0 = before panel; N = all edits applied
  selectedAtom: null,
  selectedFragment: null,
  clauses: [],
};

/* ----------------------------------------------------------------- utils */
const el = (id) => document.getElementById(id);
const esc = (v) =>
  String(v === null || v === undefined ? "" : v).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

/** Render a value honestly: null/undefined becomes an explicit "unknown". */
const val = (v) =>
  v === null || v === undefined || v === ""
    ? '<span class="chip chip-unresolved">unknown</span>'
    : esc(v);

function kv(pairs) {
  const rows = pairs
    .filter((p) => p)
    .map(([k, v]) => `<dt>${esc(k)}</dt><dd>${v}</dd>`)
    .join("");
  return `<dl class="kv">${rows}</dl>`;
}

async function getJSON(url) {
  const res = await fetch(url);
  const body = await res.json();
  if (!res.ok) throw new Error(body.error || res.statusText);
  return body;
}

async function postJSON(url, payload) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const body = await res.json();
  if (!res.ok) throw new Error(body.error || res.statusText);
  return body;
}

/* ------------------------------------------------------- replay mechanics */

/** Bond key that ignores endpoint order. */
const bondKey = (ids) => [...ids].sort().join("~");

/**
 * Apply the first `n` edits to the before-panel graph.
 * This is a symbolic graph edit replay of a published source proposal.
 * It moves no atoms and asserts no physical trajectory.
 */
function graphAtStep(view, n) {
  const bonds = new Map();
  view.before_graph.bonds.forEach((b) =>
    bonds.set(bondKey(b.atom_ids), { atom_ids: [...b.atom_ids], order: b.order }));
  const charge = new Map();
  const stereo = new Map();
  view.before_graph.atoms.forEach((a) => {
    charge.set(a.atom_id, a.formal_charge);
    stereo.set(a.atom_id, a.stereochemistry);
  });

  const touchedBonds = new Map(); // key -> edit kind, for highlighting
  const touchedAtoms = new Map();

  view.edits.slice(0, n).forEach((e) => {
    const k = bondKey(e.atom_ids);
    if (e.operation === "remove_bond") {
      bonds.delete(k);
      touchedBonds.set(k, "break");
    } else if (e.operation === "add_bond") {
      bonds.set(k, { atom_ids: [...e.atom_ids], order: e.after });
      touchedBonds.set(k, "form");
    } else if (e.operation === "set_bond_order") {
      if (bonds.has(k)) bonds.get(k).order = e.after;
      touchedBonds.set(k, "order");
    } else if (e.operation === "set_formal_charge") {
      charge.set(e.atom_ids[0], e.after);
      touchedAtoms.set(e.atom_ids[0], "charge");
    } else if (e.operation === "set_stereochemistry") {
      stereo.set(e.atom_ids[0], e.after);
      touchedAtoms.set(e.atom_ids[0], "stereo");
    }
    e.atom_ids.forEach((id) => { if (!touchedAtoms.has(id)) touchedAtoms.set(id, "bond"); });
  });

  return { bonds, charge, stereo, touchedBonds, touchedAtoms };
}

/* --------------------------------------------------------------- graph UI */

function drawGraph() {
  const svg = el("graph");
  svg.innerHTML = "";
  const view = state.view;
  if (!view) return;

  const n = state.step;
  const g = graphAtStep(view, n);
  const pos = view.layout.positions;
  const box = view.layout.viewbox;
  const pad = 1.4;
  svg.setAttribute(
    "viewBox",
    `${box.min_x - pad} ${box.min_y - pad} ${box.width + pad * 2} ${box.height + pad * 2}`);

  const fragmentAtoms = new Set(
    state.selectedFragment ? state.selectedFragment.atoms.map((a) => a.atom_id) : []);

  // The edit applied most recently, for emphasis.
  const currentEdit = n > 0 ? view.edits[n - 1] : null;
  const currentBondKey = currentEdit && currentEdit.atom_ids.length === 2
    ? bondKey(currentEdit.atom_ids) : null;

  // bonds
  const bondLayer = document.createElementNS(SVG_NS, "g");
  g.bonds.forEach((bond, key) => {
    const [a, b] = bond.atom_ids;
    if (!pos[a] || !pos[b]) return;
    const [x1, y1] = pos[a];
    const [x2, y2] = pos[b];
    const kind = g.touchedBonds.get(key);
    const order = bond.order || 1;
    // Draw multiplicity as parallel offset lines.
    const dx = x2 - x1, dy = y2 - y1;
    const len = Math.hypot(dx, dy) || 1;
    const ox = (-dy / len) * 0.09, oy = (dx / len) * 0.09;
    const lines = order >= 3 ? [-1, 0, 1] : order === 2 ? [-0.6, 0.6] : [0];
    lines.forEach((m) => {
      const line = document.createElementNS(SVG_NS, "line");
      line.setAttribute("x1", x1 + ox * m);
      line.setAttribute("y1", y1 + oy * m);
      line.setAttribute("x2", x2 + ox * m);
      line.setAttribute("y2", y2 + oy * m);
      line.setAttribute("class", "bond" + (kind ? ` is-${kind}` : ""));
      // Screen-space stroke so bond width stays legible at any zoom level.
      line.setAttribute("vector-effect", "non-scaling-stroke");
      line.setAttribute("stroke-width", key === currentBondKey ? 3.2 : 1.6);
      bondLayer.appendChild(line);
    });
  });
  svg.appendChild(bondLayer);

  // atoms
  const atomLayer = document.createElementNS(SVG_NS, "g");
  view.before_graph.atoms.forEach((atom) => {
    const p = pos[atom.atom_id];
    if (!p) return;
    const node = document.createElementNS(SVG_NS, "g");
    const changed = g.touchedAtoms.has(atom.atom_id);
    let cls = "atom-node";
    if (changed) cls += " is-changed";
    if (state.selectedAtom === atom.atom_id) cls += " is-selected";
    if (fragmentAtoms.has(atom.atom_id)) cls += " in-fragment";
    node.setAttribute("class", cls);
    node.setAttribute("transform", `translate(${p[0]},${p[1]})`);

    const circle = document.createElementNS(SVG_NS, "circle");
    circle.setAttribute("r", 0.46);
    circle.setAttribute("vector-effect", "non-scaling-stroke");
    node.appendChild(circle);

    const label = document.createElementNS(SVG_NS, "text");
    label.setAttribute("class", "atom-label");
    label.setAttribute("text-anchor", "middle");
    label.setAttribute("dy", "0.1");
    label.setAttribute("style", "font-size:0.42px");
    const q = g.charge.get(atom.atom_id);
    label.textContent = atom.element + (q ? (q > 0 ? "+".repeat(q) : "−".repeat(-q)) : "");
    node.appendChild(label);

    const idText = document.createElementNS(SVG_NS, "text");
    idText.setAttribute("class", "atom-id");
    idText.setAttribute("text-anchor", "middle");
    idText.setAttribute("dy", "0.95");
    idText.setAttribute("style", "font-size:0.3px");
    idText.textContent = atom.atom_id;
    node.appendChild(idText);

    node.addEventListener("click", () => {
      state.selectedAtom = state.selectedAtom === atom.atom_id ? null : atom.atom_id;
      state.selectedFragment = null;
      drawGraph();
      renderInspector();
      renderFragments();
    });
    atomLayer.appendChild(node);
  });
  svg.appendChild(atomLayer);
}

function renderReplayControls() {
  const view = state.view;
  const total = view.edits.length;
  el("step-readout").textContent =
    state.step === 0
      ? `before panel — 0 of ${total} edits applied`
      : `${state.step} of ${total} edits applied`;
  el("btn-step-back").disabled = state.step === 0;
  el("btn-step-fwd").disabled = state.step === total;

  el("edit-list").innerHTML = view.edits
    .map((e, i) => {
      let cls = "";
      if (i < state.step) cls = "is-applied";
      if (i === state.step - 1) cls = "is-applied is-current";
      return `<li class="${cls}" data-step="${i + 1}">${esc(e.label)}
        <span class="flow">[${esc(e.edit_id)} &middot; arrow ${esc(e.source_flow_id)}]</span></li>`;
    })
    .join("");
  el("edit-list").querySelectorAll("li").forEach((li) =>
    li.addEventListener("click", () => setStep(Number(li.dataset.step))));
}

function setStep(n) {
  const total = state.view.edits.length;
  state.step = Math.max(0, Math.min(total, n));
  drawGraph();
  renderReplayControls();
}

/* ----------------------------------------------------------- fragments/UI */

function renderFragments() {
  const host = el("fragment-list");
  const relations = (state.evidence && state.mcsaId === "M0187")
    ? state.evidence.relations : [];

  const parts = [];

  if (relations.length) {
    parts.push(relations.map((r, i) => {
      const resolved = Boolean(r.site_id);
      const label = r.residue_label && r.residue_label.residue_label
        ? r.residue_label.residue_label.raw_label : null;
      const obsCount = r.functional_evidence.matched_observations.length;
      const chip = resolved
        ? `<span class="chip chip-site">${esc(r.site_id)}</span>`
        : `<span class="chip chip-unresolved">unresolved</span>`;
      const sel = state.selectedFragment === r ? " is-selected" : "";
      return `<button class="frag${sel}" data-frag="${i}">
          <span class="frag-top"><strong>${esc(label || "source fragment")}</strong>${chip}</span>
          <span class="frag-sub">source atom ${esc(r.source_atom_id)} &middot; step ${esc(r.source_step_id)}
            &middot; ${r.atoms.length} fragment atoms &middot; ${obsCount} matched observation(s)</span>
        </button>`;
    }).join(""));
  }

  // Changed atoms and their site links, from the transformation-sites query.
  if (state.sites) {
    const s = state.sites;
    parts.push(`<h3 class="minor">Changed atoms with an explicit site label
      (${esc(s.resolved_source_atom_count)} of ${esc(s.changed_source_atom_count)} resolved)</h3>`);
    parts.push(s.atoms.map((a) => {
      const resolved = Boolean(a.site_id);
      const chip = resolved
        ? `<span class="chip chip-site">${esc(a.site_id)}</span>`
        : `<span class="chip chip-unresolved">unresolved</span>`;
      const sel = state.selectedAtom === a.source_atom_id ? " is-selected" : "";
      return `<button class="frag${sel}" data-site-atom="${esc(a.source_atom_id)}">
          <span class="frag-top"><strong>${esc(a.source_atom_id)} (${esc(a.element)})</strong>${chip}</span>
          <span class="frag-sub">edits ${esc(a.edit_ids.join(", "))}</span>
        </button>`;
    }).join(""));
    if (!relations.length && state.mcsaId !== "M0187") {
      parts.push(`<p class="note">No packaged source-fragment relation is available for this
        mechanism; the site links above come from the explicit atom-label query only.</p>`);
    }
  }

  host.innerHTML = parts.join("");
  host.querySelectorAll("[data-frag]").forEach((btn) =>
    btn.addEventListener("click", () => {
      const r = relations[Number(btn.dataset.frag)];
      state.selectedFragment = state.selectedFragment === r ? null : r;
      state.selectedAtom = state.selectedFragment ? r.source_atom_id : null;
      drawGraph(); renderFragments(); renderInspector();
    }));
  host.querySelectorAll("[data-site-atom]").forEach((btn) =>
    btn.addEventListener("click", () => {
      const id = btn.dataset.siteAtom;
      state.selectedAtom = state.selectedAtom === id ? null : id;
      state.selectedFragment = null;
      drawGraph(); renderFragments(); renderInspector();
    }));
}

function structureBlock(ctx) {
  if (!ctx || ctx.status === "not_resolved" || !(ctx.structures || []).length) {
    return `<p class="note"><span class="chip chip-unresolved">unresolved</span>
      No supported protein-structure context for this atom:
      ${val(ctx && ctx.reason)}</p>`;
  }
  const mapRows = (ctx.pdb_residue_mappings || []).map((m) => `
    <tr><td>${esc(ctx.uniprot_id)} ${esc(ctx.residue_name)}${esc(ctx.sequence_position)}</td>
        <td>${esc(m.pdb_id)} chain ${esc(m.chain_id)} author ${esc(m.author_position)}</td>
        <td>mmCIF label ${esc(m.label_position)}</td></tr>`).join("");
  // Mark a structure only where an external structure view was actually
  // recorded against its accession.
  const bySubject = (state.external && state.external.contributions_by_subject) || {};
  const structures = (ctx.structures || []).map((s) => {
    const viewed = (bySubject[`PDB:${s.pdb_id}`] || []).length
      ? ` <span class="chip chip-external">external structure view recorded</span>`
      : "";
    return `<p class="note"><span class="chip chip-structure">reference structure</span>
      <strong>${esc(s.pdb_id)}</strong> ${esc(s.experimental_method)},
      ${val(s.resolution_angstrom)} &#8491;.${viewed}
      ${esc((s.context_flags || []).join(", "))}.<br>${esc(s.limitation)}</p>`;
  }).join("");
  return `
    <p class="note">Numbering systems are distinct and travel together:</p>
    <table class="mini">
      <tr><th>UniProt natural sequence</th><th>PDB author numbering</th><th>mmCIF label numbering</th></tr>
      ${mapRows}
    </table>
    <p class="note">${esc((ctx.pdb_residue_mappings[0] || {}).numbering_note || "")}</p>
    ${structures}`;
}

function observationCard(o) {
  const r = o.result || {};
  const ep = o.endpoint || {};
  const sub = o.substrate || {};
  const cls = "k-" + (r.result_class || "unknown");

  let chip, resultText;
  if (r.result_class === "measured") {
    chip = '<span class="chip chip-measured">published measurement</span>';
    resultText = `<strong>${esc(r.value)} ${esc(r.unit)}</strong>, reported as
      <em>${esc(r.reported_relation)}</em> versus
      ${o.comparator_variant_id
        ? `comparator <strong>${esc(o.comparator_variant_id)}</strong>`
        : '<span class="chip chip-unresolved">no stated comparator</span>'}`;
  } else if (r.result_class === "not_detected") {
    chip = '<span class="chip chip-nondetect">nondetection</span>';
    resultText = `<strong>not detected</strong> under the reported conditions`;
  } else if (r.result_class === "no_detectable_difference") {
    chip = '<span class="chip chip-nodiff">no detectable difference</span>';
    resultText = `<strong>no detectable difference</strong> reported`;
  } else {
    chip = '<span class="chip chip-unresolved">unresolved</span>';
    resultText = val(r.result_class);
  }

  const conditions = (o.conditions || []).length
    ? (o.conditions || []).map((c) =>
        `${esc(c.name)} ${esc(c.value)}${c.unit ? " " + esc(c.unit) : ""}`).join(", ")
    : '<span class="chip chip-unresolved">conditions not stated</span>';

  const bySubject = (state.external && state.external.contributions_by_subject) || {};
  const badged = new Set();
  const witnesses = (o.source_witnesses || []).map((w) => {
    // Mark an external lookup only where one was actually recorded for this
    // evidence id, and only once per observation rather than per quotation.
    const looked = (bySubject[w.evidence_id] || []).length;
    let badge = "";
    if (looked && !badged.has(w.evidence_id)) {
      badged.add(w.evidence_id);
      badge = ` <span class="chip chip-external">external lookup recorded</span>`;
    }
    return `<div class="witness"><q>${esc(w.exact_text)}</q> &mdash; ${esc(w.evidence_id)}, ${esc(w.locator)}${badge}</div>`;
  }).join("");

  // A reported structural comparison is not a deposited structure. Say so
  // where the packaged record names none, so a resolution reported here is not
  // read as belonging to a reference structure shown elsewhere.
  const namesNoDeposit = ep.kind === "structure"
    ? `<p class="caveat">This packaged observation names no deposited structure.
         The resolution above belongs to the reported comparison, not to any
         reference structure shown elsewhere in this interface.</p>`
    : "";

  // Detection floors stay unknown when the source does not state them, and a
  // nondetection and an unresolved difference are not the same statement.
  let floor = "";
  if (r.result_class === "not_detected" || r.result_class === "no_detectable_difference") {
    const limit = `Detection limit: ${val(r.detection_limit)}
      ${r.detection_limit_unit ? esc(r.detection_limit_unit) : ""}.`;
    floor = r.result_class === "not_detected"
      ? `<p class="note">${limit} Nondetection is not a numeric zero and does not
           establish loss of every capability.</p>`
      : `<p class="note">${limit} No difference was resolved at the reported
           limit, which does not establish that no difference exists.</p>`;
  }

  return `<div class="obs ${cls}">
    <div class="obs-head">
      <span class="obs-title">${esc(ep.name || ep.kind)}${
        sub.name ? ` &middot; ${esc(sub.enantiomer ? sub.enantiomer + "-" : "")}${esc(sub.name)}` : ""}</span>
      ${chip}
    </div>
    <div class="obs-result">${resultText}</div>
    <p class="note">Endpoint kind <code>${esc(ep.kind)}</code> &middot; conditions: ${conditions}
      &middot; observation <code>${esc(o.observation_id)}</code></p>
    ${namesNoDeposit}
    ${floor}
    ${o.project_interpretation
      ? `<p class="obs-interp"><strong>Project reading (${esc(o.project_interpretation.status)}):</strong>
          ${esc(o.project_interpretation.statement)}</p>` : ""}
    ${witnesses}
  </div>`;
}

function renderInspector() {
  const host = el("inspector-body");
  const frag = state.selectedFragment;
  const atomId = state.selectedAtom;

  if (!frag && !atomId) { host.innerHTML = ""; el("inspect-hint").style.display = ""; return; }
  el("inspect-hint").style.display = "none";

  // A source fragment carries the richer relation (residue + evidence).
  if (frag) {
    const rl = (frag.residue_label || {}).residue_label || {};
    const fe = frag.functional_evidence || {};
    const retained = frag.retained_depiction_coordinates || {};
    const coordCount = Object.keys(retained.coordinates || {}).length;

    const obs = (fe.matched_observations || []).map(observationCard).join("");
    const evidenceBlock = obs
      ? `<h3 class="minor">Endpoint-specific evidence bound to this site</h3>${obs}`
      : `<p class="note"><span class="chip chip-unresolved">no matched observations</span>
           Relationship: <code>${val(fe.relationship)}</code>.
           This is reference-site context, not a matched control for the assayed variant.</p>`;

    host.innerHTML = `
      <h3 class="minor">Source fragment ${esc(frag.source_atom_id)}</h3>
      ${kv([
        ["source residue label", val(rl.raw_label)],
        ["fragment basis", val(frag.fragment_basis)],
        ["atlas site", frag.site_id
          ? esc(frag.site_id)
          : `<span class="chip chip-unresolved">not resolved</span> ${val((frag.site_mapping||{}).reason)}`],
        ["match basis", val((frag.site_mapping || {}).match_basis)],
        ["deposited atom identity", `${val((frag.deposited_atom_identity||{}).status)}
            ${(frag.deposited_atom_identity||{}).reason ? "<br>" + esc(frag.deposited_atom_identity.reason) : ""}`],
        ["source step", val(frag.source_step_id)],
        ["retained depiction coordinates",
          coordCount
            ? `${coordCount} atoms carry retained source x2/y2 values`
            : '<span class="chip chip-unresolved">none retained</span>'],
        ["source arrow experimentally validated",
          String(fe.source_arrow_experimentally_validated)],
      ])}
      <p class="caveat">${esc((retained.semantics || {}).note || "")}</p>
      ${structureBlock(frag.protein_structure_context)}
      ${evidenceBlock}`;
    return;
  }

  // Otherwise fall back to the transformation-sites record for this atom.
  const rec = state.sites && state.sites.atoms.find((a) => a.source_atom_id === atomId);
  const atom = state.view.before_graph.atoms.find((a) => a.atom_id === atomId);
  const edits = state.view.edits.filter((e) => e.atom_ids.includes(atomId));

  host.innerHTML = `
    <h3 class="minor">Source atom ${esc(atomId)}</h3>
    ${kv([
      ["element", val(atom && atom.element)],
      ["formal charge (before panel)", val(atom ? String(atom.formal_charge) : null)],
      ["stereochemistry (before panel)", val(atom && atom.stereochemistry)],
      ["edits naming this atom", edits.length
        ? esc(edits.map((e) => e.edit_id).join(", ")) : "none"],
      ["locator meaning",
        "local source-depiction locator, not a physical atom identity or PDB atom name"],
    ])}
    ${rec
      ? `${kv([
          ["atlas site", rec.site_id
            ? esc(rec.site_id)
            : `<span class="chip chip-unresolved">unresolved</span> ${val((rec.site_mapping||{}).reason)}`],
          ["source residue label",
            val(((rec.residue_label || {}).residue_label || {}).raw_label)],
          ["deposited atom identity", val((rec.deposited_atom_identity||{}).status)],
        ])}
        ${structureBlock(rec.protein_structure_context)}`
      : `<p class="note">This atom is not among the changed nodes returned by the
           site query, so it carries no site relationship here.</p>`}`;
}

/* ------------------------------------------------------------- evidence UI */

function renderEvidence() {
  const ev = state.evidence;
  const host = el("evidence-list");
  if (!ev) { host.innerHTML = ""; return; }

  host.innerHTML = ev.observations.map(observationCard).join("");

  const sel = el("endpoint-select");
  const current = sel.value;
  sel.innerHTML = `<option value="">all endpoints</option>` +
    (state.endpointKinds || []).map((k) =>
      `<option value="${esc(k)}"${k === current ? " selected" : ""}>${esc(k)}</option>`).join("");

  el("abstention-strip").innerHTML = (ev.abstentions || []).length
    ? `<p class="note"><strong>${esc(ev.abstentions.length)} mandatory abstentions</strong>
         apply to these observations. They are part of the packaged record.</p>` +
      (ev.abstentions || []).map((a) => `
        <details class="abstention">
          <summary>${esc(a.abstention_id || "abstention")}</summary>
          <p class="note">${esc(a.reason || JSON.stringify(a))}</p>
        </details>`).join("")
    : "";

  el("evidence-note").innerHTML = `
    Evidence set <code>${esc(ev.evidence_set_id)}</code> &middot;
    ${esc(ev.matched_observation_count)} matched observation(s) &middot;
    ${esc(ev.relation_counts.resolved)} of ${esc(ev.relation_counts.total)} source-fragment
    relations resolved to a site.
    Counts are observations, not mechanisms. An empty result means no match in the
    packaged evidence set, not absence of the chemistry.`;

  const cases = ev.cases.map((c) => `
    ${kv([
      ["case", esc(c.case_id)],
      ["question", esc(c.question)],
      ["adjudication", esc(JSON.stringify(c.adjudication))],
      ["applicability", esc(JSON.stringify(c.applicability))],
    ])}
    <h3 class="minor">Discriminants</h3>
    <ul class="note">${(c.discriminants || []).map((d) =>
        `<li>${esc(typeof d === "string" ? d : JSON.stringify(d))}</li>`).join("")}</ul>
    <h3 class="minor">Mandatory abstentions</h3>
    <ul class="note">${(c.mandatory_abstentions || []).map((a) =>
        `<li>${esc(a.reason || JSON.stringify(a))}</li>`).join("")}</ul>`).join("");

  el("evidence-detail").innerHTML = cases + `
    <h3 class="minor">Review status of this evidence set</h3>
    ${kv(Object.entries(ev.review || {}).map(([k, v]) => [k, esc(JSON.stringify(v))]))}`;
}

/**
 * Render the external tool contribution ledger exactly as it stands.
 * An empty ledger is shown as empty. Nothing is invented to fill it.
 */
function renderExternal() {
  const ex = state.external;
  if (!ex) return;
  const note = el("external-note");
  const host = el("external-list");

  if (!ex.contribution_count) {
    note.innerHTML = `<span class="chip chip-unresolved">none recorded</span>
      ${esc(ex.semantics.empty_means || "")}
      Local Python calculations are not external tool output and are not listed here.`;
    host.innerHTML = "";
    return;
  }

  note.innerHTML = `Credited to ${esc(ex.providers_used.join(", "))}.
    ${esc(ex.semantics.scope || "")}`;
  host.innerHTML = ex.contributions.map((c) => `
    <div class="binding">
      <div><strong>${esc(c.provider_suite)}</strong>
        <code>${esc(c.provider_tool)}</code>
        <span class="chip chip-external">${esc(c.action)}</span></div>
      ${kv([
        ["query", esc(c.query)],
        ["returned", c.result_count
          ? esc(c.retrieved.join(", "))
          : '<span class="chip chip-unresolved">nothing returned</span>'],
        ["subject", val(c.subject)],
        ["recorded", esc(c.recorded_at)],
        ["changes a packaged claim", String(c.changes_packaged_claim)],
      ])}
    </div>`).join("");
}

/* ------------------------------------------------------------ mechanism UI */

function renderMechanismMeta() {
  const v = state.view;
  el("mechanism-meta").innerHTML = `
    <code>${esc(v.transformation_id)}</code><br>
    set <code>${esc(v.transformation_set_id)}</code> &middot;
    ${esc(v.before_graph.atoms.length)} depiction nodes &middot;
    ${esc(v.edits.length)} reviewed edits &middot;
    replay status <code>${esc(v.status)}</code>`;

  el("replay-note").textContent = v.replay_semantics.note;
  el("layout-caveat").textContent =
    v.layout.semantics.note + " " + v.layout.semantics.union_bond_basis;

  const boundaries = (v.representation_boundaries || []).map((b) =>
    `<li>${esc(b.reason || JSON.stringify(b))}</li>`).join("");
  const abstentions = (v.abstentions || []).map((a) =>
    `<li>${esc(a.reason || JSON.stringify(a))}</li>`).join("");
  const scope = Object.entries(v.scope_effect || {}).map(([k, val_]) =>
    [k, esc(JSON.stringify(val_))]);

  el("replay-detail").innerHTML = `
    <h3 class="minor">Replay verification</h3>
    ${kv(Object.entries(v.replay || {})
        .filter(([k]) => k !== "atom_map")
        .map(([k, val_]) => [k, esc(JSON.stringify(val_))]))}
    <h3 class="minor">Representation boundaries</h3>
    <ul class="note">${boundaries || "<li>none recorded</li>"}</ul>
    <h3 class="minor">Mandatory abstentions</h3>
    <ul class="note">${abstentions || "<li>none recorded</li>"}</ul>
    <h3 class="minor">Scope effect</h3>
    ${kv(scope)}
    <h3 class="minor">Review</h3>
    ${kv(Object.entries(v.review || {}).map(([k, val_]) => [k, esc(JSON.stringify(val_))]))}
    <h3 class="minor">Source bindings</h3>
    <ul class="note">${(v.source_bindings || []).map((b) =>
      `<li><code>${esc(b.binding_id)}</code> &middot; ${esc(b.artifact_kind)}</li>`).join("")}</ul>`;
}

async function loadMechanism(mcsaId) {
  state.mcsaId = mcsaId;
  state.selectedAtom = null;
  state.selectedFragment = null;
  try {
    const [view, sites] = await Promise.all([
      getJSON(`/api/mechanism/${encodeURIComponent(mcsaId)}`),
      getJSON(`/api/sites/${encodeURIComponent(mcsaId)}`),
    ]);
    state.view = view;
    state.sites = sites;
    state.step = 0;
    renderMechanismMeta();
    renderReplayControls();
    drawGraph();
    renderFragments();
    renderInspector();
  } catch (err) {
    el("mechanism-meta").innerHTML = `<span class="err">${esc(err.message)}</span>`;
  }
}

async function loadEvidence() {
  const variant = el("variant-select").value;
  const endpoint = el("endpoint-select").value;
  try {
    const ev = await getJSON(
      `/api/evidence?variant=${encodeURIComponent(variant)}&endpoint=${encodeURIComponent(endpoint)}`);
    state.evidence = ev;
    // Keep the full endpoint list from the unfiltered query.
    if (!endpoint) state.endpointKinds = ev.endpoint_kinds;
    renderEvidence();
    renderFragments();
    renderInspector();
  } catch (err) {
    el("evidence-list").innerHTML = `<span class="err">${esc(err.message)}</span>`;
  }
}

/* -------------------------------------------------------------- patterns UI */

function renderClauses() {
  el("clause-rows").innerHTML = state.clauses.map((c, i) => {
    if (c.kind === "bond") {
      return `<div class="clause-row" data-i="${i}">
        <span class="tag">bond</span>
        <input data-f="e0" value="${esc(c.elements[0])}" size="2" aria-label="element 1">
        <input data-f="v0" value="${esc(c.variables[0])}" aria-label="variable 1">
        <input data-f="e1" value="${esc(c.elements[1])}" size="2" aria-label="element 2">
        <input data-f="v1" value="${esc(c.variables[1])}" aria-label="variable 2">
        order <input data-f="before" value="${esc(c.before)}" size="1">
        &#8594; <input data-f="after" value="${esc(c.after)}" size="1">
        <button class="rm" data-rm="${i}" title="remove">&times;</button>
      </div>`;
    }
    return `<div class="clause-row" data-i="${i}">
      <span class="tag">charge</span>
      <input data-f="e0" value="${esc(c.elements[0])}" size="2" aria-label="element">
      <input data-f="v0" value="${esc(c.variables[0])}" aria-label="variable">
      charge <input data-f="before" value="${esc(c.before)}" size="1">
      &#8594; <input data-f="after" value="${esc(c.after)}" size="1">
      <button class="rm" data-rm="${i}" title="remove">&times;</button>
    </div>`;
  }).join("");

  el("clause-rows").querySelectorAll("input").forEach((input) => {
    input.addEventListener("change", () => {
      const row = input.closest(".clause-row");
      const c = state.clauses[Number(row.dataset.i)];
      const f = input.dataset.f;
      if (f === "e0") c.elements[0] = input.value.trim();
      else if (f === "e1") c.elements[1] = input.value.trim();
      else if (f === "v0") c.variables[0] = input.value.trim();
      else if (f === "v1") c.variables[1] = input.value.trim();
      else c[f] = input.value.trim();
    });
  });
  el("clause-rows").querySelectorAll("[data-rm]").forEach((btn) =>
    btn.addEventListener("click", () => {
      state.clauses.splice(Number(btn.dataset.rm), 1);
      renderClauses();
    }));
}

const PRESETS = {
  shared: [
    { kind: "bond", elements: ["C", "C"], variables: ["x", "y"], before: 0, after: 1 },
    { kind: "charge", elements: ["C"], variables: ["x"], before: -1, after: 0 },
  ],
  disjoint: [
    { kind: "bond", elements: ["C", "O"], variables: ["x", "y"], before: 2, after: 1 },
    { kind: "charge", elements: ["C"], variables: ["x"], before: -1, after: 0 },
  ],
  symmetric: [
    { kind: "bond", elements: ["C", "C"], variables: ["x", "y"], before: 0, after: 1 },
  ],
};

async function runPattern() {
  const host = el("pattern-result");
  host.innerHTML = `<p class="note">running…</p>`;
  const clauses = state.clauses.map((c) => ({
    kind: c.kind,
    elements: c.elements.slice(0, c.kind === "bond" ? 2 : 1),
    variables: c.variables.slice(0, c.kind === "bond" ? 2 : 1),
    before: Number(c.before),
    after: Number(c.after),
  }));
  try {
    const res = await postJSON("/api/patterns", {
      clauses,
      mcsa_id: el("pattern-mcsa").value.trim() || null,
      support: el("support-select").value,
    });
    renderPatternResult(res);
  } catch (err) {
    host.innerHTML = `<p class="err">${esc(err.message)}</p>`;
  }
}

function renderPatternResult(res) {
  const bindings = [];
  (res.matches || []).forEach((m) => {
    const row = m.candidate_row || {};
    (m.bindings || []).forEach((b) => bindings.push({ row, b }));
  });

  /** Describe a clause in the same words the builder uses. */
  const clauseText = (c) => {
    const pair = (i) => `${c.elements[i]}:${c.variables[i]}`;
    return c.kind === "bond"
      ? `bond ${pair(0)} \u2013 ${pair(1)}, order ${c.before} \u2192 ${c.after}`
      : `charge on ${pair(0)}, ${c.before} \u2192 ${c.after}`;
  };

  const cards = bindings.map(({ row, b }) => {
    const assignment = Object.entries(b.atom_bindings || {})
      .map(([k, v]) => `<code>${esc(k)} = ${esc(v)}</code>`).join(", ");

    const rows = (b.clause_witnesses || []).map((w) => {
      const events = (w.events || []).map((e) => {
        const ids = ((e.source_edit || {}).atom_ids || []).join(" \u2013 ");
        return `<code>${esc(e.edit_id)}</code> on ${esc(ids)}`;
      }).join("<br>");
      return `<tr><td>${esc(clauseText(w.clause))}</td><td>${events}</td></tr>`;
    }).join("");

    const witnesses = rows
      ? `<table class="mini">
           <tr><th>clause</th><th>witness edit and source atoms</th></tr>${rows}
         </table>`
      : "";

    return `<div class="binding">
      <div><strong>${esc(row.candidate_id)}</strong></div>
      <div class="note">assignment: ${assignment}</div>
      ${witnesses}
      <p class="note">candidate sha256 <code>${esc(row.candidate_sha256)}</code></p>
    </div>`;
  }).join("");

  const empty = res.candidate_count === 0
    ? `<p class="empty-note">No match in the declared searched collection. This means the
        packaged candidate catalog contains no candidate satisfying every clause on the same
        named atoms. It does not mean the chemistry is absent in nature.</p>`
    : "";

  el("pattern-result").innerHTML = `
    <div class="result-head">
      <div><div class="count">${esc(res.candidate_count)}</div>
        <div class="count-label">candidates matched</div></div>
      <div><div class="count">${esc(res.binding_count)}</div>
        <div class="count-label">variable assignments</div></div>
      <div class="note">catalog <code>${esc(res.catalog_id)}</code>,
        status <span class="chip chip-unreviewed">${esc(res.status)}</span></div>
    </div>
    <p class="note">Binding counts are assignments, not mechanism counts; symmetry can raise
      the assignment count without adding evidence or a distinct reaction. A match does not
      promote any candidate's evidence status.</p>
    ${empty}
    ${cards}
    <details class="disclosure"><summary>Query semantics and catalog provenance</summary>
      ${kv(Object.entries(res.query_semantics || {}).map(([k, v]) => [k, esc(JSON.stringify(v))]))}
      ${kv([["catalog sha256", esc(res.catalog_sha256)],
            ["schema", esc(res.schema_version)],
            ["filters", esc(JSON.stringify(res.filters))]])}
    </details>`;
}

/* ------------------------------------------------------------------- init */

function initTabs() {
  document.querySelectorAll(".tab").forEach((tab) =>
    tab.addEventListener("click", () => {
      document.querySelectorAll(".tab").forEach((t) => t.classList.remove("is-active"));
      document.querySelectorAll(".tabpanel").forEach((p) => p.classList.remove("is-active"));
      tab.classList.add("is-active");
      el("tab-" + tab.dataset.tab).classList.add("is-active");
    }));
}

async function init() {
  initTabs();

  el("btn-before").addEventListener("click", () => setStep(0));
  el("btn-after").addEventListener("click", () => setStep(state.view.edits.length));
  el("btn-step-back").addEventListener("click", () => setStep(state.step - 1));
  el("btn-step-fwd").addEventListener("click", () => setStep(state.step + 1));

  el("variant-select").addEventListener("change", loadEvidence);
  el("endpoint-select").addEventListener("change", loadEvidence);

  el("add-bond").addEventListener("click", () => {
    state.clauses.push({ kind: "bond", elements: ["C", "C"], variables: ["x", "y"], before: 0, after: 1 });
    renderClauses();
  });
  el("add-charge").addEventListener("click", () => {
    state.clauses.push({ kind: "charge", elements: ["C"], variables: ["x"], before: -1, after: 0 });
    renderClauses();
  });
  el("run-pattern").addEventListener("click", runPattern);
  document.querySelectorAll("[data-preset]").forEach((btn) =>
    btn.addEventListener("click", () => {
      state.clauses = JSON.parse(JSON.stringify(PRESETS[btn.dataset.preset]));
      renderClauses();
      runPattern();
    }));

  state.clauses = JSON.parse(JSON.stringify(PRESETS.shared));
  renderClauses();

  try {
    state.external = await getJSON("/api/external-sources");
    renderExternal();
  } catch (err) {
    el("external-note").innerHTML = `<span class="err">${esc(err.message)}</span>`;
  }

  const { mechanisms } = await getJSON("/api/mechanisms");
  el("mechanism-select").innerHTML = mechanisms.map((m) =>
    `<option value="${esc(m.mcsa_id)}">${esc(m.mcsa_id)} — ${esc(m.short_name)}</option>`).join("");
  el("mechanism-select").addEventListener("change", (e) => loadMechanism(e.target.value));

  await loadMechanism(mechanisms[0].mcsa_id);
  await loadEvidence();
}

init();
