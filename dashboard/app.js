/* MemBridge Dashboard — palette chaude, pas de violet IA */

const PAL = {
  rust: "#C44F28",
  moss: "#2F5242",
  amber: "#D4922A",
  ink: "#1A1714",
  clay: "#9E8E7E",
  paper: "#F0E8DC",
};

const I18N = {
  fr: {
    title: "MemBridge",
    subtitle: "Mémoire partagée · Benchmark live · Multi-modal",
    present: "Présentation",
    run: "Lancer benchmark",
    naive: "Mode naïf",
    memory: "MemBridge",
    tokens_cum: "tokens cumulés",
    savings: "Économie",
    quality: "Pièges",
    chart_tokens: "Tokens par tour",
    chart_savings: "Répartition coût",
    search_live: "Recherche sémantique live",
    search: "Chercher",
    timeline: "Timeline mémoire",
    timeline_hint: "■ fait · ■ géo · ■ média",
    audio: "Audio live",
    audio_hint: "Cliquer pour dicter · reconnaissance vocale",
    video: "Vidéo / image",
    cam_on: "Caméra",
    snap: "Capture → mémoire",
    geo: "Géolocalisation",
    geo_wait: "En attente…",
    geo_btn: "Activer GPS",
    store: "→ Mémoire",
    traps: "Questions pièges — détail",
    footer: "MemBridge · INTELO2026",
    listening: "Écoute en cours…",
    stored: "Stocké en mémoire",
    no_result: "Aucun résultat",
  },
  en: {
    title: "MemBridge",
    subtitle: "Shared memory · Live benchmark · Multi-modal",
    present: "Present",
    run: "Run benchmark",
    naive: "Naive mode",
    memory: "MemBridge",
    tokens_cum: "cumulative tokens",
    savings: "Savings",
    quality: "Traps",
    chart_tokens: "Tokens per turn",
    chart_savings: "Cost split",
    search_live: "Live semantic search",
    search: "Search",
    timeline: "Memory timeline",
    timeline_hint: "■ fact · ■ geo · ■ media",
    audio: "Live audio",
    audio_hint: "Click to dictate · speech recognition",
    video: "Video / image",
    cam_on: "Camera",
    snap: "Capture → memory",
    geo: "Geolocation",
    geo_wait: "Waiting…",
    geo_btn: "Enable GPS",
    store: "→ Memory",
    traps: "Trap questions — detail",
    footer: "MemBridge · INTELO2026",
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

function t(k) { return I18N[lang][k] || k; }

function applyI18n() {
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const k = el.dataset.i18n;
    if (k === "audio_hint" && listening) return;
    el.textContent = t(k);
  });
  document.getElementById("lang-toggle").textContent = lang === "fr" ? "EN" : "FR";
}

/* ── Son organique (pas de synth bleep) ── */
function playVictorySound() {
  const ctx = new (window.AudioContext || window.webkitAudioContext)();
  const notes = [220, 277, 330, 415];
  notes.forEach((freq, i) => {
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
  const colors = [PAL.rust, PAL.moss, PAL.amber, PAL.ink, PAL.paper];
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

/* ── Compteur animé ── */
function animateCounter(el, target) {
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
    legend: { labels: { color: PAL.ink, font: { family: "'IBM Plex Mono'" } } },
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
        {
          label: t("naive"),
          data: naive,
          borderColor: PAL.rust,
          backgroundColor: "rgba(196,79,40,0.08)",
          fill: true,
          tension: 0.35,
          pointRadius: 0,
          borderWidth: 2.5,
        },
        {
          label: t("memory"),
          data: memory,
          borderColor: PAL.moss,
          backgroundColor: "rgba(47,82,66,0.08)",
          fill: true,
          tension: 0.35,
          pointRadius: 0,
          borderWidth: 2.5,
        },
      ],
    },
    options: {
      ...chartDefaults,
      scales: {
        x: { ticks: { color: PAL.clay, maxTicksLimit: 10 }, grid: { color: "rgba(26,23,20,0.06)" } },
        y: { ticks: { color: PAL.clay }, grid: { color: "rgba(26,23,20,0.06)" } },
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
      datasets: [{
        data: [memory, saved],
        backgroundColor: [PAL.moss, PAL.rust],
        borderColor: PAL.ink,
        borderWidth: 2,
      }],
    },
    options: {
      ...chartDefaults,
      cutout: "62%",
      plugins: { legend: { position: "bottom" } },
    },
  });
}

