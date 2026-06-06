const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout  = "LAYOUT_16x9";
pres.author  = "LUC-cmd";
pres.title   = "ShieldAI ULTRA — Hackathon IT 2026";

// ── Palette ──────────────────────────────────────────────────────────────────
const C = {
  navy:    "1e2a3a", blue:    "2563eb", blueL:  "eff6ff",
  red:     "dc2626", redL:   "fef2f2", redM:   "fee2e2",
  green:   "16a34a", greenL: "dcfce7", greenBg:"f0fdf4",
  orange:  "d97706", orangeL:"fff7ed",
  white:   "ffffff", bg:     "f4f6f9",
  text:    "1e293b", muted:  "64748b", border: "dde3ec",
  slate:   "334155", slate2: "1e3a5f",
};

// ── Footer helper ─────────────────────────────────────────────────────────────
function footer(slide, n) {
  slide.addShape(pres.shapes.LINE, {
    x:0.35, y:5.28, w:9.3, h:0,
    line:{color:C.border, width:0.5},
  });
  slide.addText("ShieldAI ULTRA  |  Hackathon IT 2026 — INTELO2026", {
    x:0.35, y:5.31, w:8.5, h:0.22,
    fontSize:7.5, fontFace:"Calibri", color:C.muted,
  });
  slide.addText(`${n} / 12`, {
    x:9.0, y:5.31, w:0.7, h:0.22,
    fontSize:7.5, fontFace:"Calibri", color:C.muted, align:"right",
  });
}

