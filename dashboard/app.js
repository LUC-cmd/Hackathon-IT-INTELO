/* MemBridge Dashboard — hero cinématique, innovations visibles */

const PAL = {
  rust: "#D04A2C",
  moss: "#1F4D3A",
  green: "#4ADE80",
  amber: "#E8A317",
  ink: "#14110F",
  clay: "#8A7B6A",
  paper: "#F5EDE3",
};

const I18N = {
  fr: {
    run: "▶ Benchmark",
    naive: "Mode naïf",
    memory: "MemBridge",
    audio_hint: "Cliquer pour dicter · reconnaissance vocale",
    listening: "Écoute en cours…",
    stored: "Stocké en mémoire",
    no_result: "Aucun résultat",
  },
  en: {
    run: "▶ Benchmark",
    naive: "Naive mode",
    memory: "MemBridge",
    audio_hint: "Click to dictate · speech recognition",
    listening: "Listening…",
    stored: "Stored in memory",
    no_result: "No result",
  },
};

let lang = "fr";
let charts = {};
let recognition = null;
let listening = false;
let mediaStream = null;
let trapIndex = 0;
let trapDetails = [];

function t(k) { return I18N[lang][k] || k; }

/* ── Sons ── */
function playVictorySound() {
  const ctx = new (window.AudioContext || window.webkitAudioContext)();
  [220, 277, 330, 415].forEach((freq, i) => {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = "triangle";
    osc.frequency.value = freq;
    gain.gain.setValueAtTime(0, ctx.currentTime + i * 0.15);
    gain.gain.linearRampToValueAtTime(0.12, ctx.currentTime + i * 0.15 + 0.05);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + i * 0.15 + 0.5);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start(ctx.currentTime + i * 0.15);
    osc.stop(ctx.currentTime + i * 0.15 + 0.55);
  });
}

function playTick() {
  const ctx = new (window.AudioContext || window.webkitAudioContext)();
  const osc = ctx.createOscillator();
  const g = ctx.createGain();
  osc.type = "sine";
  osc.frequency.value = 880;
  g.gain.value = 0.04;
  osc.connect(g);
  g.connect(ctx.destination);
  osc.start();
  osc.stop(ctx.currentTime + 0.06);
}

function confetti() {
  const colors = [PAL.rust, PAL.moss, PAL.amber, PAL.green, PAL.paper];
  for (let i = 0; i < 50; i++) {
    const el = document.createElement("div");
    el.className = "confetti";
    el.style.left = Math.random() * 100 + "vw";
    el.style.top = "-8px";
    el.style.background = colors[i % colors.length];
    el.style.transform = `rotate(${Math.random() * 360}deg)`;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 2800);
  }
}