function renderCumulativeChart(data) {
  destroyChart("cumulative");
  const naive = data.naive?.per_turn_tokens || [];
  const memory = data.memory?.per_turn_tokens || [];
  const naiveCum = naive.reduce((a, v, i) => { a.push((a[i - 1] || 0) + v); return a; }, []);
  const memCum = memory.reduce((a, v, i) => { a.push((a[i - 1] || 0) + v); return a; }, []);
  charts.cumulative = new Chart(document.getElementById("cumulative-chart"), {
    type: "line",
    data: {
      labels: naive.map((_, i) => i + 1),
      datasets: [
        { label: "Naïf cumulé", data: naiveCum, borderColor: PAL.rust, tension: 0.3, fill: false, pointRadius: 0 },
        { label: "MemBridge cumulé", data: memCum, borderColor: PAL.moss, tension: 0.3, fill: false, pointRadius: 0 },
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
  const c = data.memory?.compression_ratio ? Math.max(0, 100 - data.memory.compression_ratio * 200) : 80;
  charts.radar = new Chart(document.getElementById("radar-chart"), {
    type: "radar",
    data: {
      labels: ["Économie", "Qualité", "Stabilité", "Compression"],
      datasets: [{
        label: "MemBridge",
        data: [s, q, g, c],
        backgroundColor: "rgba(47,82,66,0.2)",
        borderColor: PAL.moss,
        borderWidth: 2,
      }],
    },
    options: {
      ...chartDefaults,
      scales: { r: { min: 0, max: 100, ticks: { color: PAL.clay }, grid: { color: "rgba(26,23,20,0.1)" } } },
    },
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
        { label: "MemBridge cumulé", data: mCum, borderColor: PAL.moss, tension: 0.3, fill: false, pointRadius: 0 },
      ],
    },
    options: { ...chartDefaults, scales: { x: { ticks: { color: PAL.clay } }, y: { ticks: { color: PAL.clay } } } },
  });
}

function renderRadarChart(data) {
  destroyChart("radar");
  const q = data.quality?.score_pct || 0;
  const s = Math.min(data.savings_pct || 0, 100);
  const g = data.memory?.growth_factor ? Math.max(0, 100 - data.memory.growth_factor * 30) : 80;
  const c = data.memory?.compression_ratio ? Math.max(0, 100 - data.memory.compression_ratio * 200) : 75;
  charts.radar = new Chart(document.getElementById("radar-chart"), {
    type: "radar",
    data: {
      labels: ["Économie", "Qualité", "Stabilité", "Compression"],
      datasets: [{
        label: "MemBridge",
        data: [s, q, g, c],
        backgroundColor: "rgba(47,82,66,0.2)",
        borderColor: PAL.moss,
        borderWidth: 2,
      }],
    },
    options: {
      ...chartDefaults,
      scales: { r: { min: 0, max: 100, ticks: { display: false }, grid: { color: "rgba(26,23,20,0.1)" } } },
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
      datasets: [{
        label: "Score",
        data: details.map((d) => d.score || 0),
        backgroundColor: details.map((d) => d.passed ? PAL.moss : PAL.rust),
        borderColor: PAL.ink,
        borderWidth: 1,
      }],
    },
    options: {
      ...chartDefaults,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: PAL.clay }, grid: { display: false } },
        y: { min: 0, max: 1, ticks: { color: PAL.clay }, grid: { color: "rgba(26,23,20,0.06)" } },
      },
    },
  });
}

function renderBattleBar(data) {
  const naive = data.naive?.total_tokens || 1;
  const memory = data.memory?.total_tokens || 1;
  const total = naive + memory;
  const naivePct = Math.round((naive / total) * 100);
  const memPct = 100 - naivePct;
  document.getElementById("battle-naive").style.width = naivePct + "%";
  document.getElementById("battle-memory").style.width = memPct + "%";
}

function renderTraps(quality) {
  const list = document.getElementById("trap-list");
  list.innerHTML = "";
  (quality?.details || []).forEach((item) => {
    const div = document.createElement("div");
    div.className = `trap-item ${item.passed ? "ok" : "ko"}`;
    div.innerHTML = `
      <span>${item.query}</span>
      <span class="trap-score">${(item.score || 0).toFixed(3)}</span>
      <span>${item.passed ? "✓" : "✗"} ${item.expected}</span>`;
    list.appendChild(div);
  });
}

function renderTimeline(entries) {
  const el = document.getElementById("memory-timeline");
  el.innerHTML = "";
  (entries || []).forEach((e) => {
    const dot = document.createElement("div");
    dot.className = "timeline-dot";
    dot.title = e.content?.slice(0, 60) || "";
    if (e.tags?.includes("fact")) dot.classList.add("fact");
    else if (e.tags?.includes("geo")) dot.classList.add("geo");
    else if (e.tags?.some((t) => ["audio", "video", "call", "transcript"].includes(t)))
      dot.classList.add("media");
    el.appendChild(dot);
  });
}

