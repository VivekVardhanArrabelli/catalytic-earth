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
  // A stable relation id, never a relation object: the objects are replaced on
  // every evidence fetch, so holding one would pin stale observations.
  selectedFragmentId: null,
  clauses: [],
  // Monotonic request generations. A response is installed only if it belongs
  // to the newest request, so a slow earlier reply cannot overwrite a later
  // selection.
  // The filters of the last evidence result actually on screen, so a failed
  // load can put the controls back in agreement with what is displayed.
  loadedFilters: { variant: "", endpoint: "" },
  mechanismRequest: 0,
  evidenceRequest: 0,
  patternRequest: 0,
  chem: null,
  chemRequest: 0,
  // The complete query a displayed result came from: its clauses, its filters
  // and the generation that produced it. Chemistry is opened from this, never
  // from control values that may have been edited without re-running.
  acceptedQuery: null,
  guided: false,
  guidedDone: {},
};

/** The selected relation, re-resolved against the current evidence result. */
function selectedFragment() {
  if (!state.selectedFragmentId || !state.evidence) return null;
  return (state.evidence.relations || []).find(
    (r) => r.relation_id === state.selectedFragmentId) || null;
}

/* ----------------------------------------------------------------- utils */
const el = (id) => document.getElementById(id);
const esc = (v) =>
  String(v === null || v === undefined ? "" : v).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

/**
 * Display wording for a packaged enumeration value.
 *
 * Presentation only: the underlying value is never rewritten, every raw field
 * stays visible in the expert disclosures, and an unrecognised value is shown
 * exactly as it arrived rather than guessed at.
 */
const PHRASE = {
  not_detected: "Not detected",
  no_detectable_difference: "No detectable difference",
  measured: "Measured",
  isotope_exchange: "Proton exchange with solvent",
  turnover: "Turnover",
  structure: "Reported structure comparison",
  after_graph_confirmed: "Confirmed by the source after-graph",
  source_arrow_only: "Source arrow only, not after-graph confirmed",
  literature_lookup: "Literature lookup",
  database_lookup: "Database lookup",
  structure_view: "Structure view",
};
const phrase = (value) =>
  Object.prototype.hasOwnProperty.call(PHRASE, value) ? PHRASE[value] : value;

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

/** Show or clear a failure notice without destroying the content below it. */
function notice(id, message) {
  const node = el(id);
  node.textContent = message || "";
  node.hidden = !message;
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

  const chosen = selectedFragment();
  const fragmentAtoms = new Set(chosen ? chosen.atoms.map((a) => a.atom_id) : []);

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
      state.selectedFragmentId = null;
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
      const sel = state.selectedFragmentId === r.relation_id ? " is-selected" : "";
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
      const wasSelected = state.selectedFragmentId === r.relation_id;
      state.selectedFragmentId = wasSelected ? null : r.relation_id;
      state.selectedAtom = wasSelected ? null : r.source_atom_id;
      drawGraph(); renderFragments(); renderInspector();
    }));
  host.querySelectorAll("[data-site-atom]").forEach((btn) =>
    btn.addEventListener("click", () => {
      const id = btn.dataset.siteAtom;
      state.selectedAtom = state.selectedAtom === id ? null : id;
      state.selectedFragmentId = null;
      drawGraph(); renderFragments(); renderInspector();
    }));
}

/**
 * Describe the external contributions recorded for one subject, restricted to
 * a given action. The action is read from the record, never inferred from the
 * subject, and a call that returned nothing is described as returning nothing.
 */