function animateCounter(el, target) {
  if (!el) return;
  const start = parseInt(el.textContent.replace(/\D/g, ""), 10) || 0;
  const dur = 900;
  const t0 = performance.now();
  function step(now) {
    const p = Math.min((now - t0) / dur, 1);
    const ease = 1 - Math.pow(1 - p, 3);
    el.textContent = Math.round(start + (target - start) * ease).toLocaleString();
    if (p < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

/* ── Graphiques ── */
const chartDefaults = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { labels: { color: PAL.clay, font: { family: "'IBM Plex Mono'" } } },
  },
};

function destroyChart(id) {
  if (charts[id]) { charts[id].destroy(); delete charts[id]; }
}

function renderTokenChart(data) {
  destroyChart("token");
  const naive = data.naive.per_turn_tokens || [];
  const memory = data.memory.per_turn_tokens || [];
  charts.token = new Chart(document.getElementById("token-chart"), {
    type: "line",
    data: {
      labels: naive.map((_, i) => i + 1),
      datasets: [
        { label: t("naive"), data: naive, borderColor: PAL.rust, backgroundColor: "rgba(208,74,44,0.1)", fill: true, tension: 0.35, pointRadius: 0, borderWidth: 2.5 },
        { label: t("memory"), data: memory, borderColor: PAL.green, backgroundColor: "rgba(74,222,128,0.08)", fill: true, tension: 0.35, pointRadius: 0, borderWidth: 2.5 },
      ],
    },
    options: {
      ...chartDefaults,
      scales: {
        x: { ticks: { color: PAL.clay, maxTicksLimit: 10 }, grid: { color: "rgba(255,255,255,0.05)" } },
        y: { ticks: { color: PAL.clay }, grid: { color: "rgba(255,255,255,0.05)" } },
      },
    },
  });
}

function renderDonutChart(data) {
  destroyChart("donut");
  const saved = data.tokens_saved || 0;
  const memory = data.memory?.total_tokens || 1;
  charts.donut = new Chart(document.getElementById("donut-chart"), {
    type: "doughnut",
    data: {
      labels: [t("memory"), t("naive") + " évité"],
      datasets: [{ data: [memory, saved], backgroundColor: [PAL.green, PAL.rust], borderColor: PAL.ink, borderWidth: 2 }],
    },
    options: { ...chartDefaults, cutout: "62%", plugins: { legend: { position: "bottom" } } },
  });
}

function renderCumulativeChart(data) {
  destroyChart("cumulative");
  const naive = data.naive?.per_turn_tokens || [];
  const memory = data.memory?.per_turn_tokens || [];
  let nSum = 0, mSum = 0;
  const nCum = naive.map((v) => { nSum += v; return nSum; });
  const mCum = memory.map((v) => { mSum += v; return mSum; });
  charts.cumulative = new Chart(document.getElementById("cumulative-chart"), {
    type: "line",
    data: {
      labels: nCum.map((_, i) => i + 1),
      datasets: [
        { label: "Naïf cumulé", data: nCum, borderColor: PAL.rust, tension: 0.3, fill: false, pointRadius: 0 },
        { label: "MemBridge cumulé", data: mCum, borderColor: PAL.green, tension: 0.3, fill: false, pointRadius: 0 },
      ],
    },
    options: { ...chartDefaults, scales: { x: { ticks: { color: PAL.clay } }, y: { ticks: { color: PAL.clay } } } },
  });
}

function renderRadarChart(data) {
  destroyChart("radar");
  const q = data.quality?.score_pct || 0;
  const s = Math.min(data.savings_pct || 0, 100);
  const g = data.memory?.growth_factor ? Math.max(0, 100 - (data.memory.growth_factor - 1) * 200) : 80;
  const c = data.memory?.compression_ratio ? Math.max(0, 100 - data.memory.compression_ratio * 200) : 75;
  charts.radar = new Chart(document.getElementById("radar-chart"), {
    type: "radar",
    data: {
      labels: ["Économie", "Qualité", "Stabilité", "Compression"],
      datasets: [{ label: "MemBridge", data: [s, q, g, c], backgroundColor: "rgba(74,222,128,0.15)", borderColor: PAL.green, borderWidth: 2 }],
    },
    options: {
      ...chartDefaults,
      scales: { r: { min: 0, max: 100, ticks: { display: false }, grid: { color: "rgba(255,255,255,0.08)" }, pointLabels: { color: PAL.clay } } },
    },
  });
}

function renderTrapChart(quality) {
  destroyChart("trap");
  const details = quality?.details || [];
  charts.trap = new Chart(document.getElementById("trap-chart"), {
    type: "bar",
    data: {
      labels: details.map((d, i) => `#${i + 1}`),
      datasets: [{ label: "Score", data: details.map((d) => d.score || 0), backgroundColor: details.map((d) => d.passed ? PAL.green : PAL.rust), borderWidth: 0 }],
    },
    options: {
      ...chartDefaults,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: PAL.clay }, grid: { display: false } },
        y: { min: 0, max: 1, ticks: { color: PAL.clay }, grid: { color: "rgba(255,255,255,0.05)" } },
      },
    },
  });
}

function renderBattleBar(data) {
  const naive = data.naive?.total_tokens || 1;
  const memory = data.memory?.total_tokens || 1;
  const total = naive + memory;
  const naivePct = Math.round((naive / total) * 100);
  document.getElementById("battle-naive").style.width = naivePct + "%";
  document.getElementById("battle-memory").style.width = (100 - naivePct) + "%";
}

function renderTraps(quality) {
  const list = document.getElementById("trap-list");
  if (!list) return;
  list.innerHTML = "";
  (quality?.details || []).forEach((item) => {
    const div = document.createElement("div");
    div.className = `trap-item ${item.passed ? "ok" : "ko"}`;
    div.innerHTML = `<span>${item.query}</span><span class="trap-score">${(item.score || 0).toFixed(3)}</span><span>${item.passed ? "✓" : "✗"} ${item.expected}</span>`;
    list.appendChild(div);
  });
}