function renderInsights(insights) {
  const panel = document.getElementById("insights-panel");
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

function renderReport(data) {
  animateCounter(document.getElementById("naive-tokens"), data.naive.total_tokens);
  animateCounter(document.getElementById("memory-tokens"), data.memory.total_tokens);
  document.getElementById("savings").textContent = `-${data.savings_pct}%`;
  document.getElementById("euros-saved").textContent =
    `${(data.tokens_saved || 0).toLocaleString()} tokens économisés`;
  document.getElementById("quality-score").textContent =
    `${data.quality.passed}/${data.quality.total}`;
  document.getElementById("quality-bar").style.width = `${data.quality.score_pct}%`;
  renderTokenChart(data);
  renderDonutChart(data);
  renderCumulativeChart(data);
  renderRadarChart(data);
  renderTrapChart(data.quality);
  renderBattleBar(data);
  renderTraps(data.quality);
  renderInsights(data.insights);
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
    const mem = await api("/api/memory");
    renderTimeline(mem.entries);
  } catch {
    try {
      const data = await api("/api/report");
      renderReport(data);
    } catch { /* offline */ }
  }
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
  } finally {
    btn.disabled = false;
    btn.textContent = t("run");
  }
}

/* ── Recherche live ── */
document.getElementById("search-btn").onclick = async () => {
  const q = document.getElementById("search-query").value.trim();
  if (!q) return;
  playTick();
  const res = await api(`/api/search?q=${encodeURIComponent(q)}`);
  const box = document.getElementById("search-result");
  if (res.results?.length) {
    const top = res.results[0];
    box.innerHTML = `<strong>Score ${top.score}</strong> — ${top.content}`;
    box.classList.add("visible");
  } else {
    box.textContent = t("no_result");
    box.classList.add("visible");
  }
};

/* ── Audio / Speech ── */
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
    document.getElementById("audio-zone").classList.remove("recording");
    document.getElementById("audio-zone").textContent = t("audio_hint");
  };
}

document.getElementById("audio-zone").onclick = () => {
  if (!recognition) { initSpeech(); }
  if (!recognition) {
    document.getElementById("audio-status").textContent = "Speech API non supportée";
    return;
  }
  if (listening) { recognition.stop(); return; }
  listening = true;
  recognition.lang = lang === "fr" ? "fr-FR" : "en-US";
  document.getElementById("audio-zone").classList.add("recording");
  document.getElementById("audio-zone").innerHTML =
    `<span class="rec-indicator"></span>${t("listening")}`;
  window.AudioViz?.start();
  recognition.start();
};

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

// Export PDF (add button if it doesn't exist)
const pdfBtn = document.createElement("button");
pdfBtn.id = "export-pdf";
pdfBtn.className = "btn ghost";
pdfBtn.textContent = "📄 PDF";
pdfBtn.addEventListener("click", async () => {
  try {
    const res = await fetch("/api/export/pdf");
    if (res.ok) {
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "MemBridge-Report.pdf";
      a.click();
      URL.revokeObjectURL(url);
    }
  } catch (e) {
    console.error("PDF export failed:", e);
  }
});
const controls = document.querySelector(".controls");
if (controls && !document.getElementById("export-pdf")) {
  controls.insertBefore(pdfBtn, controls.lastChild);
}

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
};

/* ── Caméra ── */
document.getElementById("cam-btn").onclick = async () => {
  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    document.getElementById("video-preview").srcObject = mediaStream;
    document.getElementById("video-status").textContent = "Caméra active";
  } catch (e) {
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
    document.getElementById("geo-status").textContent =
      `${latitude.toFixed(4)}, ${longitude.toFixed(4)}`;
    document.getElementById("map-preview").style.backgroundImage =
      `url(https://staticmap.openstreetmap.de/staticmap.php?center=${latitude},${longitude}&zoom=13&size=400x140&markers=${latitude},${longitude},red)`;
    await api("/api/locate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ latitude, longitude, label: "Démo jury" }),
    });
    const mem = await api("/api/memory");
    renderTimeline(mem.entries);
  });
};

/* ── UI ── */
document.getElementById("lang-toggle").onclick = () => {
  lang = lang === "fr" ? "en" : "fr";
  applyI18n();
};

document.getElementById("present-mode").onclick = () => {
  document.body.classList.toggle("present-mode");
};

document.getElementById("run-benchmark").onclick = runBenchmark;

initSpeech();
applyI18n();
loadReport();