function contributionBadge(subject, action, label) {
  const entries = (((state.external || {}).contributions_by_subject) || {})[subject] || [];
  const matching = entries.filter((e) => e.action === action);
  if (!matching.length) return "";
  return matching.map((e) => {
    const empty = e.result_count === 0 ? ", returned nothing" : "";
    return ` <span class="chip chip-external">${esc(label)}: ${esc(e.provider_suite)}
      <code>${esc(e.provider_tool)}</code>${esc(empty)}</span>`;
  }).join("");
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
  // recorded against its accession. Any other action on the same accession is
  // reported as that action, never as a structure view.
  const structures = (ctx.structures || []).map((s) => {
    const subject = `PDB:${s.pdb_id}`;
    const viewed = contributionBadge(subject, "structure_view", "structure view")
      + contributionBadge(subject, "database_lookup", "database lookup")
      + contributionBadge(subject, "literature_lookup", "literature lookup");
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
    // Phrased for reading; the raw relation stays beside it.
    const relation = String(r.reported_relation || "");
    const phrased = relation === "fold_lower_than_wild_type"
      ? `Reported ${esc(r.value)}-fold lower than WT`
      : `${esc(r.value)} ${esc(r.unit)}, reported as ${esc(relation)}`;
    resultText = `<strong>${phrased}</strong>
      <code>${esc(relation)}</code> versus
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

  const badged = new Set();
  const witnesses = (o.source_witnesses || []).map((w) => {
    // Mark an external contribution only where one was actually recorded for
    // this evidence id, naming the action it was, and once per observation
    // rather than once per quotation.
    let badge = "";
    if (!badged.has(w.evidence_id)) {
      badge = contributionBadge(w.evidence_id, "literature_lookup", "literature lookup")
        + contributionBadge(w.evidence_id, "database_lookup", "database lookup")
        + contributionBadge(w.evidence_id, "structure_view", "structure view");
      if (badge) badged.add(w.evidence_id);
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

  const variantId = (o.variant || {}).variant_id;
  return `<div class="obs ${cls}">
    <div class="obs-head">
      <span class="obs-title">${variantId ? `<code>${esc(variantId)}</code> ` : ""}${esc(ep.name || ep.kind)}${
        sub.name ? ` &middot; ${esc(sub.enantiomer ? sub.enantiomer + "-" : "")}${esc(sub.name)}` : ""}</span>
      ${chip}
    </div>
    <div class="obs-result">${resultText}</div>
    <p class="note">${esc(phrase(ep.kind))} <code>${esc(ep.kind)}</code>
      &middot; conditions: ${conditions}
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
  // Re-resolved every render: a relation object from an earlier response would
  // keep showing that response's observations after the filters changed.
  const frag = selectedFragment();
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

  // Selectors list exactly what the packaged evidence contains, so no part of
  // the evidence set can be hidden by a stale hand-written list.
  const available = ev.available || {};
  const fill = (id, values, allLabel) => {
    const select = el(id);
    const current = select.value;
    select.innerHTML = `<option value="">${allLabel}</option>` +
      (values || []).map((v) =>
        `<option value="${esc(v)}"${v === current ? " selected" : ""}>${esc(v)}</option>`).join("");
  };
  fill("endpoint-select", available.endpoint_kinds, "all endpoints");
  fill("variant-select", available.variants, "all variants");

  el("abstention-strip").innerHTML = (ev.abstentions || []).length
    ? `<p class="note"><strong>${esc(ev.abstentions.length)} mandatory abstentions</strong>
         apply to these observations. They are part of the packaged record.</p>` +
      (ev.abstentions || []).map((a) => `
        <details class="abstention">
          <summary>${esc(a.abstention_id || "abstention")}</summary>
          <p class="note">${esc(a.reason || JSON.stringify(a))}</p>
        </details>`).join("")
    : "";

  const filters = [];
  if ((ev.filters || {}).variant) filters.push(`variant ${esc(ev.filters.variant)}`);
  if ((ev.filters || {}).endpoint) filters.push(`endpoint ${esc(ev.filters.endpoint)}`);
  el("evidence-note").innerHTML = `
    Evidence set <code>${esc(ev.evidence_set_id)}</code> &middot;
    ${filters.length ? `filtered by ${filters.join(" and ")}` : "no filter"} &middot;
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
        <span class="chip chip-external">${esc(phrase(c.action))}</span>
        ${c.result ? matchChip(c.result.match_status) : ""}</div>
      ${kv([
        ["query", esc(c.query)],
        ["subject", val(c.subject)],
        ["recorded", esc(c.recorded_at)],
        ["changes a packaged claim", String(c.changes_packaged_claim)],
      ])}
      ${c.result ? renderResult(c.result) : `<p class="note">
        No output has been returned for this request yet.</p>`}
    </div>`).join("");
}

/** How a declared association compares with the packaged record. */
function matchChip(status) {
  const label = {
    confirmed: "association confirmed",
    conflict: "association conflict",
    unresolved: "association unresolved",
  }[status] || status;
  const style = status === "confirmed" ? "chip chip-measured"
    : status === "conflict" ? "chip chip-nondetect" : "chip chip-unresolved";
  return `<span class="${style}">${esc(label)}</span>`;
}

/**
 * Render one returned external result.
 *
 * Shows the scientific context the tool reported and the files it saved, not
 * just that something happened. A conflict or an unresolved association is
 * shown as such; neither is presented as a match, and none of this is merged
 * into the packaged record beside it.
 */
function renderResult(result) {
  const a = result.association || {};
  const checks = (a.checks || []).map((c) => `
    <tr><td>${esc(c.label)}</td>
        <td>${esc(c.declared || "not declared")}</td>
        <td>${matchChip(c.status)}</td>
        <td>${esc(c.reason || "")}</td></tr>`).join("");

  const context = Object.entries(result.context || {});
  const artifacts = (result.artifacts || []).map((f) => `
    <tr><td>${esc(f.name)}</td>
        <td>${esc(f.media_type)}</td>
        <td>${esc(f.bytes)} bytes</td>
        <td><code>${esc(String(f.sha256).slice(0, 16))}…</code></td></tr>`).join("");

  return `
    <h3 class="minor">Returned scientific context</h3>
    ${context.length
      ? `<table class="mini"><tr><th>field</th><th>as the tool reported it</th></tr>
         ${context.map(([k, v]) =>
           `<tr><td>${esc(k)}</td><td>${esc(v)}</td></tr>`).join("")}</table>`
      : `<p class="note">The output reported no structured field.</p>`}

    <h3 class="minor">Saved artifacts</h3>
    <table class="mini">
      <tr><th>file</th><th>type</th><th>size</th><th>sha256</th></tr>${artifacts}
    </table>

    <h3 class="minor">Association with the packaged record</h3>
    <p class="note">Case <code>${esc(a.case_ref)}</code>
      ${a.case_resolved
        ? `resolved as <code>${esc(a.case_kind)}</code>`
        : '<span class="chip chip-unresolved">not resolved</span>'}.
      ${a.packaged_question ? esc(String(a.packaged_question).slice(0, 220)) : ""}</p>
    <table class="mini">
      <tr><th>field</th><th>declared</th><th>status</th><th>reason</th></tr>${checks}
    </table>
    <p class="caveat">${esc((result.semantics || {}).separation || "")}
      ${esc((result.semantics || {}).conflicts || "")}</p>`;
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

  // Shortened on screen; the full statement remains in the replay disclosure.
  el("replay-note").textContent =
    "Symbolic replay of a published source proposal. Not a molecular trajectory.";
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
  // A slow earlier request must never install its mechanism over a later
  // selection, which would show one mechanism's graph under another's name.
  const seq = ++state.mechanismRequest;
  const stale = () => seq !== state.mechanismRequest;

  el("mechanism-meta").innerHTML = `<span class="note">loading ${esc(mcsaId)}…</span>`;
  try {
    const [view, sites] = await Promise.all([
      getJSON(`/api/mechanism/${encodeURIComponent(mcsaId)}`),
      getJSON(`/api/sites/${encodeURIComponent(mcsaId)}`),
    ]);
    if (stale()) return;
    notice("mechanism-notice", "");
    // Selection and results commit together, for this request only.
    state.mcsaId = mcsaId;
    state.selectedAtom = null;
    state.selectedFragmentId = null;
    state.view = view;
    state.sites = sites;
    state.step = 0;
    renderMechanismMeta();
    renderReplayControls();
    drawGraph();
    renderFragments();
    renderInspector();
  } catch (err) {
    if (stale()) return;
    // The request failed, so nothing new is on screen. Put the control back in
    // agreement with the mechanism that is actually displayed, and say so.
    if (state.view && state.mcsaId) {
      el("mechanism-select").value = state.mcsaId;
      renderMechanismMeta();
      notice(
        "mechanism-notice",
        `Could not load ${mcsaId}: ${err.message}. Selection restored to ` +
        `${state.mcsaId}, which is what is shown below.`);
    } else {
      state.view = null;
      state.sites = null;
      el("graph").innerHTML = "";
      el("edit-list").innerHTML = "";
      el("mechanism-meta").innerHTML = "";
      el("replay-detail").innerHTML = "";
      el("fragment-list").innerHTML = "";
      el("inspector-body").innerHTML = "";
      notice("mechanism-notice",
        `Could not load ${mcsaId}: ${err.message}. No mechanism is loaded.`);
    }
  }
}

async function loadEvidence() {
  const variant = el("variant-select").value;
  const endpoint = el("endpoint-select").value;
  const seq = ++state.evidenceRequest;
  const stale = () => seq !== state.evidenceRequest;
  try {
    const ev = await getJSON(
      `/api/evidence?variant=${encodeURIComponent(variant)}&endpoint=${encodeURIComponent(endpoint)}`);
    if (stale()) return;
    notice("evidence-notice", "");
    state.evidence = ev;
    state.loadedFilters = { variant, endpoint };
    // Drop a selection the new result no longer supports, rather than leaving
    // the inspector showing a relation that is not in this result.
    if (state.selectedFragmentId &&
        !(ev.relations || []).some((r) => r.relation_id === state.selectedFragmentId)) {
      state.selectedFragmentId = null;
    }
    renderEvidence();
    renderFragments();
    renderInspector();
    drawGraph();
  } catch (err) {
    if (stale()) return;
    // Put the filters back to the result that is actually on screen, so the
    // controls, the observation list and the inspector describe one state.
    if (state.evidence) {
      el("variant-select").value = state.loadedFilters.variant;
      el("endpoint-select").value = state.loadedFilters.endpoint;
      renderEvidence();
      renderFragments();
      renderInspector();
      drawGraph();
      const describe = (f) =>
        [f.variant ? `variant ${f.variant}` : "", f.endpoint ? `endpoint ${f.endpoint}` : ""]
          .filter(Boolean).join(" and ") || "no filter";
      notice(
        "evidence-notice",
        `Could not load that evidence filter: ${err.message}. Filters restored ` +
        `to ${describe(state.loadedFilters)}, which is what is shown below.`);
    } else {
      el("evidence-list").innerHTML = "";
      el("abstention-strip").innerHTML = "";
      el("evidence-note").innerHTML = "";
      notice("evidence-notice",
        `Could not load evidence: ${err.message}. No evidence is loaded.`);
    }
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

/**
 * Read a bond order or formal charge exactly as typed.
 * A blank, fractional or malformed entry is refused, never coerced: rounding
 * it would quietly search for a different chemical constraint.
 */
function clauseInteger(raw) {
  const text = String(raw === null || raw === undefined ? "" : raw).trim();
  if (!/^-?(0|[1-9][0-9]*)$/.test(text)) return null;
  return Number(text);
}

async function runPattern() {
  const host = el("pattern-result");
  // Advance the generation for every attempt, including one that never
  // reaches the network. A refusal must retire any request still in flight,
  // otherwise that older response lands on top of the refusal message.
  const seq = ++state.patternRequest;
  const stale = () => seq !== state.patternRequest;
  // Every attempt, valid or not, retires the displayed result and any
  // chemistry opened from it, so a stale panel cannot sit under a new result.
  state.acceptedQuery = null;
  state.chem = null;
  state.chemRequest += 1;
  const openChem = el("chem-view");
  if (openChem) openChem.innerHTML = "";

  const clauses = [];
  const invalid = [];
  state.clauses.forEach((c, i) => {
    const width = c.kind === "bond" ? 2 : 1;
    const before = clauseInteger(c.before);
    const after = clauseInteger(c.after);
    if (before === null) invalid.push(`clause ${i + 1}: "${c.before}" is not an integer`);
    if (after === null) invalid.push(`clause ${i + 1}: "${c.after}" is not an integer`);
    clauses.push({
      kind: c.kind,
      elements: c.elements.slice(0, width),
      variables: c.variables.slice(0, width),
      before,
      after,
    });
  });
  if (invalid.length) {
    host.innerHTML = `<p class="err">Query not run. Values are used exactly as
      written and are never rounded.<br>${invalid.map(esc).join("<br>")}</p>`;
    return;
  }

  host.innerHTML = `<p class="note">running…</p>`;
  const mcsaId = el("pattern-mcsa").value.trim() || null;
  const support = el("support-select").value;
  try {
    const res = await postJSON("/api/patterns", {
      clauses,
      mcsa_id: mcsaId,
      support,
    });
    if (stale()) return;
    // The exact accepted query, captured with the result it produced.
    state.acceptedQuery = {
      clauses,
      mcsa_id: mcsaId,
      support,
      generation: seq,
    };
    renderPatternResult(res);
  } catch (err) {
    if (stale()) return;
    host.innerHTML = `<p class="err">${esc(err.message)}</p>`;
  }
}

function renderPatternResult(res) {
  const bindings = [];
  (res.matches || []).forEach((m) => {
    const row = m.candidate_row || {};
    (m.bindings || []).forEach((b, i) => bindings.push({ row, b, i }));
  });

  /** Describe a clause in the same words the builder uses. */
  const clauseText = (c) => {
    const pair = (i) => `${c.elements[i]}:${c.variables[i]}`;
    return c.kind === "bond"
      ? `bond ${pair(0)} \u2013 ${pair(1)}, order ${c.before} \u2192 ${c.after}`
      : `charge on ${pair(0)}, ${c.before} \u2192 ${c.after}`;
  };

  const cards = bindings.map(({ row, b, i: index }) => {
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
      <div class="gs-actions">
        <button class="pill pill-primary" data-chem="${esc(row.candidate_id)}"
          data-chem-index="${esc(index)}">View matched chemistry</button>
      </div>
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
    <div id="chem-view" class="chem-view"></div>
    <details class="disclosure"><summary>Query semantics and catalog provenance</summary>
      ${kv(Object.entries(res.query_semantics || {}).map(([k, v]) => [k, esc(JSON.stringify(v))]))}
      ${kv([["catalog sha256", esc(res.catalog_sha256)],
            ["schema", esc(res.schema_version)],
            ["filters", esc(JSON.stringify(res.filters))]])}
    </details>`;

  el("pattern-result").querySelectorAll("[data-chem]").forEach((btn) =>
    btn.addEventListener("click", () =>
      viewMatchedChemistry(btn.dataset.chem, Number(btn.dataset.chemIndex))));
}



/* ------------------------------------------------- matched chemistry viewer */

/**
 * Draw one retained source panel.
 *
 * Coordinates are the retained source depiction values returned by the query.
 * Nothing is laid out or invented here: an atom the record does not place is
 * listed as unplaced rather than drawn at a guessed position.
 */
function drawPanel(panel, opts) {
  const { bound, witnessAtoms, editAtoms, witnessBonds, title } = opts;
  const ids = Object.keys(panel.coordinates);
  if (!ids.length) {
    return `<div class="panel"><h4>${esc(title)}</h4>
      <p class="note">This panel retains no depiction coordinates, so it is not
      drawn. Its ${esc(panel.atoms.length)} atoms remain listed in the record.</p></div>`;
  }
  const xs = ids.map((i) => panel.coordinates[i][0]);
  const ys = ids.map((i) => panel.coordinates[i][1]);
  const pad = 1.2;
  const minX = Math.min(...xs) - pad, maxX = Math.max(...xs) + pad;
  const minY = Math.min(...ys) - pad, maxY = Math.max(...ys) + pad;
  // Source depiction y grows upward; SVG y grows downward.
  const fy = (y) => maxY + minY - y;

  const bonds = panel.bonds.map((b) => {
    const [a1, a2] = b.atom_ids;
    const p1 = panel.coordinates[a1], p2 = panel.coordinates[a2];
    if (!p1 || !p2) return "";
    const dx = p2[0] - p1[0], dy = fy(p2[1]) - fy(p1[1]);
    const len = Math.hypot(dx, dy) || 1;
    const ox = (-dy / len) * 0.09, oy = (dx / len) * 0.09;
    const offsets = b.order >= 3 ? [-1, 0, 1] : b.order === 2 ? [-0.6, 0.6] : [0];
    // A bond is a witness only when a bond edit names this exact pair. Two
    // charge edits on connected atoms do not make the bond between them a
    // witness, and inferring one would show an edge that never changed.
    const witness = witnessBonds.has(bondKey([a1, a2]));
    return offsets.map((m) => `<line class="bond${witness ? " is-order" : ""}"
      x1="${p1[0] + ox * m}" y1="${fy(p1[1]) + oy * m}"
      x2="${p2[0] + ox * m}" y2="${fy(p2[1]) + oy * m}"
      vector-effect="non-scaling-stroke" stroke-width="${witness ? 3 : 1.4}"/>`).join("");
  }).join("");

  const atoms = panel.atoms.map((a) => {
    const pos = panel.coordinates[a.atom_id];
    if (!pos) return "";
    const role = bound[a.atom_id]
      ? "is-bound" : witnessAtoms.has(a.atom_id)
      ? "is-witness" : editAtoms.has(a.atom_id) ? "is-edit" : "";
    const q = a.formal_charge;
    const label = a.element + (q ? (q > 0 ? "+".repeat(q) : "−".repeat(-q)) : "");
    return `<g class="patom ${role}" transform="translate(${pos[0]},${fy(pos[1])})">
      <circle r="${bound[a.atom_id] ? 0.62 : 0.42}" vector-effect="non-scaling-stroke"/>
      <text text-anchor="middle" dy="0.13" style="font-size:0.4px">${esc(label)}</text>
      ${bound[a.atom_id]
        ? `<text class="bvar" text-anchor="middle" dy="-0.95"
             style="font-size:0.8px">${esc(bound[a.atom_id])}=${esc(a.atom_id)}</text>` : ""}
    </g>`;
  }).join("");

  return `<div class="panel">
    <h4>${esc(title)}</h4>
    <svg viewBox="${minX} ${minY} ${maxX - minX} ${maxY - minY}" class="panel-svg">
      <g>${bonds}</g><g>${atoms}</g>
    </svg>
    ${panel.unplaced_atom_ids.length
      ? `<p class="caveat">${esc(panel.unplaced_atom_ids.length)} atoms carry no
         retained coordinate and are not drawn:
         ${esc(panel.unplaced_atom_ids.join(", "))}.</p>` : ""}
  </div>`;
}

async function viewMatchedChemistry(candidateId, bindingIndex) {
  const host = el("chem-view");
  const query = state.acceptedQuery;
  if (!query) {
    host.innerHTML = `<p class="err">These results are no longer current.
      Run the query again before inspecting a match.</p>`;
    return;
  }
  host.innerHTML = `<p class="note">loading the retained panels…</p>`;
  host.scrollIntoView({ behavior: "smooth", block: "nearest" });
  const seq = ++state.chemRequest;
  // Valid only while both this request and the result it belongs to are
  // current: a newer search must be able to retire an in-flight inspection.
  const stale = () =>
    seq !== state.chemRequest ||
    state.acceptedQuery !== query ||
    query.generation !== state.patternRequest;
  try {
    const view = await postJSON("/api/match-chemistry", {
      clauses: query.clauses,
      candidate_id: candidateId,
      binding_index: bindingIndex,
      mcsa_id: query.mcsa_id,
      support: query.support,
    });
    if (stale()) return;
    state.chem = view;
    renderMatchedChemistry();
  } catch (err) {
    if (stale()) return;
    host.innerHTML = `<p class="err">${esc(err.message)}</p>`;
  }
}

function renderMatchedChemistry() {
  const v = state.chem;
  if (!v) return;
  const bound = {};
  Object.entries(v.assignment.atom_bindings).forEach(([k, id]) => { bound[id] = k; });

  const witnessAtoms = new Set();
  const witnessBonds = new Set();
  v.clause_witnesses.forEach((w) =>
    w.edits.forEach((e) => {
      const ids = e.atom_ids || [];
      ids.forEach((id) => witnessAtoms.add(id));
      // Only an edit that acts on a bond contributes a witness bond.
      if (ids.length === 2 && String(e.operation || "").includes("bond")) {
        witnessBonds.add(bondKey(ids));
      }
    }));
  const editAtoms = new Set();
  v.edits.forEach((e) => (e.atom_ids || []).forEach((id) => editAtoms.add(id)));

  // Edit ids are before-panel locators. The after panel is annotated through
  // the retained correspondence, never by assuming the ids match. An atom the
  // correspondence does not map is left unannotated rather than guessed.
  const toAfter = new Map(
    ((v.correspondence || {}).atom_map || [])
      .filter((m) => m.before_atom_id && m.after_atom_id)
      .map((m) => [m.before_atom_id, m.after_atom_id]));
  const project = (ids) => {
    const out = new Set();
    ids.forEach((id) => { if (toAfter.has(id)) out.add(toAfter.get(id)); });
    return out;
  };
  const afterBound = {};
  Object.entries(bound).forEach(([id, name]) => {
    if (toAfter.has(id)) afterBound[toAfter.get(id)] = name;
  });
  const afterWitnessBonds = new Set();
  witnessBonds.forEach((key) => {
    const [a, b] = key.split("~");
    if (toAfter.has(a) && toAfter.has(b)) {
      afterWitnessBonds.add(bondKey([toAfter.get(a), toAfter.get(b)]));
    }
  });
  const unmappedBound = Object.keys(bound).filter((id) => !toAfter.has(id));

  const clauseRows = v.clause_witnesses.map((w) => {
    const c = w.clause;
    const text = c.kind === "bond"
      ? `bond ${c.elements[0]}:${c.variables[0]} – ${c.elements[1]}:${c.variables[1]}, order ${c.before} → ${c.after}`
      : `charge on ${c.elements[0]}:${c.variables[0]}, ${c.before} → ${c.after}`;
    const edits = w.edits.map((e) => `<code>${esc(e.edit_id)}</code> on
      ${esc((e.atom_ids || []).join(" – "))}
      <span class="${e.support === "after_graph_confirmed"
        ? "chip chip-confirmed" : "chip chip-unreviewed"}"
        >${esc(phrase(e.support))}</span> <code>${esc(e.support)}</code>`).join("<br>");
    return `<tr><td>${esc(text)}</td><td>${edits}</td></tr>`;
  }).join("");

  const others = v.edits.filter((e) => !e.is_witness);
  const assignments = v.assignment.of > 1
    ? `<div class="gs-actions">${Array.from({ length: v.assignment.of }, (_, i) =>
        `<button class="pill ${i === v.assignment.index ? "pill-primary" : ""}"
          data-binding="${i}">assignment ${i + 1}</button>`).join("")}</div>
       <p class="note">${esc(v.assignment_semantics.note)}</p>` : "";

  el("chem-view").innerHTML = `
    <div class="card-head">
      <h3>Matched chemistry</h3>
      <span class="chip chip-unreviewed">${esc(v.provenance.review_status)} candidate</span>
    </div>
    <p class="note"><code>${esc(v.candidate_id)}</code> &middot; assignment
      ${esc(v.assignment.index + 1)} of ${esc(v.assignment.of)}:
      ${Object.entries(v.assignment.atom_bindings).map(([k, id]) =>
        `<code>${esc(k)} = ${esc(id)}</code>`).join(", ")}</p>
    <p class="caveat">${esc(v.provenance.not_a_reviewed_transformation)}</p>
    ${assignments}
    <div class="panels">
      ${drawPanel(v.panels.before, {
        bound, witnessAtoms, editAtoms, witnessBonds, title: "Before panel" })}
      ${drawPanel(v.panels.after, {
        bound: afterBound,
        witnessAtoms: project(witnessAtoms),
        editAtoms: project(editAtoms),
        witnessBonds: afterWitnessBonds,
        title: "After panel" })}
    </div>
    <p class="note"><span class="swatch sw-bound"></span> atom bound to a query
      variable &middot; <span class="swatch sw-witness"></span> atom or bond in an
      edit that satisfies a clause &middot; <span class="swatch sw-edit"></span>
      atom in another proposed edit</p>
    ${unmappedBound.length
      ? `<p class="caveat">${esc(unmappedBound.join(", "))} has no retained
         correspondence to the after panel and is left unmarked there.</p>` : ""}
    <p class="note">After-panel marks are placed through the retained
      correspondence (<code>${esc((v.correspondence || {}).method)}</code>),
      not by matching identifier strings across panels.</p>
    <p class="caveat">${esc(v.panels.before.coordinate_semantics.note)}</p>
    <h3 class="minor">Which edits satisfy each clause</h3>
    <table class="mini"><tr><th>clause</th><th>witness edit and support</th></tr>
      ${clauseRows}</table>
    <h3 class="minor">Other proposed edits in this candidate (${esc(others.length)})</h3>
    <ul class="note">${others.map((e) =>
      `<li>${esc(e.label)} <span class="${e.after_graph_verified
        ? "chip chip-confirmed" : "chip chip-unreviewed"}">${esc(e.support)}</span></li>`).join("")}</ul>
    <details class="disclosure">
      <summary>Correspondence, coverage, opaque context and scope</summary>
      ${kv([
        ["correspondence method", esc(v.correspondence.method)],
        ["correspondence meaning", esc(v.correspondence.interpretation)],
        ["mapped nodes", `${esc(v.coverage.mapped_node_count)} of
           ${esc(v.coverage.before_node_count)} before /
           ${esc(v.coverage.after_node_count)} after`],
        ["full covalent replay asserted",
          String(v.coverage.full_covalent_graph_replay_asserted)],
        ["after-graph unverified edits",
          esc((v.coverage.after_graph_unverified_edit_ids || []).join(", ") || "none")],
        ["support counts", esc(JSON.stringify(v.support_counts))],
        ["candidate sha256", esc(v.candidate_sha256)],
      ])}
      ${kv(Object.entries(v.scope_effect).map(([k, val_]) => [k, esc(JSON.stringify(val_))]))}
    </details>`;

  el("chem-view").querySelectorAll("[data-binding]").forEach((btn) =>
    btn.addEventListener("click", () =>
      viewMatchedChemistry(v.candidate_id, Number(btn.dataset.binding))));
}

/* ------------------------------------------------------------- guided path */

/**
 * An optional ordered path through the existing controls and queries.
 *
 * Every step drives the ordinary interface: it changes selectors, runs the
 * same backend queries and updates the same panels. Nothing here is a
 * precomputed narrative, and no value below is written by hand. The question,
 * the alternatives, the adjudication, the observations and the residue link
 * are all read out of the live query results.
 */

/** The relation the packaged evidence actually supports for the focal site. */
function focalRelation() {
  const relations = (state.evidence || {}).relations || [];
  return relations.find(
    (r) => r.site_id && r.functional_evidence.matched_observations.length) || null;
}

/** The variant those bound observations belong to, read from the data. */
function focalVariant() {
  const relation = focalRelation();
  const bound = relation ? relation.functional_evidence.matched_observations : [];
  const ids = [...new Set(bound.map((o) => (o.variant || {}).variant_id).filter(Boolean))];
  return ids.length === 1 ? ids[0] : null;
}

/** The mechanism this case is bound to, taken from the record, never assumed. */
function guidedMechanismId() {
  const kase = ((state.evidence || {}).cases || [])[0] || {};
  const fromCase = (kase.transformation_binding || {}).mcsa_id;
  if (fromCase) return fromCase;
  const relation = focalRelation();
  return (((relation || {}).transformation_context || {}).binding || {}).mcsa_id || null;
}

/**
 * Load the case's own mechanism before a step that depends on it.
 * Returns false when it cannot be loaded, so the caller stops rather than
 * showing one case's residue against another case's graph.
 */
async function guidedEnsureMechanism() {
  const wanted = guidedMechanismId();
  if (!wanted) return false;
  if (state.mcsaId === wanted && state.view) return true;
  const option = el("mechanism-select").querySelector(`[value="${wanted}"]`);
  if (!option) return false;
  el("mechanism-select").value = wanted;
  await loadMechanism(wanted);
  return state.mcsaId === wanted && Boolean(state.view);
}

const GUIDED_STEPS = [
  {
    id: "question",
    title: "Open the research question",
    hint: "Shows the question and adjudication this case actually records.",
    actions: [{ label: "Show the question", run: guidedQuestion }],
  },
  {
    id: "replay",
    title: "Inspect the proposed step",
    hint: "Loads the source proposal and its before and after graph state.",
    actions: [
      { label: "Show the before panel", run: () => guidedReplay(0) },
      { label: "Show the after panel", run: () => guidedReplay(-1) },
    ],
  },
  {
    id: "residue",
    title: "Show the supported residue link",
    hint: "Selects the supported source fragment by its own relation id.",
    actions: [{ label: "Select the supported fragment", run: guidedResidue }],
  },
  {
    id: "endpoints",
    title: "Compare the reported endpoints",
    hint: "Puts the focal variant's endpoints side by side, with their conditions.",
    actions: [{ label: "Compare the endpoints", run: guidedEndpoints }],
  },
  {
    id: "structure",
    title: "Prepare the reference structure inspection",
    hint: "Collects the supported site and structure context for a real session.",
    actions: [{ label: "Prepare the request", run: guidedStructure }],
  },
];

function renderGuided() {
  el("guided").hidden = !state.guided;
  el("guided-toggle").classList.toggle("is-active", state.guided);
  if (!state.guided) return;
  el("guided-steps").innerHTML = GUIDED_STEPS.map((s, i) => `
    <li class="${state.guidedDone[s.id] ? "is-done" : ""}">
      <div class="gs-body">
        <div class="gs-title">${esc(s.title)}</div>
        <div class="gs-hint">${esc(s.hint)}</div>
        <div class="gs-actions">${s.actions.map((a, j) =>
          `<button class="pill" data-gs="${i}" data-ga="${j}">${esc(a.label)}</button>`).join("")}</div>
      </div>
    </li>`).join("");
  el("guided-steps").querySelectorAll("[data-gs]").forEach((btn) =>
    btn.addEventListener("click", async () => {
      const step = GUIDED_STEPS[Number(btn.dataset.gs)];
      // Marked done only when the action reports success. An unsupported
      // relation or a failed prerequisite load must not read as completed.
      let ok = false;
      try {
        ok = (await step.actions[Number(btn.dataset.ga)].run()) === true;
      } catch (err) {
        guidedDetail(`<p class="err">${esc(err.message)}</p>`);
      }
      state.guidedDone[step.id] = ok;
      renderGuided();
    }));
}

function guidedDetail(html) {
  el("guided-detail").innerHTML = html;
  el("guided-detail").scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function guidedQuestion() {
  const kase = ((state.evidence || {}).cases || [])[0];
  if (!kase) {
    guidedDetail(`<p class="note">No case is loaded for the current filters.</p>`);
    return false;
  }
  const adj = kase.adjudication || {};
  const alternatives = (kase.alternatives || []).map((a) => `
    <div class="alt ${a.alternative_id === adj.selected_alternative_id ? "is-selected" : ""}">
      ${a.alternative_id === adj.selected_alternative_id ? "&#9656; " : "&nbsp;&nbsp;"}
      ${esc(a.statement)}
      <span class="rel">[${esc(a.alternative_id)}]</span>
    </div>`).join("");
  const basis = (adj.basis_discriminant_ids || []).map((id) => {
    const d = (kase.discriminants || []).find((x) => x.discriminant_id === id);
    const rows = d ? (d.alternative_assessments || []).map((a) =>
      `<li><span class="rel">${esc(a.relation)}</span> ${esc(a.statement)}</li>`).join("") : "";
    return `<p class="note">Basis <code>${esc(id)}</code>${
      d ? `, status <code>${esc(d.status)}</code>` : ""}</p><ul class="note">${rows}</ul>`;
  }).join("");

  guidedDetail(`
    <h3>${esc((kase.question || {}).statement || "")}</h3>
    <p class="note">Case <code>${esc(kase.case_id)}</code>, question
      <code>${esc((kase.question || {}).question_id || "")}</code>.</p>
    <h3 class="minor">Alternatives considered</h3>
    ${alternatives}
    <div class="claim"><strong>Adjudication (${esc(adj.claim_status)}):</strong>
      ${esc(adj.statement)}</div>
    ${basis}
    <p class="note">${esc((kase.applicability || {}).scope || "")}</p>`);
  return true;
}

async function guidedReplay(step) {
  if (!(await guidedEnsureMechanism())) {
    guidedDetail(`<p class="err">Could not load this case's mechanism
      (${esc(guidedMechanismId() || "unresolved")}), so the proposed step is not
      shown. Nothing else was changed.</p>`);
    return false;
  }
  setStep(step < 0 ? state.view.edits.length : step);
  const panel = step < 0 ? state.view.state_pair.after : state.view.state_pair.before;
  guidedDetail(`
    <h3>${esc(state.view.transformation_id)}</h3>
    <p class="note">${esc(state.view.replay_semantics.note)}</p>
    <p class="note">Showing the ${step < 0 ? "after" : "before"} panel:
      source step <code>${esc((panel || {}).source_step_id)}</code>,
      ${esc(state.view.edits.length)} reviewed edits in this transition.</p>
    <p class="caveat">${esc(state.view.layout.semantics.note)}</p>`);
  el("graph").scrollIntoView({ behavior: "smooth", block: "center" });
  return true;
}

async function guidedResidue() {
  // The residue belongs to this case's mechanism. Load it first, so the graph
  // on screen and the selected relation cannot belong to different cases.
  if (!(await guidedEnsureMechanism())) {
    guidedDetail(`<p class="err">Could not load this case's mechanism
      (${esc(guidedMechanismId() || "unresolved")}), so no residue was selected.</p>`);
    return false;
  }
  const relation = focalRelation();
  if (!relation) {
    guidedDetail(`<p class="note">The current filters return no supported
      site relation with bound observations, so there is nothing to select.</p>`);
    return false;
  }
  // Selected by its own relation id, never by position or by a written-in atom.
  state.selectedFragmentId = relation.relation_id;
  state.selectedAtom = relation.source_atom_id;
  drawGraph(); renderFragments(); renderInspector();
  const ctx = relation.protein_structure_context || {};
  const mapping = (ctx.pdb_residue_mappings || [])[0] || {};
  guidedDetail(`
    <h3>Supported residue link</h3>
    <p class="note">Relation <code>${esc(relation.relation_id)}</code>,
      source atom <code>${esc(relation.source_atom_id)}</code>,
      match basis <code>${esc((relation.site_mapping || {}).match_basis)}</code>.</p>
    <table class="mini">
      <tr><th>atlas site</th><th>UniProt</th><th>PDB author</th><th>mmCIF label</th></tr>
      <tr><td>${esc(relation.site_id)}</td>
          <td>${esc(ctx.uniprot_id)} ${esc(ctx.residue_name)}${esc(ctx.sequence_position)}</td>
          <td>${esc(mapping.pdb_id)} ${esc(mapping.chain_id)} ${esc(mapping.author_position)}</td>
          <td>${esc(mapping.label_position)}</td></tr>
    </table>
    <p class="note">Deposited atom identity:
      <code>${esc((relation.deposited_atom_identity || {}).status)}</code>. The full
      relation, its witnesses and its limits are in the inspector on the right.</p>`);
  return true;
}

async function guidedEndpoints() {
  if (!(await guidedEnsureMechanism())) {
    guidedDetail(`<p class="err">Could not load this case's mechanism
      (${esc(guidedMechanismId() || "unresolved")}), so no comparison was run.</p>`);
    return false;
  }
  // A complete comparison needs every observation in the result, so both
  // filters are cleared and the real query re-run BEFORE the focal variant is
  // derived. Deriving it first would read a variant out of a filtered result.
  if (el("variant-select").value !== "" || el("endpoint-select").value !== "") {
    el("variant-select").value = "";
    el("endpoint-select").value = "";
    await loadEvidence();
  }
  const variant = focalVariant();
  if (!variant) {
    guidedDetail(`<p class="note">No focal variant is bound to a supported site
      relation in this result, so no comparison is shown. Nothing is guessed.</p>`);
    return false;
  }
  const all = ((state.evidence || {}).observations) || [];
  const focal = all.filter((o) => (o.variant || {}).variant_id === variant);
  const contextual = all.filter((o) => (o.variant || {}).variant_id !== variant);

  const reported = (o) => {
    const r = o.result || {};
    if (r.result_class !== "measured") {
      return `${esc(phrase(r.result_class))} <code>${esc(r.result_class)}</code>`;
    }
    return String(r.reported_relation) === "fold_lower_than_wild_type"
      ? `Reported ${esc(r.value)}-fold lower than WT <code>${esc(r.reported_relation)}</code>`
      : `${esc(r.value)} ${esc(r.unit)} <code>${esc(r.reported_relation)}</code>`;
  };
  const row = (o) => {
    const r = o.result || {};
    const value = reported(o);
    const conditions = (o.conditions || []).length
      ? (o.conditions || []).map((c) =>
          `${esc(c.name)} ${esc(c.value)}${c.unit ? " " + esc(c.unit) : ""}`).join(", ")
      : "not stated";
    return `<tr>
      <td>${esc(phrase((o.endpoint || {}).kind))}</td>
      <td>${esc((o.substrate || {}).enantiomer || "")} ${esc((o.substrate || {}).name || "")}</td>
      <td>${value}</td>
      <td>${o.comparator_variant_id ? esc(o.comparator_variant_id) : "none stated"}</td>
      <td>${conditions}</td>
      <td>${r.detection_limit === null || r.detection_limit === undefined
            ? "unknown" : esc(r.detection_limit)}</td>
    </tr>`;
  };

  guidedDetail(`
    <h3>Reported endpoints for ${esc(variant)}</h3>
    <table class="mini">
      <tr><th>endpoint</th><th>substrate</th><th>reported result</th>
          <th>comparator</th><th>conditions</th><th>detection limit</th></tr>
      ${focal.map(row).join("")}
    </table>
    <p class="caveat">A reported value belongs to its own comparator and conditions.
      A nondetection is not a numeric zero, and an unknown detection limit stays
      unknown.</p>
    ${contextual.length ? `
      <h3 class="minor">Contextual observations, not matched controls</h3>
      <table class="mini">
        <tr><th>variant</th><th>endpoint</th><th>substrate</th><th>reported result</th><th>comparator</th></tr>
        ${contextual.map((o) => `<tr>
          <td>${esc((o.variant || {}).variant_id)}</td>
          <td>${esc(phrase((o.endpoint || {}).kind))}</td>
          <td>${esc((o.substrate || {}).enantiomer || "")} ${esc((o.substrate || {}).name || "")}</td>
          <td>${reported(o)}</td>
          <td>${o.comparator_variant_id ? esc(o.comparator_variant_id) : "none stated"}</td>
        </tr>`).join("")}
      </table>
      <p class="caveat">These come from a different variant and are not matched
        controls for the focal variant.</p>` : ""}`);
  return true;
}


/**
 * Build a plain-text inspection request for a real external session.
 *
 * Every field is read from the current query results. This is a request, not a
 * result: it records what a session should look at, and says plainly that no
 * call has been made. It invents no deep link, tool name, protocol or receipt,
 * and it is never itself evidence that an inspection happened.
 */
function inspectionRequestText() {
  const relation = focalRelation();
  if (!relation) return null;
  const ctx = relation.protein_structure_context || {};
  const mapping = (ctx.pdb_residue_mappings || [])[0] || {};
  const structure = (ctx.structures || [])[0] || {};
  const kase = ((state.evidence || {}).cases || [])[0] || {};
  const variant = focalVariant();
  const papers = [...new Set(
    ((state.evidence || {}).observations || [])
      .filter((o) => (o.variant || {}).variant_id === variant)
      .flatMap((o) => o.evidence_ids || []))];

  const lines = [
    "Catalytic Earth Workbench — external inspection request",
    "STATUS: NOT YET EXECUTED. No external tool has been called for this request.",
    "",
    `Question: ${(kase.question || {}).statement || ""}`,
    `Case: ${kase.case_id || ""}`,
    `Focal variant: ${variant || "unresolved"}`,
    `Paper identifiers on the record: ${papers.join(", ") || "none"}`,
    "",
    "Site identity, numbering systems travel together:",
    `  atlas site        ${relation.site_id}`,
    `  UniProt           ${ctx.uniprot_id} ${ctx.residue_name}${ctx.sequence_position}`,
    `  PDB author        ${mapping.pdb_id} chain ${mapping.chain_id} ${mapping.author_position}`,
    `  mmCIF label       ${mapping.label_position}`,
    `  source locator    ${relation.source_atom_id} (depiction locator, not an atom name)`,
    `  deposited atom    ${(relation.deposited_atom_identity || {}).status}`,
    "",
    "Reference structure:",
    `  ${structure.pdb_id || "none"} ${structure.experimental_method || ""} ` +
      `${structure.resolution_angstrom !== undefined ? structure.resolution_angstrom + " A" : ""}`,
    `  context flags     ${(structure.context_flags || []).join(", ")}`,
    `  limitation        ${structure.limitation || ""}`,
    "",
    "Requested inspection:",
    `  1. View ${structure.pdb_id || "the reference structure"} and locate ` +
      `${ctx.residue_name}${ctx.sequence_position} using PDB author numbering ` +
      `${mapping.author_position} in chain ${mapping.chain_id}.`,
    `  2. Retrieve the bibliographic record for ${papers[0] || "the cited paper"}.`,
    "",
    "Boundaries to preserve in the session:",
    `  - ${structure.pdb_id || "This structure"} is reference site context. It is not ` +
      `an ${variant || "assayed"} mutant structure and must not be presented as one.`,
    "  - A reported structural comparison in the evidence names no deposited structure.",
    "  - Record the result only from a call actually made, with its exact tool name.",
  ];
  return lines.join("\n");
}

async function guidedStructure() {
  if (!(await guidedResidue())) return false;
  const relation = focalRelation();
  if (!relation) {
    guidedDetail(`<p class="note">The current filters return no supported site
      relation, so there is nothing to prepare.</p>`);
    return false;
  }
  const text = inspectionRequestText();
  const ledger = state.external || {};
  guidedDetail(`
    <h3>Inspection request for a real external session</h3>
    <p class="note">This records what a session should look at. It is not a tool
      call and not a receipt. Nothing here is sent anywhere.</p>
    <p class="note">Contribution ledger: <strong>${esc(ledger.contribution_count || 0)}</strong>
      recorded. ${ledger.contribution_count
        ? esc((ledger.providers_used || []).join(", "))
        : "No external tool has been credited yet."}</p>
    <pre id="inspection-request">${esc(text)}</pre>
    <div class="gs-actions">
      <button id="copy-request" class="pill pill-primary">Copy inspection request</button>
      <span id="copy-state" class="note"></span>
    </div>
    <p class="caveat">After a real call, record it with
      <code>python -m catalytic_earth.workbench.external_sources</code>, using the
      exact suite and tool that produced it.</p>`);

  el("copy-request").addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(text);
      el("copy-state").textContent = "Copied. It has not been executed.";
    } catch (err) {
      // Clipboard access can be refused; the text is on screen either way.
      const node = el("inspection-request");
      const range = document.createRange();
      range.selectNodeContents(node);
      const sel = window.getSelection();
      sel.removeAllRanges(); sel.addRange(range);
      el("copy-state").textContent = "Clipboard unavailable; the text is selected above.";
    }
  });
  return true;
}

/* ------------------------------------------------------ init and tab wiring */

/* ------------------------------------------------------------------- init */

function initGuided() {
  const setMode = (on) => {
    state.guided = on;
    if (!on) el("guided-detail").innerHTML = "";
    renderGuided();
    if (on) el("guided").scrollIntoView({ behavior: "smooth", block: "nearest" });
  };
  el("guided-toggle").addEventListener("click", () => {
    // Entering the guided path needs the replay tab's controls.
    document.querySelectorAll(".tab[data-tab]").forEach((x) =>
      x.classList.remove("is-active"));
    document.querySelectorAll(".tabpanel").forEach((x) => x.classList.remove("is-active"));
    document.querySelector('[data-tab="replay"]').classList.add("is-active");
    el("tab-replay").classList.add("is-active");
    setMode(!state.guided);
  });
  el("guided-exit").addEventListener("click", () => setMode(false));
}

function initTabs() {
  // Only buttons that name a panel are panel tabs. The guided toggle shares
  // their styling but owns its own state, so it is excluded here.
  document.querySelectorAll(".tab[data-tab]").forEach((tab) =>
    tab.addEventListener("click", () => {
      document.querySelectorAll(".tab[data-tab]").forEach((t) =>
        t.classList.remove("is-active"));
      document.querySelectorAll(".tabpanel").forEach((p) => p.classList.remove("is-active"));
      tab.classList.add("is-active");
      el("tab-" + tab.dataset.tab).classList.add("is-active");
    }));
}

async function init() {
  initTabs();
  initGuided();

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