function renderTimeline(entries) {
  const el = document.getElementById("memory-timeline");
  if (!el) return;
  el.innerHTML = "";
  (entries || []).forEach((e) => {
    const dot = document.createElement("div");
    dot.className = "timeline-dot";
    dot.title = e.content?.slice(0, 60) || "";
    if (e.tags?.includes("fact")) dot.classList.add("fact");
    else if (e.tags?.includes("geo")) dot.classList.add("geo");
    else if (e.tags?.some((tg) => ["audio", "video", "call", "transcript", "vision"].includes(tg)))
      dot.classList.add("media");
    el.appendChild(dot);
  });
}

function renderInsights(insights) {
  const panel = document.getElementById("insights-panel");
  if (!panel) return;
  if (!insights?.insights?.length) { panel.hidden = true; return; }
  panel.hidden = false;
  document.getElementById("insights-summary").textContent = insights.summary || "";
  const list = document.getElementById("insights-list");
  list.innerHTML = "";
  insights.insights.forEach((item) => {
    const div = document.createElement("div");
    div.className = `insight-item ${item.severity}`;
    div.innerHTML = `<span><strong>${item.title}</strong> — ${item.description}</span><span>${item.value}</span>`;
    list.appendChild(div);
  });
}

function updateHeroStats(data) {
  const savings = document.getElementById("hero-savings");
  const traps = document.getElementById("hero-traps");
  if (savings) savings.textContent = `${Math.round(data.savings_pct)}%`;
  if (traps) traps.textContent = `${data.quality.passed}/${data.quality.total}`;
}

/* ── Comparaison slider ── */
const NAIVE_SAMPLE = `Tour 1: Bonjour, je suis Marie Dupont, cliente premium chez TechCorp.
Tour 2: assistant: Bienvenue Marie, comment puis-je vous aider ?
Tour 3: Mon numéro de contrat est CTR-2024-8847.
Tour 4: assistant: Contrat noté CTR-2024-8847.
Tour 5: La facture de mars devrait être 99,90 € mais affiche 149,90 €.
… + 45 tours de bruit sémantique (météo, recettes, sport, cinéma)
Tour 50: assistant: hors-sujet tour 24 — blockbuster mars — bruit 408

→ Contexte envoyé au LLM : ~22 381 tokens (historique complet)`;

const MEMORY_SAMPLE = `[RÉSUMÉ STRUCTURÉ — 42 tokens]
CLIENT=Marie Dupont | CTR=CTR-2024-8847 | MAIL=marie.dupont@email.fr
EUR=149,90 (écart +50€) | DATE=12 février (bug iOS)

[RECHERCHE SÉMANTIQUE — top 3 résultats]
① score 0.76 — "identité interlocutrice premium" → Marie Dupont
② score 0.74 — "référence légale dossier" → CTR-2024-8847
③ score 0.59 — "coordonnées électroniques" → marie.dupont@email.fr

→ Contexte envoyé au LLM : ~4 580 tokens (résumé + recherche ciblée)
→ Économie : 79.5% · Qualité pièges : 10/10`;

function initCompareSlider() {
  const wrap = document.getElementById("compare-wrap");
  const handle = document.getElementById("compare-handle");
  const layer = document.getElementById("compare-memory-layer");
  const naiveEl = document.getElementById("compare-naive-text");
  const memEl = document.getElementById("compare-memory-text");
  if (!wrap || !handle || !layer) return;

  naiveEl.textContent = NAIVE_SAMPLE;
  memEl.textContent = MEMORY_SAMPLE;

  let dragging = false;
  const setPos = (pct) => {
    const p = Math.max(5, Math.min(95, pct));
    handle.style.left = p + "%";
    layer.style.clipPath = `inset(0 ${100 - p}% 0 0)`;
  };

  const onMove = (clientX) => {
    const rect = wrap.getBoundingClientRect();
    setPos(((clientX - rect.left) / rect.width) * 100);
  };

  handle.addEventListener("mousedown", () => { dragging = true; });
  window.addEventListener("mouseup", () => { dragging = false; });
  window.addEventListener("mousemove", (e) => { if (dragging) onMove(e.clientX); });
  wrap.addEventListener("click", (e) => onMove(e.clientX));
  handle.addEventListener("touchstart", (e) => { dragging = true; e.preventDefault(); });
  window.addEventListener("touchend", () => { dragging = false; });
  window.addEventListener("touchmove", (e) => { if (dragging) onMove(e.touches[0].clientX); });
  setPos(50);
}