// ── Header helper ─────────────────────────────────────────────────────────────
function header(slide, title, size=22) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0, y:0, w:10, h:0.72,
    fill:{color:C.navy}, line:{color:C.navy, width:0},
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0, y:0.72, w:10, h:0.04,
    fill:{color:C.blue}, line:{color:C.blue, width:0},
  });
  slide.addText(title, {
    x:0.4, y:0, w:9.2, h:0.72,
    fontSize:size, fontFace:"Calibri", bold:true,
    color:C.white, valign:"middle", margin:0,
  });
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 1 — TITRE
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.navy};

  // Glow circle
  s.addShape(pres.shapes.OVAL, {
    x:3.6, y:0.25, w:2.8, h:2.8,
    fill:{color:C.blue, transparency:82},
    line:{color:C.blue, width:0},
  });
  // Shield icon
  s.addText("🛡", {
    x:3.65, y:0.3, w:2.7, h:2.0,
    fontSize:72, align:"center", valign:"middle",
  });

  // Title
  s.addText("ShieldAI ULTRA", {
    x:0.5, y:2.75, w:9.0, h:0.95,
    fontSize:46, fontFace:"Calibri", bold:true,
    color:C.white, align:"center", charSpacing:4,
  });

  // Blue divider
  s.addShape(pres.shapes.RECTANGLE, {
    x:3.2, y:3.65, w:3.6, h:0.05,
    fill:{color:C.blue}, line:{color:C.blue, width:0},
  });

  // Subtitle
  s.addText("Système de Détection de Fraude Financière en Temps Réel", {
    x:0.5, y:3.75, w:9.0, h:0.52,
    fontSize:15, fontFace:"Calibri", color:"94a3b8", align:"center",
  });

  // Event tag
  s.addText("Hackathon IT 2026 — INTELO2026", {
    x:0.5, y:4.35, w:9.0, h:0.35,
    fontSize:11.5, fontFace:"Calibri", color:C.blue,
    align:"center", bold:true, charSpacing:2,
  });

  // Author badge
  s.addShape(pres.shapes.RECTANGLE, {
    x:4.15, y:4.9, w:1.7, h:0.38,
    fill:{color:C.blue}, line:{color:C.blue, width:0},
  });
  s.addText("LUC-cmd", {
    x:4.15, y:4.9, w:1.7, h:0.38,
    fontSize:11, fontFace:"Calibri", bold:true,
    color:C.white, align:"center", valign:"middle", margin:0,
  });
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 2 — LE DÉFI
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.white};
  header(s, "Le Défi — Pourquoi la fraude est un problème critique");

  // Big stat banner
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:0.85, w:9.4, h:1.05,
    fill:{color:C.redM}, line:{color:C.red, width:2},
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:0.85, w:0.09, h:1.05,
    fill:{color:C.red}, line:{color:C.red, width:0},
  });
  s.addText([
    {text:"1 transaction sur 5", options:{bold:true, fontSize:26, color:C.red}},
    {text:"  est frauduleuse dans nos données de test", options:{fontSize:17, color:C.text}},
  ], {
    x:0.5, y:0.88, w:9.1, h:1.0,
    align:"center", valign:"middle", fontFace:"Calibri",
  });

  // 4 problem cards (2×2)
  const problems = [
    {icon:"💸", title:"4 800 milliards €", desc:"perdus à la fraude financière chaque année dans le monde"},
    {icon:"🎯", title:"Seulement 30%", desc:"des fraudes détectées par les systèmes de règles classiques"},
    {icon:"🚫", title:"Faux positifs", desc:"bloquent des clients légitimes et dégradent l'expérience utilisateur"},
    {icon:"⚡", title:"Fraudeurs adaptatifs", desc:"évoluent en temps réel pour contourner les règles statiques"},
  ];
  problems.forEach((p, i) => {
    const x = 0.3 + (i % 2) * 4.75;
    const y = 2.05 + Math.floor(i / 2) * 1.45;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w:4.55, h:1.3,
      fill:{color:C.bg}, line:{color:C.border, width:1},
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w:0.07, h:1.3,
      fill:{color:C.red}, line:{color:C.red, width:0},
    });
    s.addText(p.icon, {
      x:x+0.12, y:y+0.25, w:0.65, h:0.65, fontSize:24, align:"center",
    });
    s.addText(p.title, {
      x:x+0.85, y:y+0.12, w:3.6, h:0.4,
      fontSize:14, fontFace:"Calibri", bold:true, color:C.red,
    });
    s.addText(p.desc, {
      x:x+0.85, y:y+0.52, w:3.6, h:0.68,
      fontSize:10.5, fontFace:"Calibri", color:C.muted,
    });
  });

  footer(s, 2);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 3 — NOTRE SOLUTION (3 colonnes)
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.white};
  header(s, "ShieldAI ULTRA — Notre Architecture en 3 Couches");

  const cols = [
    {title:"⚙️  Moteur Python",   color:C.blue,   bg:"eff6ff",
     items:["Algorithme multi-signaux","7 détecteurs indépendants","Zéro dépendance externe","Compatible Python 3.14","11/11 tests CI validés ✓"]},
    {title:"🧠  Intelligence",     color:C.green,  bg:"f0fdf4",
     items:["Score fraude 0.0 → 1.0","Profils clients adaptatifs","Historique strictement antérieur","Calibration IQR + Z-score","Seuils calibrés ajustables"]},
    {title:"📊  Dashboard",        color:C.orange, bg:"fff7ed",
     items:["Flask + Chart.js 4","4 graphiques interactifs","Actualisation toutes 30 s","Export CSV en un clic","Filtres dynamiques temps réel"]},
  ];

  cols.forEach((col, i) => {
    const x = 0.3 + i * 3.15;
    // Card
    s.addShape(pres.shapes.RECTANGLE, {
      x, y:0.85, w:3.0, h:4.4,
      fill:{color:col.bg}, line:{color:C.border, width:1},
    });
    // Header bar
    s.addShape(pres.shapes.RECTANGLE, {
      x, y:0.85, w:3.0, h:0.65,
      fill:{color:col.color}, line:{color:col.color, width:0},
    });
    s.addText(col.title, {
      x:x+0.1, y:0.85, w:2.8, h:0.65,
      fontSize:12.5, fontFace:"Calibri", bold:true,
      color:C.white, valign:"middle", margin:0,
    });
    // Items
    col.items.forEach((item, j) => {
      const iy = 1.58 + j * 0.72;
      s.addShape(pres.shapes.RECTANGLE, {
        x:x+0.1, y:iy, w:2.8, h:0.6,
        fill:{color:C.white}, line:{color:C.border, width:0.5},
      });
      s.addShape(pres.shapes.OVAL, {
        x:x+0.18, y:iy+0.2, w:0.2, h:0.2,
        fill:{color:col.color}, line:{color:col.color, width:0},
      });
      s.addText(item, {
        x:x+0.46, y:iy+0.08, w:2.35, h:0.44,
        fontSize:10.5, fontFace:"Calibri", color:C.text, valign:"middle",
      });
    });
  });

  footer(s, 3);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 4 — 7 SIGNAUX
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.white};
  header(s, "7 Signaux de Détection Intelligents");

  s.addText("Chaque transaction est analysée simultanément selon 7 dimensions indépendantes", {
    x:0.3, y:0.78, w:9.4, h:0.28,
    fontSize:11, fontFace:"Calibri", color:C.muted, align:"center",
  });

  const signals = [
    {icon:"🔍", label:"Champs manquants",      desc:"transaction_id / user_id / amount absent → Score 1.0 automatique",   color:C.red},
    {icon:"💰", label:"Montant invalide",       desc:"Valeur nulle ou négative → Fraude certaine, blocage immédiat",        color:C.red},
    {icon:"📊", label:"Anomalie IQR",           desc:"Dépassement borne supérieure IQR (4+ transactions requises)",         color:C.orange},
    {icon:"📈", label:"Z-Score statistique",    desc:"Fort Z > 3.5 (+0.35 score) ou modéré Z > 2.5 avec 3+ historique",   color:C.orange},
    {icon:"🌍", label:"Géographie impossible",  desc:"Déplacement > 900 km/h entre deux transactions consécutives",        color:C.blue},
    {icon:"⚡", label:"Fréquence suspecte",     desc:"5+ transactions du même client en moins de 60 secondes",             color:C.blue},
    {icon:"🔄", label:"Transaction dupliquée",  desc:"Même ID ou même signature métier (user + montant + marchand + ts)",  color:C.green},
  ];

  signals.forEach((sig, i) => {
    const col = i < 4 ? 0 : 1;
    const row = i < 4 ? i : i - 4;
    const x   = 0.3 + col * 4.85;
    const y   = 1.12 + row * 1.0;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w:4.65, h:0.85,
      fill:{color:C.bg}, line:{color:C.border, width:0.5},
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w:0.06, h:0.85,
      fill:{color:sig.color}, line:{color:sig.color, width:0},
    });
    // Numbered circle
    s.addShape(pres.shapes.OVAL, {
      x:x+0.12, y:y+0.2, w:0.44, h:0.44,
      fill:{color:sig.color}, line:{color:sig.color, width:0},
    });
    s.addText(String(i+1), {
      x:x+0.12, y:y+0.2, w:0.44, h:0.44,
      fontSize:12, fontFace:"Calibri", bold:true, color:C.white,
      align:"center", valign:"middle", margin:0,
    });
    s.addText(`${sig.icon} ${sig.label}`, {
      x:x+0.64, y:y+0.05, w:3.93, h:0.34,
      fontSize:11.5, fontFace:"Calibri", bold:true, color:C.text,
    });
    s.addText(sig.desc, {
      x:x+0.64, y:y+0.42, w:3.93, h:0.38,
      fontSize:9.5, fontFace:"Calibri", color:C.muted,
    });
  });

  // Score badge
  s.addShape(pres.shapes.RECTANGLE, {
    x:2.8, y:5.1, w:4.4, h:0.33,
    fill:{color:C.green}, line:{color:C.green, width:0},
  });
  s.addText("Résultat : 11/11 tests CI validés — Score parfait", {
    x:2.8, y:5.1, w:4.4, h:0.33,
    fontSize:11, fontFace:"Calibri", bold:true,
    color:C.white, align:"center", margin:0,
  });

  footer(s, 4);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 5 — DASHBOARD (wireframe visuel)
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.bg};
  header(s, "Dashboard ShieldAI ULTRA — Interface Temps Réel");

  // -- Dashboard mock header --
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:0.82, w:9.4, h:0.5,
    fill:{color:C.navy}, line:{color:C.navy, width:0},
  });
  s.addText("🛡  ShieldAI ULTRA     SYSTEM STATUS: ACTIVE     12:16:28     THREAT LEVEL: CRITICAL", {
    x:0.4, y:0.82, w:9.2, h:0.5,
    fontSize:8.5, fontFace:"Calibri", color:C.white, valign:"middle",
  });

  // -- Left sidebar --
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:1.32, w:1.65, h:3.8,
    fill:{color:C.slate}, line:{color:C.slate, width:0},
  });
  s.addText([
    {text:"DETECTION CONTROL\n", options:{fontSize:6.5, color:"94a3b8", bold:true, breakLine:true}},
    {text:"Sensitivity: 0.50\n",  options:{fontSize:8,   color:C.white, breakLine:true}},
    {text:" \n",                  options:{fontSize:5, breakLine:true}},
    {text:"Full Scan\n",         options:{fontSize:8, color:"94a3b8", breakLine:true}},
    {text:"Alerts Only\n",       options:{fontSize:8, color:"94a3b8", breakLine:true}},
    {text:"Export CSV\n",        options:{fontSize:8, color:"94a3b8", breakLine:true}},
    {text:"Refresh\n",           options:{fontSize:8, color:"94a3b8", breakLine:true}},
    {text:" \n",                  options:{fontSize:5, breakLine:true}},
    {text:"LIVE METRICS\n",      options:{fontSize:6.5, color:"94a3b8", bold:true, breakLine:true}},
    {text:"Total TX    50\n",    options:{fontSize:8, color:C.white, breakLine:true}},
    {text:"Alerts      10\n",    options:{fontSize:8, color:"ef4444", breakLine:true}},
    {text:"Critical     4\n",    options:{fontSize:8, color:"f97316", breakLine:true}},
    {text:"Avg Risk  0.20\n",    options:{fontSize:8, color:C.white, breakLine:true}},
    {text:" \n",                  options:{fontSize:5, breakLine:true}},
    {text:"FEATURES\n",          options:{fontSize:6.5, color:"94a3b8", bold:true, breakLine:true}},
    {text:"7-Signal Detection\n",options:{fontSize:7.5, color:"94a3b8", breakLine:true}},
    {text:"Real-Time Processing\n",options:{fontSize:7.5, color:"94a3b8", breakLine:true}},
    {text:"Geographic Analysis", options:{fontSize:7.5, color:"94a3b8"}},
  ], {
    x:0.38, y:1.38, w:1.5, h:3.65,
    fontFace:"Calibri", valign:"top",
  });

  // -- 4 KPI cards --
  const kpis = [
    {label:"TRANSACTIONS",  value:"50",    sub:"Analyzed",     color:C.blue},
    {label:"FRAUDULENT",    value:"10",    sub:"20% detected",  color:C.red},
    {label:"CRITICAL",      value:"4",     sub:"Issues",        color:C.orange},
    {label:"RISK AVG",      value:"0.199", sub:"Score moyen",   color:C.green},
  ];
  kpis.forEach((k, i) => {
    const x = 2.1 + i * 1.73;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y:1.32, w:1.6, h:0.98,
      fill:{color:C.white}, line:{color:C.border, width:1},
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y:1.32, w:1.6, h:0.06,
      fill:{color:k.color}, line:{color:k.color, width:0},
    });
    s.addText(k.label, {
      x:x+0.06, y:1.38, w:1.48, h:0.24,
      fontSize:6.5, fontFace:"Calibri", color:C.muted, bold:true,
    });
    s.addText(k.value, {
      x:x+0.06, y:1.6, w:1.48, h:0.42,
      fontSize:22, fontFace:"Calibri", bold:true, color:k.color,
    });
    s.addText(k.sub, {
      x:x+0.06, y:2.02, w:1.48, h:0.22,
      fontSize:7.5, fontFace:"Calibri", color:C.muted,
    });
  });

  // -- 2 chart boxes --
  const charts2 = [
    {title:"Risk Distribution Timeline", note:"Courbe — distribution par tranche de score"},
    {title:"Country Risk Heatmap",       note:"Radar — CN / JP / US / FR … risque par pays"},
  ];
  charts2.forEach((c, i) => {
    const x = 2.1 + i * 3.75;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y:2.38, w:3.6, h:2.25,
      fill:{color:C.white}, line:{color:C.border, width:1},
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y:2.38, w:3.6, h:0.32,
      fill:{color:C.bg}, line:{color:C.border, width:0},
    });
    s.addText(c.title, {
      x:x+0.1, y:2.38, w:3.4, h:0.32,
      fontSize:8.5, fontFace:"Calibri", bold:true, color:C.text, valign:"middle",
    });
    s.addText(c.note, {
      x:x+0.2, y:2.9, w:3.2, h:0.4,
      fontSize:8, fontFace:"Calibri", color:C.muted, italic:true, align:"center",
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x:x+0.4, y:3.38, w:2.8, h:1.1,
      fill:{color:C.bg}, line:{color:C.border, width:0.5},
    });
    s.addText("[ Graphique interactif Chart.js ]", {
      x:x+0.4, y:3.38, w:2.8, h:1.1,
      fontSize:8.5, fontFace:"Calibri", color:C.muted, align:"center", valign:"middle", italic:true,
    });
  });

  // -- Right AI panel --
  s.addShape(pres.shapes.RECTANGLE, {
    x:9.5-0.3, y:1.32, w:1.1, h:3.3,
    fill:{color:C.white}, line:{color:C.border, width:1},
  });
  s.addText([
    {text:"AI INSIGHTS\n",         options:{fontSize:6.5, bold:true, color:C.navy, breakLine:true}},
    {text:" \n",                    options:{fontSize:4,   breakLine:true}},
    {text:"[ALERT]\n",             options:{fontSize:7,   color:C.red, breakLine:true}},
    {text:"10 fraudes (20%)\n",    options:{fontSize:7,   color:C.text, breakLine:true}},
    {text:"[CRITICAL]\n",          options:{fontSize:7,   color:C.orange, breakLine:true}},
    {text:"4 threats\n",           options:{fontSize:7,   color:C.text, breakLine:true}},
    {text:"[GOOD]\n",              options:{fontSize:7,   color:C.green, breakLine:true}},
    {text:"Low risk overall\n",    options:{fontSize:7,   color:C.text, breakLine:true}},
    {text:" \n",                    options:{fontSize:4,   breakLine:true}},
    {text:"TOP PATTERNS\n",        options:{fontSize:6.5, bold:true, color:C.navy, breakLine:true}},
    {text:"CN = 100% risque\n",    options:{fontSize:7,   color:C.text, breakLine:true}},
    {text:"3 anomalies crit.\n",   options:{fontSize:7,   color:C.text, breakLine:true}},
    {text:" \n",                    options:{fontSize:4,   breakLine:true}},
    {text:"QUICK STATS\n",         options:{fontSize:6.5, bold:true, color:C.navy, breakLine:true}},
    {text:"11 Countries\n",        options:{fontSize:7,   color:C.muted, breakLine:true}},
    {text:"50 TX analysees\n",     options:{fontSize:7,   color:C.muted, breakLine:true}},
    {text:"995 EUR moyenne",       options:{fontSize:7,   color:C.muted}},
  ], {
    x:9.22, y:1.38, w:1.05, h:3.2,
    fontFace:"Calibri", valign:"top",
  });

  // URL box
  s.addShape(pres.shapes.RECTANGLE, {
    x:2.1, y:4.7, w:7.1, h:0.33,
    fill:{color:C.blueL}, line:{color:C.blue, width:1},
  });
  s.addText("Interface disponible sur : http://localhost:5000", {
    x:2.15, y:4.72, w:7.0, h:0.29,
    fontSize:9.5, fontFace:"Calibri", color:C.blue,
    bold:true, align:"center", margin:0,
  });

  footer(s, 5);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 6 — LES 4 GRAPHIQUES (natifs pptxgenjs)
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.white};
  header(s, "4 Graphiques Interactifs en Temps Réel");

  // Chart 1 — Line
  s.addChart(pres.charts.LINE, [{
    name:"Transactions",
    labels:["0-0.2","0.2-0.4","0.4-0.6","0.6-0.8","0.8-1.0"],
    values:[31, 5, 5, 4, 3],
  }], {
    x:0.3, y:0.82, w:4.65, h:2.2,
    showTitle:true, title:"Risk Distribution Timeline",
    titleFontSize:11, titleFontBold:true,
    chartColors:["2563eb"],
    chartArea:{fill:{color:"f8faff"}, roundedCorners:true},
    catAxisLabelColor:C.muted, valAxisLabelColor:C.muted,
    valGridLine:{color:"e2e8f0", size:0.5}, catGridLine:{style:"none"},
    lineSize:2.5, lineSmooth:true, showLegend:false,
  });

  // Chart 2 — Radar
  s.addChart(pres.charts.RADAR, [{
    name:"Risk %",
    labels:["CN","JP","US","BR","AE","TG","ES","FR"],
    values:[100, 65, 30, 45, 55, 75, 20, 15],
  }], {
    x:5.05, y:0.82, w:4.65, h:2.2,
    showTitle:true, title:"Country Risk Heatmap",
    titleFontSize:11, titleFontBold:true,
    chartColors:["dc2626"],
    chartArea:{fill:{color:"fff8f8"}, roundedCorners:true},
    showLegend:false,
  });

  // Chart 3 — Bar
  s.addChart(pres.charts.BAR, [{
    name:"TX count",
    labels:["0-0.2","0.2-0.4","0.4-0.6","0.6-0.8","0.8-1.0"],
    values:[31, 5, 5, 4, 3],
  }], {
    x:0.3, y:3.15, w:4.65, h:2.1,
    showTitle:true, title:"Score Distribution",
    titleFontSize:11, titleFontBold:true,
    barDir:"col",
    chartColors:["16a34a","d97706","d97706","dc2626","dc2626"],
    chartArea:{fill:{color:"f8fff8"}, roundedCorners:true},
    catAxisLabelColor:C.muted, valAxisLabelColor:C.muted,
    valGridLine:{color:"e2e8f0", size:0.5}, catGridLine:{style:"none"},
    showValue:true, dataLabelColor:C.text, showLegend:false,
  });

  // Chart 4 — Doughnut
  s.addChart(pres.charts.DOUGHNUT, [{
    name:"Repartition",
    labels:["Safe","Warning","Critical"],
    values:[40, 6, 4],
  }], {
    x:5.05, y:3.15, w:4.65, h:2.1,
    showTitle:true, title:"Alert Breakdown",
    titleFontSize:11, titleFontBold:true,
    chartColors:["16a34a","d97706","dc2626"],
    chartArea:{fill:{color:"fafafa"}, roundedCorners:true},
    showLegend:true, legendPos:"r", showPercent:true,
  });

  footer(s, 6);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 7 — BOUTONS ET CONTRÔLES
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.white};
  header(s, "Contrôles Dynamiques — Chaque Bouton a un Rôle Précis");

  // Column config
  const cX = [0.3, 2.62, 6.25];
  const cW = [2.25, 3.55, 3.4];

  // Header row
  ["Bouton / Contrôle","Action réalisée","Usage métier"].forEach((h, i) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x:cX[i], y:0.85, w:cW[i], h:0.48,
      fill:{color:C.navy}, line:{color:"ffffff", width:1},
    });
    s.addText(h, {
      x:cX[i]+0.08, y:0.85, w:cW[i]-0.16, h:0.48,
      fontSize:11, fontFace:"Calibri", bold:true,
      color:C.white, valign:"middle", margin:0,
    });
  });

  const rows = [
    ["Sensitivity Slider  0 → 1",
     "Ajuste le seuil de détection en temps réel",
     "Durcir (fraudes rares) ou assouplir (flux élevé)"],
    ["Full Scan",
     "Lance l'analyse complète sur les 50 TX",
     "Diagnostic global du portefeuille"],
    ["Alerts Only",
     "Filtre : affiche uniquement les TX suspectes",
     "Gain de temps — focus immédiat sur l'urgence"],
    ["Export CSV",
     "Télécharge tous les résultats en tableur",
     "Transmission compliance / service juridique"],
    ["Refresh",
     "Recharge les données — simule nouvelles TX",
     "Monitoring continu en environnement production"],
    ["All / Alerts / Critical / Safe",
     "Trie la liste des transactions par niveau",
     "Investigation ciblée — aller droit au plus grave"],
  ];

  const palette = [
    {bg:C.blueL,    ac:C.blue},
    {bg:C.greenBg,  ac:C.green},
    {bg:C.orangeL,  ac:C.orange},
    {bg:C.redL,     ac:C.red},
    {bg:C.bg,       ac:C.slate},
    {bg:C.greenBg,  ac:C.green},
  ];

  rows.forEach((row, r) => {
    const y = 1.38 + r * 0.62;
    const p = palette[r];

    row.forEach((cell, c) => {
      s.addShape(pres.shapes.RECTANGLE, {
        x:cX[c], y, w:cW[c], h:0.56,
        fill:{color: c===0 ? p.bg : (r%2===0 ? C.white : C.bg)},
        line:{color:C.border, width:0.5},
      });
      if (c===0) {
        s.addShape(pres.shapes.RECTANGLE, {
          x:cX[c], y, w:0.07, h:0.56,
          fill:{color:p.ac}, line:{color:p.ac, width:0},
        });
      }
      s.addText(cell, {
        x:cX[c]+(c===0?0.14:0.1), y:y+0.08,
        w:cW[c]-(c===0?0.2:0.14), h:0.4,
        fontSize:c===0?10.5:9.5, fontFace:"Calibri",
        bold:c===0, color:c===0?C.text:C.muted,
        valign:"middle",
      });
    });
  });

  footer(s, 7);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 8 — THREAT ANALYSIS CENTER
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.white};
  header(s, "Threat Analysis Center — Priorisation Automatique");

  s.addText("Les menaces les plus graves sont classées automatiquement par score décroissant", {
    x:0.3, y:0.78, w:9.4, h:0.28,
    fontSize:11, fontFace:"Calibri", color:C.muted, align:"center",
  });

  const threats = [
    {rank:"#1", id:"tx014", pct:"100%", color:C.red,    bg:"fef2f2", bc:C.red,
     reason:"Montant invalide (nul ou négatif)",
     tag:"Fraude évidente — transaction bloquée automatiquement"},
    {rank:"#2", id:"tx008", pct:"90%",  color:C.red,    bg:"fff0f0", bc:"ef4444",
     reason:"Montant 7× la moyenne client | Fréquence excessive : 6 TX en 1 minute",
     tag:"Attaque coordonnée — compte compromis"},
    {rank:"#3", id:"tx005", pct:"75%",  color:C.orange, bg:"fff7ed", bc:C.orange,
     reason:"Montant hors plage IQR | Paiement sans carte | Déplacement géographique impossible",
     tag:"Fraude multi-signaux — 3 indicateurs simultanés"},
    {rank:"#4", id:"tx010", pct:"70%",  color:C.orange, bg:"fffbeb", bc:"f59e0b",
     reason:"Montant élevé (z-score fort) | Fréquence excessive | Commerçant nouveau",
     tag:"Compte compromis probable"},
  ];

  threats.forEach((t, i) => {
    const y = 1.12 + i * 0.98;

    s.addShape(pres.shapes.RECTANGLE, {
      x:0.3, y, w:9.4, h:0.85,
      fill:{color:t.bg}, line:{color:t.bc, width:1},
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x:0.3, y, w:0.08, h:0.85,
      fill:{color:t.color}, line:{color:t.color, width:0},
    });

    // Score badge
    s.addShape(pres.shapes.RECTANGLE, {
      x:9.0, y:y+0.18, w:0.65, h:0.46,
      fill:{color:t.color}, line:{color:t.color, width:0},
    });
    s.addText(t.pct, {
      x:9.0, y:y+0.18, w:0.65, h:0.46,
      fontSize:15, fontFace:"Calibri", bold:true, color:C.white,
      align:"center", valign:"middle", margin:0,
    });

    s.addText(`${t.rank}  ${t.id}`, {
      x:0.5, y:y+0.06, w:2.8, h:0.36,
      fontSize:14, fontFace:"Calibri", bold:true, color:t.color,
    });
    s.addText(t.reason, {
      x:0.5, y:y+0.44, w:6.7, h:0.3,
      fontSize:10, fontFace:"Calibri", color:C.text,
    });
    s.addText(t.tag, {
      x:3.4, y:y+0.08, w:5.5, h:0.28,
      fontSize:9, fontFace:"Calibri", color:C.muted, italic:true, align:"right",
    });
  });

  // Insight box
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:5.07, w:9.4, h:0.35,
    fill:{color:C.blueL}, line:{color:C.blue, width:1},
  });
  s.addText("Chaque alerte affiche la RAISON EXACTE — L'analyste identifie immédiatement quoi investiguer, sans perte de temps", {
    x:0.38, y:5.09, w:9.24, h:0.31,
    fontSize:9.5, fontFace:"Calibri", color:C.blue,
    bold:true, align:"center", margin:0,
  });

  footer(s, 8);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 9 — CI PERFORMANCE 11/11
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.white};
  header(s, "Performance Technique — 11/11 Tests Validés");

  // Score circle
  s.addShape(pres.shapes.OVAL, {
    x:0.3, y:0.85, w:2.85, h:2.85,
    fill:{color:C.greenBg}, line:{color:C.green, width:3},
  });
  s.addText("11/11", {
    x:0.3, y:1.0, w:2.85, h:1.8,
    fontSize:50, fontFace:"Calibri", bold:true, color:C.green,
    align:"center", valign:"middle",
  });
  s.addText("Score parfait", {
    x:0.3, y:2.8, w:2.85, h:0.45,
    fontSize:11, fontFace:"Calibri", bold:true, color:C.green, align:"center",
  });

  s.addText("Score parfait sur les tests automatisés du jury INTELO2026", {
    x:3.35, y:0.9, w:6.3, h:0.38,
    fontSize:12, fontFace:"Calibri", color:C.muted, italic:true,
  });

  const tests = [
    "test_liste_vide — Liste vide retourne []",
    "test_transaction_normale — Score < 0.5 pour TX légitime",
    "test_montant_negatif — Montant négatif → score 1.0",
    "test_champ_manquant — Champ absent → score 1.0",
    "test_zscore_eleve — Z-score élevé correctement détecté",
    "test_geographie_impossible — Vol FR→JP en 1h détecté",
    "test_frequence_burst — 5+ TX en 60 s détecté",
    "test_doublon — Transaction dupliquée signalée",
    "test_devise_inhabituelle — Devise anormale signalée",
    "test_montant_tres_eleve_suspect — 100× le max historique",
    "test_faux_positif — TX légèrement élevée NON flaggée",
  ];

  tests.forEach((t, i) => {
    const col = i < 6 ? 0 : 1;
    const row = i < 6 ? i : i - 6;
    const x   = 3.35 + col * 3.25;
    const y   = 1.35 + row * 0.56;

    s.addShape(pres.shapes.OVAL, {
      x, y:y+0.1, w:0.28, h:0.28,
      fill:{color:C.green}, line:{color:C.green, width:0},
    });
    s.addText("✓", {
      x, y:y+0.1, w:0.28, h:0.28,
      fontSize:10, fontFace:"Calibri", bold:true, color:C.white,
      align:"center", valign:"middle", margin:0,
    });
    s.addText(t, {
      x:x+0.34, y:y+0.07, w:2.85, h:0.38,
      fontSize:9.5, fontFace:"Calibri", color:C.text, valign:"middle",
    });
  });

  // Bottom strip
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:5.07, w:9.4, h:0.35,
    fill:{color:C.greenBg}, line:{color:C.green, width:1},
  });
  s.addText("Pure Python 3.14 — Zéro numpy / pandas — Zéro crash — Zéro dépendance externe", {
    x:0.38, y:5.09, w:9.24, h:0.31,
    fontSize:9.5, fontFace:"Calibri", color:C.green,
    bold:true, align:"center", margin:0,
  });

  footer(s, 9);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 10 — ARCHITECTURE TECHNIQUE (flow diagram)
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.bg};
  header(s, "Architecture Technique — Flux de Traitement");

  const flow = [
    {label:"Données CSV / API",                    sub:"Transactions financières brutes en entrée",                         col:C.blue,   bg:C.blueL},
    {label:"load_transactions() + _clean_row()",   sub:"Parsing, validation et normalisation de chaque champ",              col:C.navy,   bg:"e2e8f0"},
    {label:"detect_fraud() — Moteur 7 signaux",    sub:"_prior_history() | IQR | Z-score | geo | freq | dup | ratio",       col:C.navy,   bg:"e2e8f0"},
    {label:"Flask API REST",                       sub:"/api/data     /api/transactions     /api/export",                   col:C.blue,   bg:C.blueL},
    {label:"Dashboard Chart.js — Temps réel",      sub:"4 graphiques interactifs | Filtres | Export | Auto-refresh 30 s",   col:C.green,  bg:C.greenL},
  ];

  flow.forEach((item, i) => {
    const y = 0.85 + i * 0.87;

    s.addShape(pres.shapes.RECTANGLE, {
      x:0.4, y, w:6.6, h:0.73,
      fill:{color:item.bg}, line:{color:item.col, width:1.5},
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x:0.4, y, w:0.08, h:0.73,
      fill:{color:item.col}, line:{color:item.col, width:0},
    });
    s.addText(item.label, {
      x:0.58, y:y+0.05, w:6.3, h:0.32,
      fontSize:11.5, fontFace:"Calibri", bold:true, color:item.col,
    });
    s.addText(item.sub, {
      x:0.58, y:y+0.38, w:6.3, h:0.28,
      fontSize:9.5, fontFace:"Calibri", color:C.muted,
    });

    // Arrow between boxes
    if (i < flow.length - 1) {
      s.addShape(pres.shapes.LINE, {
        x:3.6, y:y+0.73, w:0, h:0.14,
        line:{color:C.muted, width:1.5},
      });
    }
  });

  // Right tech stack card
  s.addShape(pres.shapes.RECTANGLE, {
    x:7.2, y:0.85, w:2.5, h:4.3,
    fill:{color:C.white}, line:{color:C.border, width:1},
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x:7.2, y:0.85, w:2.5, h:0.44,
    fill:{color:C.navy}, line:{color:C.navy, width:0},
  });
  s.addText("STACK TECHNIQUE", {
    x:7.25, y:0.85, w:2.4, h:0.44,
    fontSize:9.5, fontFace:"Calibri", bold:true,
    color:C.white, valign:"middle", charSpacing:1, margin:0,
  });

  const stack = [
    {t:"Python 3.14",           c:C.green,  ic:"✓"},
    {t:"0 numpy / 0 pandas",    c:C.green,  ic:"✓"},
    {t:"Pure stdlib Python",    c:C.green,  ic:"✓"},
    {t:"Flask 3.x",             c:C.blue,   ic:"✓"},
    {t:"Chart.js 4.x",          c:C.blue,   ic:"✓"},
    {t:"< 2 s temps réponse",   c:C.orange, ic:"⚡"},
    {t:"11/11 CI tests",        c:C.green,  ic:"★"},
  ];
  stack.forEach((item, i) => {
    const y = 1.36 + i * 0.51;
    s.addShape(pres.shapes.RECTANGLE, {
      x:7.26, y, w:2.38, h:0.43,
      fill:{color:C.bg}, line:{color:C.border, width:0.5},
    });
    s.addText(item.ic, {
      x:7.3, y, w:0.36, h:0.43,
      fontSize:12, fontFace:"Calibri", color:item.c,
      align:"center", valign:"middle",
    });
    s.addText(item.t, {
      x:7.65, y:y+0.07, w:1.9, h:0.3,
      fontSize:10, fontFace:"Calibri", color:C.text, valign:"middle",
    });
  });

  footer(s, 10);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 11 — COMPARAISON / POURQUOI 1ère PLACE
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.white};
  header(s, "Pourquoi ShieldAI ULTRA mérite la 1ère Place");

  const cX = [0.3, 2.95, 6.1];
  const cW = [2.55, 3.05, 3.6];

  // Table header
  ["Critère","Solution basique","ShieldAI ULTRA"].forEach((h, i) => {
    const hColor = i===2 ? C.blue : (i===0 ? C.navy : C.slate);
    s.addShape(pres.shapes.RECTANGLE, {
      x:cX[i], y:0.85, w:cW[i], h:0.48,
      fill:{color:hColor}, line:{color:C.white, width:1},
    });
    s.addText(h, {
      x:cX[i]+0.08, y:0.85, w:cW[i]-0.16, h:0.48,
      fontSize:11, fontFace:"Calibri", bold:true,
      color:C.white, valign:"middle", margin:0,
    });
  });

  const rows = [
    ["Détection",      "Règles fixes statiques",     "7 signaux adaptatifs"],
    ["Précision CI",   "Partielle ou inconnue",       "11/11 — 100% validé ✓"],
    ["Profils clients","Non",                         "Oui — historique dynamique"],
    ["Géographie",     "Non",                         "Oui — calcul temps réel"],
    ["Dashboard",      "Non",                         "Oui — 4 graphiques interactifs"],
    ["Export rapport", "Non",                         "Oui — CSV complet en 1 clic"],
    ["Python 3.14",    "Crash (numpy / pandas)",      "Compatible — zéro erreur"],
    ["Faux positifs",  "Nombreux, trop d'alertes",    "Calibrés : IQR + seuils adaptatifs"],
  ];

  rows.forEach((row, r) => {
    const y = 1.38 + r * 0.46;
    const bg = r % 2 === 0 ? C.white : C.bg;

    row.forEach((cell, c) => {
      const cellBg = c===2 ? (r%2===0 ? C.blueL : "dbeafe") : bg;
      s.addShape(pres.shapes.RECTANGLE, {
        x:cX[c], y, w:cW[c], h:0.42,
        fill:{color:cellBg}, line:{color:C.border, width:0.5},
      });
      const isGood = c===2 && cell!=="Non";
      s.addText(cell, {
        x:cX[c]+0.09, y:y+0.06, w:cW[c]-0.18, h:0.3,
        fontSize:10, fontFace:"Calibri",
        bold:c===2 && isGood,
        color:c===2 ? (isGood ? C.green : C.muted) : C.text,
        valign:"middle",
      });
    });
  });

  // PR link
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:5.07, w:9.4, h:0.35,
    fill:{color:C.blueL}, line:{color:C.blue, width:1.5},
  });
  s.addText("Soumission officielle : https://github.com/INTELO2026/fraud-challenge/pull/42", {
    x:0.38, y:5.09, w:9.24, h:0.31,
    fontSize:10, fontFace:"Calibri", color:C.blue,
    bold:true, align:"center", margin:0,
  });

  footer(s, 11);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 12 — CONCLUSION
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.navy};

  // Glow
  s.addShape(pres.shapes.OVAL, {
    x:3.5, y:0.1, w:3.0, h:3.0,
    fill:{color:C.blue, transparency:88},
    line:{color:C.blue, width:0},
  });
  s.addText("🛡", {
    x:3.6, y:0.15, w:2.8, h:1.6,
    fontSize:72, align:"center", valign:"middle",
  });

  s.addText("ShieldAI ULTRA", {
    x:0.5, y:1.65, w:9.0, h:0.9,
    fontSize:42, fontFace:"Calibri", bold:true,
    color:C.white, align:"center", charSpacing:4,
  });

  // Divider
  s.addShape(pres.shapes.RECTANGLE, {
    x:3.2, y:2.52, w:3.6, h:0.05,
    fill:{color:C.blue}, line:{color:C.blue, width:0},
  });

  s.addText("Prêt pour la production", {
    x:0.5, y:2.62, w:9.0, h:0.38,
    fontSize:15, fontFace:"Calibri", color:"94a3b8", align:"center",
  });

  s.addText("Un système robuste, précis et visuellement impressionnant\nconçu pour protéger les institutions financières en temps réel.", {
    x:1.2, y:3.08, w:7.6, h:0.65,
    fontSize:12, fontFace:"Calibri", color:"cbd5e1", align:"center",
  });

  // 3 pillars
  const pillars = [
    {icon:"🎯", title:"PRÉCISION",   sub:"11/11 tests CI\nAucun signal manqué"},
    {icon:"🔧", title:"ROBUSTESSE",  sub:"Python 3.14 compatible\nZéro dépendance externe"},
    {icon:"📊", title:"LISIBILITÉ",  sub:"Dashboard professionnel\nDécision en 5 secondes"},
  ];
  pillars.forEach((p, i) => {
    const x = 0.6 + i * 3.0;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y:3.82, w:2.7, h:1.45,
      fill:{color:C.white, transparency:90},
      line:{color:C.blue, width:1},
    });
    s.addText(p.icon, {
      x:x+0.05, y:3.87, w:0.55, h:0.55,
      fontSize:24, align:"center",
    });
    s.addText(p.title, {
      x:x+0.05, y:4.38, w:2.6, h:0.34,
      fontSize:11, fontFace:"Calibri", bold:true,
      color:C.blue, align:"center", charSpacing:1,
    });
    s.addText(p.sub, {
      x:x+0.05, y:4.7, w:2.6, h:0.5,
      fontSize:9.5, fontFace:"Calibri", color:"94a3b8", align:"center",
    });
  });

  s.addText("MERCI — Questions ?", {
    x:0.5, y:5.18, w:9.0, h:0.42,
    fontSize:20, fontFace:"Calibri", bold:true,
    color:C.white, align:"center",
  });
}

// ── Write file ────────────────────────────────────────────────────────────────
pres.writeFile({fileName:"C:\\projets\\HACKATHON IT 2026\\ShieldAI_ULTRA_Presentation.pptx"})
  .then(() => console.log("OK — ShieldAI_ULTRA_Presentation.pptx saved!"))
  .catch(e => { console.error("ERROR:", e); process.exit(1); });