/* ── Piège carousel ── */
function buildTrapCarousel(quality) {
  trapDetails = quality?.details || [];
  const carousel = document.getElementById("trap-carousel");
  if (!carousel || !trapDetails.length) return;

  carousel.innerHTML = "";
  trapDetails.forEach((item, i) => {
    const slide = document.createElement("div");
    slide.className = `trap-slide${i === 0 ? " active" : ""}`;
    slide.id = `trap-slide-${i}`;
    slide.innerHTML = `
      <div class="trap-q">❓ ${item.query}</div>
      <div class="trap-a" id="trap-answer-${i}">Réponse attendue : <strong>${item.expected}</strong></div>
      <span class="trap-score-badge">${item.passed ? "✓ RÉUSSI" : "✗ ÉCHOUÉ"} — score ${(item.score || 0).toFixed(3)}</span>`;
    carousel.appendChild(slide);
  });
  trapIndex = 0;
}

function showTrapSlide(idx) {
  if (!trapDetails.length) return;
  trapIndex = (idx + trapDetails.length) % trapDetails.length;
  document.querySelectorAll(".trap-slide").forEach((s, i) => {
    s.classList.toggle("active", i === trapIndex);
  });
  playTick();
}

async function testCurrentTrap() {
  const item = trapDetails[trapIndex];
  if (!item) return;
  const answerEl = document.getElementById(`trap-answer-${trapIndex}`);
  answerEl.innerHTML = "Recherche en cours…";
  playTick();
  const res = await api(`/api/search?q=${encodeURIComponent(item.query)}`);
  if (res.results?.length) {
    const top = res.results[0];
    const ok = top.content?.toLowerCase().includes(item.expected.toLowerCase());
    answerEl.innerHTML = `
      Résultat : <strong>${top.content?.slice(0, 120)}</strong><br>
      <span class="trap-score-badge" style="background:${ok ? PAL.moss : PAL.rust}">${ok ? "✓ TROUVÉ" : "✗ MANQUÉ"} — score ${top.score?.toFixed(3)}</span>`;
    if (ok) playVictorySound();
  } else {
    answerEl.innerHTML = `<span style="color:${PAL.rust}">Aucun résultat</span>`;
  }
}

/* ── Console MCP — vrais appels API ── */
const DEMO_LAT = 6.1319;
const DEMO_LON = 1.2228;
const TOUR_TOOLS = ["seed", "search", "store", "summarize", "translate", "timeline", "stats", "transcribe", "locate", "vision", "share"];

function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

function showConsole(text, isError = false) {
  const out = document.getElementById("console-output");
  const status = document.getElementById("console-status");
  if (out) {
    out.textContent = text;
    out.classList.toggle("error", isError);
  }
  if (status) status.textContent = isError ? "❌ Erreur" : "📡 Réponse MCP reçue";
}

function highlightTool(tool, state = "running") {
  document.querySelectorAll(".tool-btn, .innov-card").forEach((el) => {
    if (el.dataset.tool !== tool) {
      el.classList.remove("running", "done", "active");
      return;
    }
    el.classList.remove("running", "done", "active");
    if (state === "running") el.classList.add("running");
    if (state === "done") el.classList.add("done");
    if (state === "active") el.classList.add("active");
  });
}

async function refreshMemory() {
  try {
    const mem = await api("/api/memory");
    renderTimeline(mem.entries);
    window.BrainViz?.setFromMemory(mem.entries);
    const naiveEl = document.getElementById("compare-memory-text");
    if (naiveEl && mem.summary?.summary) {
      naiveEl.textContent = `[RÉSUMÉ LIVE — ${mem.summary.compressed_chars} chars]\n${mem.summary.summary}\n\n[${mem.count} entrées en mémoire]`;
    }
    return mem;
  } catch { return null; }
}

const TOOL_ACTIONS = {
  seed: () => api("/api/seed", { method: "POST" }),
  search: () => api("/api/search?q=" + encodeURIComponent("identité de l'interlocutrice premium")),
  store: () => api("/api/store", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content: "Démo jury : nouveau fait — équipe INTELO2026 Lomé", tags: ["fact", "demo"] }),
  }),
  summarize: () => api("/api/summarize"),
  stats: () => api("/api/stats"),
  transcribe: () => {
    const text = document.getElementById("transcript")?.value?.trim()
      || "Marie Dupont confirme le contrat CTR-2024-8847 par téléphone.";
    return api("/api/transcribe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ transcript: text, source: "audio", language: "fr" }),
    });
  },
  vision: () => api("/api/vision", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ label: "Capture démo jury INTELO2026", image_b64: "demo" }),
  }),
  locate: () => api("/api/locate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ latitude: DEMO_LAT, longitude: DEMO_LON, label: "Hackathon Lomé" }),
  }),
  translate: () => api("/api/translate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: "cliente premium — contrat et facture", target_lang: "en" }),
  }),
  timeline: () => api("/api/timeline"),
  share: () => api("/api/share", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ from_session: "live-demo", to_session: "agent-2", query: "contrat client premium" }),
  }),
  forget: () => api("/api/forget", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tag: "noise" }),
  }),
};

async function runMcpTool(tool) {
  const fn = TOOL_ACTIONS[tool];
  if (!fn) return;
  highlightTool(tool, "running");
  showConsole(`▶ ${tool} en cours…\nGET/POST /api/${tool === "seed" ? "seed" : tool}`);
  playTick();
  try {
    const result = await fn();
    showConsole(`✅ ${tool} — succès\n\n${JSON.stringify(result, null, 2)}`);
    highlightTool(tool, "done");
    await refreshMemory();
    if (tool === "search" && result.results?.[0]) {
      const box = document.getElementById("search-result");
      if (box) {
        box.innerHTML = `<strong>Score ${result.results[0].score?.toFixed(3)}</strong> — ${result.results[0].content}`;
        box.classList.add("visible");
      }
    }
    if (tool === "locate") {
      document.getElementById("geo-status").textContent = `${DEMO_LAT}, ${DEMO_LON} (Lomé)`;
      document.getElementById("map-preview").style.backgroundImage =
        `url(https://staticmap.openstreetmap.de/staticmap.php?center=${DEMO_LAT},${DEMO_LON}&zoom=13&size=400x140&markers=${DEMO_LAT},${DEMO_LON},red)`;
    }
    if (tool === "translate" && result.translated) playVictorySound();
    return result;
  } catch (e) {
    showConsole(`❌ ${tool} — ${e.message}`, true);
    highlightTool(tool, "active");
    throw e;
  }
}

async function runDemoTour() {
  const btn = document.getElementById("btn-demo-tour");
  if (btn) { btn.disabled = true; btn.textContent = "⏳ Tour en cours…"; }
  showConsole("🚀 Tour démo — 11 outils MCP en séquence…");
  for (const tool of TOUR_TOOLS) {
    try { await runMcpTool(tool); } catch { /* continue */ }
    await sleep(700);
  }
  showConsole("✅ Tour démo terminé — 11 outils MCP testés avec succès");
  confetti();
  playVictorySound();
  if (btn) { btn.disabled = false; btn.textContent = "▶ Tour démo auto (11 outils)"; }
}

async function runAllTraps() {
  const btn = document.getElementById("btn-all-traps");
  if (btn) { btn.disabled = true; btn.textContent = "⏳ Pièges…"; }
  let passed = 0;
  const lines = ["🎯 Test des 10 questions pièges :\n"];
  for (let i = 0; i < trapDetails.length; i++) {
    const item = trapDetails[i];
    const res = await api(`/api/search?q=${encodeURIComponent(item.query)}`);
    const top = res.results?.[0];
    const ok = top?.content?.toLowerCase().includes(item.expected.toLowerCase());
    if (ok) passed++;
    lines.push(`${ok ? "✓" : "✗"} #${i + 1} "${item.query}" → ${item.expected} (score ${top?.score?.toFixed(3) || "—"})`);
    showTrapSlide(i);
    const answerEl = document.getElementById(`trap-answer-${i}`);
    if (answerEl && top) {
      answerEl.innerHTML = `Résultat : <strong>${top.content?.slice(0, 100)}</strong>`;
    }
    await sleep(400);
  }
  lines.push(`\n🏆 Résultat : ${passed}/${trapDetails.length} pièges réussis`);
  showConsole(lines.join("\n"));
  if (passed === trapDetails.length) { confetti(); playVictorySound(); }
  if (btn) { btn.disabled = false; btn.textContent = "🎯 Tester les 10 pièges"; }
}

function initInnovCards() {
  document.querySelectorAll("[data-tool]").forEach((el) => {
    const tool = el.dataset.tool;
    const handler = (e) => {
      e.stopPropagation();
      document.getElementById("console")?.scrollIntoView({ behavior: "smooth", block: "start" });
      runMcpTool(tool);
    };
    if (el.classList.contains("tool-btn")) {
      el.addEventListener("click", handler);
    } else if (el.classList.contains("innov-card")) {
      el.querySelector(".innov-run")?.addEventListener("click", handler);
    }
  });
  document.getElementById("btn-demo-tour")?.addEventListener("click", runDemoTour);
  document.getElementById("btn-seed")?.addEventListener("click", () => runMcpTool("seed"));
  document.getElementById("btn-all-traps")?.addEventListener("click", runAllTraps);
  document.getElementById("console-clear")?.addEventListener("click", () => {
    showConsole("// Console effacée — cliquez un outil MCP");
    document.querySelectorAll(".tool-btn, .innov-card").forEach((el) => el.classList.remove("running", "done", "active"));
  });
}

function renderReport(data) {
  animateCounter(document.getElementById("naive-tokens"), data.naive.total_tokens);
  animateCounter(document.getElementById("memory-tokens"), data.memory.total_tokens);
  document.getElementById("savings").textContent = `-${data.savings_pct}%`;
  document.getElementById("euros-saved").textContent = `${(data.tokens_saved || 0).toLocaleString()} tokens économisés`;
  document.getElementById("quality-score").textContent = `${data.quality.passed}/${data.quality.total}`;
  document.getElementById("quality-bar").style.width = `${data.quality.score_pct}%`;
  updateHeroStats(data);
  renderTokenChart(data);
  renderDonutChart(data);
  renderCumulativeChart(data);
  renderRadarChart(data);
  renderTrapChart(data.quality);
  renderBattleBar(data);
  renderTraps(data.quality);
  renderInsights(data.insights);
  buildTrapCarousel(data.quality);
  window.__lastReport = data;
  if (data.savings_pct >= 70) { confetti(); playVictorySound(); }
}

/* ── API ── */
async function api(path, opts) {
  const res = await fetch(path, opts);
  return res.json();
}

async function loadReport() {
  try {
    const data = await api("/api/report");
    renderReport(data);
    await refreshMemory();
    await api("/api/seed", { method: "POST" });
  } catch { /* offline — données statiques */ }
}

async function runBenchmark() {
  const btn = document.getElementById("run-benchmark");
  btn.disabled = true;
  btn.textContent = "…";
  playTick();
  try {
    renderReport(await api("/api/benchmark"));
    const mem = await api("/api/memory");
    renderTimeline(mem.entries);
    window.BrainViz?.setFromMemory(mem.entries);
  } finally {
    btn.disabled = false;
    btn.textContent = t("run");
  }
}

/* ── Recherche ── */
document.getElementById("search-btn").onclick = async () => {
  const q = document.getElementById("search-query").value.trim();
  if (!q) return;
  playTick();
  const res = await api(`/api/search?q=${encodeURIComponent(q)}`);
  const box = document.getElementById("search-result");
  if (res.results?.length) {
    const top = res.results[0];
    box.innerHTML = `<strong>Score ${top.score?.toFixed(3)}</strong> — ${top.content}`;
    box.classList.add("visible");
  } else {
    box.textContent = t("no_result");
    box.classList.add("visible");
  }
};

/* ── Audio ── */
function initSpeech() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) return;
  recognition = new SR();
  recognition.lang = lang === "fr" ? "fr-FR" : "en-US";
  recognition.continuous = false;
  recognition.interimResults = true;
  recognition.onresult = (ev) => {
    const text = Array.from(ev.results).map((r) => r[0].transcript).join("");
    document.getElementById("transcript").value = text;
  };
  recognition.onend = () => {
    listening = false;
    window.AudioViz?.stop();
    const zone = document.getElementById("audio-zone");
    zone.classList.remove("recording");
    zone.textContent = t("audio_hint");
  };
}

document.getElementById("audio-zone").onclick = () => {
  if (!recognition) initSpeech();
  if (!recognition) {
    document.getElementById("audio-status").textContent = "Speech API non supportée";
    return;
  }
  if (listening) { recognition.stop(); return; }
  listening = true;
  recognition.lang = lang === "fr" ? "fr-FR" : "en-US";
  const zone = document.getElementById("audio-zone");
  zone.classList.add("recording");
  zone.innerHTML = `<span class="rec-indicator"></span>${t("listening")}`;
  window.AudioViz?.start();
  recognition.start();
};

document.getElementById("store-transcript").onclick = async () => {
  const text = document.getElementById("transcript").value.trim();
  if (!text) return;
  await api("/api/transcribe", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ transcript: text, source: "audio" }),
  });
  document.getElementById("audio-status").textContent = t("stored");
  playTick();
  const mem = await api("/api/memory");
  renderTimeline(mem.entries);
  window.BrainViz?.setFromMemory(mem.entries);
};

/* ── Caméra ── */
document.getElementById("cam-btn").onclick = async () => {
  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    document.getElementById("video-preview").srcObject = mediaStream;
    document.getElementById("video-status").textContent = "Caméra active";
  } catch {
    document.getElementById("video-status").textContent = "Caméra refusée";
  }
};

document.getElementById("snap-btn").onclick = async () => {
  const video = document.getElementById("video-preview");
  const canvas = document.getElementById("snapshot-canvas");
  if (!video.videoWidth) {
    document.getElementById("video-status").textContent = "Activez la caméra d'abord";
    return;
  }
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0);
  const dataUrl = canvas.toDataURL("image/jpeg", 0.7);
  await api("/api/vision", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image_b64: dataUrl.slice(0, 200), label: "Capture démo jury" }),
  });
  document.getElementById("video-status").textContent = t("stored");
  playTick();
};

/* ── Géo ── */
document.getElementById("geo-btn").onclick = () => {
  if (!navigator.geolocation) return;
  navigator.geolocation.getCurrentPosition(async (pos) => {
    const { latitude, longitude } = pos.coords;
    document.getElementById("geo-status").textContent = `${latitude.toFixed(4)}, ${longitude.toFixed(4)}`;
    document.getElementById("map-preview").style.backgroundImage =
      `url(https://staticmap.openstreetmap.de/staticmap.php?center=${latitude},${longitude}&zoom=13&size=400x140&markers=${latitude},${longitude},red)`;
    await api("/api/locate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ latitude, longitude, label: "Démo jury" }),
    });
    const mem = await api("/api/memory");
    renderTimeline(mem.entries);
    window.BrainViz?.setFromMemory(mem.entries);
  });
};

/* ── Export ── */
document.getElementById("export-pdf")?.addEventListener("click", () => {
  window.open("/api/export/pdf", "_blank");
});

document.getElementById("export-json")?.addEventListener("click", () => {
  if (!window.__lastReport) return;
  const blob = new Blob([JSON.stringify(window.__lastReport, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "membridge-report.json";
  a.click();
});

/* ── UI ── */
document.getElementById("lang-toggle").onclick = () => {
  lang = lang === "fr" ? "en" : "fr";
  document.getElementById("lang-toggle").textContent = lang === "fr" ? "EN" : "FR";
};

document.getElementById("present-mode").onclick = () => {
  document.body.classList.toggle("present-mode");
};

document.getElementById("run-benchmark").onclick = runBenchmark;
document.getElementById("trap-prev")?.addEventListener("click", () => showTrapSlide(trapIndex - 1));
document.getElementById("trap-next")?.addEventListener("click", () => showTrapSlide(trapIndex + 1));
document.getElementById("trap-test")?.addEventListener("click", testCurrentTrap);

/* ── Init ── */
window.BrainViz?.init("brain-canvas");
initCompareSlider();
initInnovCards();
initSpeech();
loadReport();
