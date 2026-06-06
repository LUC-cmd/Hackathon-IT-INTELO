const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "LUC-cmd";
pres.title  = "ShieldAI ULTRA — Hackathon IT 2026";

// ── Palette ─────────────────────────────────────────────────────────────────
const C = {
  navy:"1e2a3a", blue:"2563eb", blueL:"eff6ff", blueMid:"dbeafe",
  red:"dc2626",  redL:"fef2f2", redM:"fee2e2",
  green:"16a34a",greenL:"dcfce7",greenBg:"f0fdf4",
  orange:"d97706",orangeL:"fff7ed",
  white:"ffffff", bg:"f4f6f9",
  text:"1e293b",  muted:"64748b", border:"dde3ec",
  slate:"334155", yellow:"fefce8", yellowB:"ca8a04",
};

// ── "En clair" strip helper — explication simple pour tout le monde ─────────
function enclair(slide, txt) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:4.86, w:9.4, h:0.38,
    fill:{color:"fefce8"}, line:{color:C.yellowB, width:1.2},
  });
  slide.addText([
    {text:"💡 En clair : ", options:{bold:true, color:C.yellowB, fontSize:9.5}},
    {text:txt,              options:{color:C.text,    fontSize:9.5}},
  ], {
    x:0.38, y:4.87, w:9.22, h:0.36,
    fontFace:"Calibri", valign:"middle", margin:0,
  });
}

// ── Footer ───────────────────────────────────────────────────────────────────
function footer(slide, n) {
  slide.addShape(pres.shapes.LINE, {
    x:0.35, y:5.3, w:9.3, h:0,
    line:{color:C.border, width:0.5},
  });
  slide.addText("ShieldAI ULTRA  |  Hackathon IT 2026 — INTELO2026", {
    x:0.35, y:5.33, w:8.5, h:0.2,
    fontSize:7.5, fontFace:"Calibri", color:C.muted,
  });
  slide.addText(`${n} / 15`, {
    x:9.0, y:5.33, w:0.7, h:0.2,
    fontSize:7.5, fontFace:"Calibri", color:C.muted, align:"right",
  });
}

// ── Header ───────────────────────────────────────────────────────────────────
function header(slide, title, sz=22) {
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
    fontSize:sz, fontFace:"Calibri", bold:true,
    color:C.white, valign:"middle", margin:0,
  });
}

// ── Callout helper (annotation flottante) ────────────────────────────────────
function callout(slide, txt, x, y, w=2.2, color=C.blue) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h:0.4,
    fill:{color:C.blueL}, line:{color:color, width:1},
  });
  slide.addText(txt, {
    x:x+0.06, y:y+0.04, w:w-0.12, h:0.32,
    fontSize:8.5, fontFace:"Calibri", color:color,
    valign:"middle", italic:true,
  });
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 1 — TITRE
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.navy};

  s.addShape(pres.shapes.OVAL, {
    x:3.6, y:0.22, w:2.8, h:2.8,
    fill:{color:C.blue, transparency:82},
    line:{color:C.blue, width:0},
  });
  s.addText("🛡", {
    x:3.65, y:0.28, w:2.7, h:1.9,
    fontSize:72, align:"center", valign:"middle",
  });

  s.addText("ShieldAI ULTRA", {
    x:0.5, y:2.7, w:9.0, h:0.9,
    fontSize:46, fontFace:"Calibri", bold:true,
    color:C.white, align:"center", charSpacing:4,
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x:3.2, y:3.57, w:3.6, h:0.05,
    fill:{color:C.blue}, line:{color:C.blue, width:0},
  });

  // Subtitle — ce que le système fait, en langage simple
  s.addText("Système de Détection de Fraude Financière en Temps Réel", {
    x:0.5, y:3.68, w:9.0, h:0.45,
    fontSize:15, fontFace:"Calibri", color:"94a3b8", align:"center",
  });

  // Phrase simple pour n'importe qui
  s.addShape(pres.shapes.RECTANGLE, {
    x:1.5, y:4.2, w:7.0, h:0.55,
    fill:{color:C.white, transparency:90},
    line:{color:C.blue, width:1},
  });
  s.addText("Un gardien automatique qui surveille chaque paiement bancaire et lève l'alarme si quelque chose est anormal — 24h/24, 7j/7.", {
    x:1.6, y:4.22, w:6.8, h:0.51,
    fontSize:11, fontFace:"Calibri", color:C.white,
    align:"center", valign:"middle", italic:true,
  });

  s.addText("Hackathon IT 2026 — INTELO2026", {
    x:0.5, y:4.88, w:9.0, h:0.3,
    fontSize:11, fontFace:"Calibri", color:C.blue,
    align:"center", bold:true, charSpacing:2,
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x:4.15, y:5.22, w:1.7, h:0.35,
    fill:{color:C.blue}, line:{color:C.blue, width:0},
  });
  s.addText("LUC-cmd", {
    x:4.15, y:5.22, w:1.7, h:0.35,
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

  // Bannière choc
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:0.82, w:9.4, h:1.0,
    fill:{color:C.redM}, line:{color:C.red, width:2},
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:0.82, w:0.09, h:1.0,
    fill:{color:C.red}, line:{color:C.red, width:0},
  });
  s.addText([
    {text:"1 transaction sur 5", options:{bold:true, fontSize:26, color:C.red}},
    {text:"  est frauduleuse dans nos données", options:{fontSize:17, color:C.text}},
  ], {
    x:0.5, y:0.85, w:9.1, h:0.95,
    align:"center", valign:"middle", fontFace:"Calibri",
  });

  // Annotation bannière
  callout(s, "= 10 fraudes sur 50 TX analysées", 6.3, 1.85, 3.35, C.red);

  // 4 cartes problèmes
  const problems = [
    {icon:"💸", title:"4 800 milliards €", desc:"perdus à la fraude financière chaque année dans le monde entier",
     note:"= le PIB de l'Allemagne perdu à cause des fraudeurs"},
    {icon:"🎯", title:"Seulement 30%", desc:"des fraudes détectées par les anciens systèmes à règles fixes",
     note:"= 70% des fraudes passent entre les mailles du filet"},
    {icon:"🚫", title:"Faux positifs", desc:"bloquent des clients honnêtes qui font des achats légitimes",
     note:"= votre carte bloquée alors que c'est bien vous qui payez"},
    {icon:"⚡", title:"Fraudeurs adaptatifs", desc:"changent de technique chaque jour pour contourner les règles",
     note:"= les règles d'hier ne protègent pas contre les fraudes d'aujourd'hui"},
  ];

  problems.forEach((p, i) => {
    const x = 0.3 + (i%2)*4.75;
    const y = 2.0  + Math.floor(i/2)*1.42;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w:4.55, h:1.28,
      fill:{color:C.bg}, line:{color:C.border, width:1},
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w:0.07, h:1.28,
      fill:{color:C.red}, line:{color:C.red, width:0},
    });
    s.addText(p.icon, {x:x+0.12, y:y+0.2, w:0.65, h:0.65, fontSize:24, align:"center"});
    s.addText(p.title, {
      x:x+0.85, y:y+0.08, w:3.6, h:0.36,
      fontSize:14, fontFace:"Calibri", bold:true, color:C.red,
    });
    s.addText(p.desc, {
      x:x+0.85, y:y+0.44, w:3.6, h:0.35,
      fontSize:10, fontFace:"Calibri", color:C.muted,
    });
    // Analogie simple
    s.addText(`→ ${p.note}`, {
      x:x+0.85, y:y+0.82, w:3.6, h:0.3,
      fontSize:9, fontFace:"Calibri", color:C.orange, italic:true,
    });
  });

  enclair(s, "La fraude bancaire n'est pas un problème rare — c'est une menace quotidienne et massive. ShieldAI ULTRA est la réponse.");
  footer(s, 2);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 3 — NOTRE SOLUTION (3 colonnes)
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.white};
  header(s, "ShieldAI ULTRA — 3 Couches qui Travaillent Ensemble");

  // Intro phrase
  s.addText("Imaginez 3 experts qui collaborent en temps réel : un analyste, une mémoire et un écran de contrôle.", {
    x:0.3, y:0.78, w:9.4, h:0.28,
    fontSize:11, fontFace:"Calibri", color:C.muted, align:"center", italic:true,
  });

  const cols = [
    {title:"⚙️  Moteur Python", sub:"Le cerveau — il analyse", color:C.blue, bg:"eff6ff",
     items:[
       {t:"7 détecteurs indépendants",  n:"= 7 questions posées pour chaque paiement"},
       {t:"Zéro dépendance externe",    n:"= fonctionne seul, sans logiciel tiers"},
       {t:"Compatible Python 3.14",     n:"= utilise la toute dernière version du langage"},
       {t:"11/11 tests CI validés ✓",   n:"= approuvé à 100% par les tests du jury"},
     ]},
    {title:"🧠  Intelligence",  sub:"La mémoire — il apprend", color:C.green, bg:"f0fdf4",
     items:[
       {t:"Score 0.0 → 1.0",            n:"= 0 = innocent, 1 = fraudeur certain"},
       {t:"Profils clients adaptatifs", n:"= chaque client a son propre profil de dépenses"},
       {t:"Historique antérieur seul",  n:"= compare avec AVANT, pas avec l'avenir"},
       {t:"Calibration IQR + Z-score",  n:"= deux méthodes statistiques pour plus de fiabilité"},
     ]},
    {title:"📊  Dashboard",     sub:"Les yeux — il affiche",  color:C.orange, bg:"fff7ed",
     items:[
       {t:"4 graphiques interactifs",   n:"= vous voyez tout d'un seul coup d'œil"},
       {t:"Actualisation toutes 30 s",  n:"= les données se rafraîchissent seules"},
       {t:"Export CSV en 1 clic",       n:"= téléchargez le rapport pour votre comptable"},
       {t:"Filtres dynamiques",         n:"= affichez uniquement ce qui vous intéresse"},
     ]},
  ];

  cols.forEach((col, i) => {
    const x = 0.3 + i*3.15;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y:1.1, w:3.0, h:4.05,
      fill:{color:col.bg}, line:{color:C.border, width:1},
    });
    // Header
    s.addShape(pres.shapes.RECTANGLE, {
      x, y:1.1, w:3.0, h:0.55,
      fill:{color:col.color}, line:{color:col.color, width:0},
    });
    s.addText(col.title, {
      x:x+0.1, y:1.1, w:2.8, h:0.3,
      fontSize:12, fontFace:"Calibri", bold:true, color:C.white, margin:0,
    });
    s.addText(col.sub, {
      x:x+0.1, y:1.38, w:2.8, h:0.24,
      fontSize:9.5, fontFace:"Calibri", color:"e0f2fe", italic:true, margin:0,
    });

    col.items.forEach((item, j) => {
      const iy = 1.72 + j*0.85;
      s.addShape(pres.shapes.RECTANGLE, {
        x:x+0.1, y:iy, w:2.8, h:0.78,
        fill:{color:C.white}, line:{color:C.border, width:0.5},
      });
      s.addShape(pres.shapes.OVAL, {
        x:x+0.18, y:iy+0.12, w:0.2, h:0.2,
        fill:{color:col.color}, line:{color:col.color, width:0},
      });
      s.addText(item.t, {
        x:x+0.45, y:iy+0.06, w:2.35, h:0.3,
        fontSize:10, fontFace:"Calibri", bold:true, color:C.text,
      });
      s.addText(item.n, {
        x:x+0.45, y:iy+0.38, w:2.35, h:0.32,
        fontSize:9, fontFace:"Calibri", color:col.color, italic:true,
      });
    });
  });

  enclair(s, "Moteur = analyse. Intelligence = apprend du passé. Dashboard = affiche les résultats. Les 3 travaillent ensemble en même temps.");
  footer(s, 3);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 4 — 7 SIGNAUX avec analogies
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.white};
  header(s, "7 Signaux de Détection — Ce Que le Système Surveille");

  s.addText("Chaque paiement reçoit 7 vérifications automatiques. Si l'une sonne l'alarme, le score monte.", {
    x:0.3, y:0.78, w:9.4, h:0.28,
    fontSize:11, fontFace:"Calibri", color:C.muted, align:"center", italic:true,
  });

  const signals = [
    {icon:"🔍", label:"Champs manquants",      color:C.red,
     tech:"transaction_id / user_id / amount absent → Score 1.0",
     analogy:"Comme un chèque sans nom, sans date et sans montant — invalide d'office"},
    {icon:"💰", label:"Montant invalide",       color:C.red,
     tech:"Valeur nulle ou négative → Fraude certaine, blocage immédiat",
     analogy:"Personne ne paye -50€. Si c'est le cas, quelqu'un a trafiqué les données"},
    {icon:"📊", label:"Anomalie statistique IQR", color:C.orange,
     tech:"Dépassement de la borne supérieure IQR (4+ transactions historiques)",
     analogy:"Vous dépensez 50€/jour depuis 1 mois. Soudain 9 800€ → alarme"},
    {icon:"📈", label:"Z-Score anormal",        color:C.orange,
     tech:"Z > 3.5 (+0.35) ou Z > 2.5 avec 3+ transactions dans l'historique",
     analogy:"Calcul statistique : ce montant est-il 'normal' pour CE client précis ?"},
    {icon:"🌍", label:"Géographie impossible",  color:C.blue,
     tech:"Déplacement > 900 km/h entre deux transactions consécutives",
     analogy:"Impossible d'acheter à Paris à 10h01 et à Tokyo à 10h02 — c'est un vol"},
    {icon:"⚡", label:"Fréquence suspecte",     color:C.blue,
     tech:"5+ transactions du même client en moins de 60 secondes",
     analogy:"Un humain normal ne fait pas 6 achats en 1 minute — c'est un robot"},
    {icon:"🔄", label:"Transaction dupliquée",  color:C.green,
     tech:"Même ID ou même signature : user + montant + marchand + horodatage",
     analogy:"Comme être débité deux fois pour le même café — le système le détecte"},
  ];

  signals.forEach((sig, i) => {
    const col = i < 4 ? 0 : 1;
    const row = i < 4 ? i : i - 4;
    const x   = 0.3 + col * 4.85;
    const y   = 1.12 + row * 0.96;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w:4.65, h:0.88,
      fill:{color:C.bg}, line:{color:C.border, width:0.5},
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w:0.06, h:0.88,
      fill:{color:sig.color}, line:{color:sig.color, width:0},
    });
    // Numéro
    s.addShape(pres.shapes.OVAL, {
      x:x+0.12, y:y+0.07, w:0.42, h:0.42,
      fill:{color:sig.color}, line:{color:sig.color, width:0},
    });
    s.addText(String(i+1), {
      x:x+0.12, y:y+0.07, w:0.42, h:0.42,
      fontSize:12, fontFace:"Calibri", bold:true, color:C.white,
      align:"center", valign:"middle", margin:0,
    });
    // Label
    s.addText(`${sig.icon} ${sig.label}`, {
      x:x+0.62, y:y+0.04, w:3.95, h:0.28,
      fontSize:11, fontFace:"Calibri", bold:true, color:C.text,
    });
    // Technique (muted)
    s.addText(sig.tech, {
      x:x+0.62, y:y+0.31, w:3.95, h:0.24,
      fontSize:8.5, fontFace:"Calibri", color:C.muted,
    });
    // Analogie (couleur, italic)
    s.addText(`→ ${sig.analogy}`, {
      x:x+0.62, y:y+0.56, w:3.95, h:0.26,
      fontSize:8.5, fontFace:"Calibri", color:sig.color, italic:true,
    });
  });

  enclair(s, "Chaque vérification correspond à un comportement humain normal. Si quelque chose sort de la normale, le score augmente automatiquement.");
  footer(s, 4);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 5 — L'ALGORITHME DE SCORE : COMMENT ÇA CALCULE
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.white};
  header(s, "L'Algorithme de Score — Comment le Système Décide");

  s.addText("Le score de fraude n'est pas une décision binaire OUI/NON. C'est un calcul progressif : chaque signal ajoute du poids jusqu'à dépasser le seuil d'alerte (0.5).", {
    x:0.3, y:0.78, w:9.4, h:0.3,
    fontSize:11, fontFace:"Calibri", color:C.muted, align:"center", italic:true,
  });

  // ── Exemple concret tx005 (gauche) ─────────────────────────────────────────
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:1.12, w:5.1, h:0.38,
    fill:{color:C.navy}, line:{color:C.navy, width:0},
  });
  s.addText("📋  Exemple réel : transaction tx005 — Score final = 0.75 → FRAUDE", {
    x:0.38, y:1.12, w:5.0, h:0.38,
    fontSize:10, fontFace:"Calibri", bold:true, color:C.white, valign:"middle", margin:0,
  });

  const steps = [
    {sig:"Score de départ",              add:0,    total:0.00, color:C.muted,   bg:C.bg,      bar:0},
    {sig:"Montant 9 800€ > seuil IQR 222€ (×43 le seuil)", add:0.40, total:0.40, color:C.orange, bg:C.orangeL, bar:40},
    {sig:"Paiement sans carte (client toujours en magasin)", add:0.10, total:0.50, color:C.orange, bg:"fff3e0",  bar:50},
    {sig:"Géographie impossible : FR → JP en 2h",           add:0.25, total:0.75, color:C.red,    bg:C.redL,    bar:75},
    {sig:"Résultat final",               add:null, total:0.75, color:C.red,    bg:"fde8e8",   bar:75},
  ];

  steps.forEach((step, i) => {
    const y = 1.58 + i * 0.62;
    s.addShape(pres.shapes.RECTANGLE, {
      x:0.3, y, w:5.1, h:0.54,
      fill:{color:step.bg}, line:{color:C.border, width:0.5},
    });
    // Signal name
    s.addText(step.sig, {
      x:0.38, y:y+0.04, w:3.0, h:0.26,
      fontSize:i===4?11:10, fontFace:"Calibri", bold:i===0||i===4,
      color:step.color,
    });
    // +score badge
    if (step.add !== null && step.add > 0) {
      s.addShape(pres.shapes.RECTANGLE, {
        x:3.42, y:y+0.06, w:0.62, h:0.28,
        fill:{color:step.color}, line:{color:step.color, width:0},
      });
      s.addText(`+${step.add.toFixed(2)}`, {
        x:3.42, y:y+0.06, w:0.62, h:0.28,
        fontSize:10, fontFace:"Calibri", bold:true, color:C.white,
        align:"center", valign:"middle", margin:0,
      });
    }
    // Running total
    s.addText(i===4?"SCORE FINAL :":i===0?"":"→", {
      x:4.1, y:y+0.06, w:0.4, h:0.28,
      fontSize:10, fontFace:"Calibri", color:C.muted, align:"center",
    });
    s.addText(step.total.toFixed(2), {
      x:4.55, y:y+0.04, w:0.75, h:0.32,
      fontSize:i===4?16:12, fontFace:"Calibri", bold:true, color:step.color,
    });
    // Mini progress bar
    if (step.bar > 0) {
      s.addShape(pres.shapes.RECTANGLE, {
        x:0.38, y:y+0.38, w:4.7, h:0.1,
        fill:{color:C.border}, line:{color:C.border, width:0},
      });
      s.addShape(pres.shapes.RECTANGLE, {
        x:0.38, y:y+0.38, w:4.7*step.bar/100, h:0.1,
        fill:{color:step.bar>=50?C.red:C.orange}, line:{color:step.bar>=50?C.red:C.orange, width:0},
      });
    }
  });

  // Seuil badge
  s.addShape(pres.shapes.LINE, {
    x:0.38+4.7*0.5, y:1.58, w:0, h:3.1+0.1,
    line:{color:C.red, width:1.5, dashType:"dash"},
  });
  s.addText("⚠ Seuil 0.50", {
    x:2.67, y:1.52, w:1.3, h:0.28,
    fontSize:9, fontFace:"Calibri", bold:true, color:C.red, align:"center",
  });

  // ── Règles de scoring (droite) ──────────────────────────────────────────────
  s.addShape(pres.shapes.RECTANGLE, {
    x:5.6, y:1.12, w:4.1, h:0.38,
    fill:{color:C.navy}, line:{color:C.navy, width:0},
  });
  s.addText("⚙️  Règles de pondération du moteur", {
    x:5.68, y:1.12, w:3.94, h:0.38,
    fontSize:10, fontFace:"Calibri", bold:true, color:C.white, valign:"middle", margin:0,
  });

  const rules = [
    {rule:"Champs manquants / Montant ≤ 0", w:"1.00", color:C.red,    note:"STOP immédiat"},
    {rule:"Montant dépasse le seuil IQR",   w:"+0.20 à +0.40", color:C.orange, note:"selon l'excès"},
    {rule:"Z-score > 3.5 (fort écart)",     w:"+0.35", color:C.orange, note:"anomalie forte"},
    {rule:"Z-score > 2.5 (écart modéré)",   w:"+0.15", color:C.yellowB,note:"avec 3+ historique"},
    {rule:"Géographie impossible",          w:"+0.25", color:C.blue,  note:"> 900 km/h"},
    {rule:"Déplacement rapide",             w:"+0.15", color:C.blue,  note:"< 2h, > 500 km"},
    {rule:"Fréquence burst (≥ 5 TX/60s)",  w:"+0.55", color:C.red,   note:"attaque robot"},
    {rule:"Transaction dupliquée",          w:"+0.40", color:C.orange, note:"même ID ou signature"},
    {rule:"Paiement sans carte (profil)",   w:"+0.10", color:C.muted, note:"signal faible"},
  ];

  rules.forEach((r, i) => {
    const y = 1.58 + i * 0.36;
    s.addShape(pres.shapes.RECTANGLE, {
      x:5.6, y, w:4.1, h:0.32,
      fill:{color:i%2===0?C.bg:C.white}, line:{color:C.border, width:0.4},
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x:5.6, y, w:0.05, h:0.32,
      fill:{color:r.color}, line:{color:r.color, width:0},
    });
    s.addText(r.rule, {
      x:5.68, y:y+0.04, w:2.45, h:0.24,
      fontSize:8.5, fontFace:"Calibri", color:C.text,
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x:8.15, y:y+0.03, w:0.85, h:0.26,
      fill:{color:r.color}, line:{color:r.color, width:0},
    });
    s.addText(r.w, {
      x:8.15, y:y+0.03, w:0.85, h:0.26,
      fontSize:8, fontFace:"Calibri", bold:true, color:C.white,
      align:"center", valign:"middle", margin:0,
    });
    s.addText(r.note, {
      x:9.02, y:y+0.04, w:0.62, h:0.24,
      fontSize:7.5, fontFace:"Calibri", color:C.muted, italic:true,
    });
  });

  // Formula box
  s.addShape(pres.shapes.RECTANGLE, {
    x:5.6, y:4.82, w:4.1, h:0.4,
    fill:{color:C.navy}, line:{color:C.navy, width:0},
  });
  s.addText("score = min(1.0,  Σ signaux)  —  is_suspicious = score ≥ 0.5", {
    x:5.65, y:4.83, w:4.0, h:0.38,
    fontSize:9.5, fontFace:"Calibri", bold:true, color:C.white,
    align:"center", valign:"middle", margin:0,
  });

  enclair(s, "Aucune règle magique — juste des mathématiques : chaque signal ajoute du poids. Si le total dépasse 0.5, la transaction est suspecte. Simple et transparent.");
  footer(s, 5);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 6 — LES 3 CERVEAUX STATISTIQUES (IQR, Z-SCORE, RATIO)
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.white};
  header(s, "Les 3 Méthodes Statistiques — La Science Derrière le Score");

  s.addText("ShieldAI ULTRA n'invente pas les règles — il applique des méthodes mathématiques éprouvées pour rendre la détection objective et calibrée.", {
    x:0.3, y:0.78, w:9.4, h:0.28,
    fontSize:11, fontFace:"Calibri", color:C.muted, align:"center", italic:true,
  });

  // ── MÉTHODE 1 : IQR ────────────────────────────────────────────────────────
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:1.1, w:2.95, h:3.68,
    fill:{color:C.orangeL}, line:{color:C.orange, width:1.5},
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:1.1, w:2.95, h:0.48,
    fill:{color:C.orange}, line:{color:C.orange, width:0},
  });
  s.addText("📊  Méthode 1 : IQR", {
    x:0.38, y:1.1, w:2.79, h:0.48,
    fontSize:12, fontFace:"Calibri", bold:true, color:C.white, valign:"middle", margin:0,
  });
  s.addText("Interquartile Range — Borne supérieure robuste", {
    x:0.38, y:1.62, w:2.79, h:0.3,
    fontSize:9, fontFace:"Calibri", color:C.orange, italic:true,
  });

  // Box plot visuel simplifié
  const bpY = 2.0;
  // Line
  s.addShape(pres.shapes.LINE, {x:0.5, y:bpY+0.3, w:2.55, h:0, line:{color:C.muted, width:1}});
  // Box Q1-Q3
  s.addShape(pres.shapes.RECTANGLE, {
    x:1.0, y:bpY+0.1, w:1.1, h:0.4,
    fill:{color:C.orange, transparency:60}, line:{color:C.orange, width:1.5},
  });
  // Median
  s.addShape(pres.shapes.LINE, {x:1.4, y:bpY+0.1, w:0, h:0.4, line:{color:C.orange, width:2}});
  // Outlier
  s.addShape(pres.shapes.OVAL, {x:2.8, y:bpY+0.18, w:0.18, h:0.18, fill:{color:C.red}, line:{color:C.red, width:0}});
  // Labels
  s.addText("Q1", {x:0.9, y:bpY+0.52, w:0.3, h:0.22, fontSize:8, fontFace:"Calibri", color:C.orange, align:"center"});
  s.addText("Q3", {x:2.05, y:bpY+0.52, w:0.3, h:0.22, fontSize:8, fontFace:"Calibri", color:C.orange, align:"center"});
  s.addText("Fence", {x:2.5, y:bpY-0.02, w:0.55, h:0.22, fontSize:8, fontFace:"Calibri", color:C.muted, align:"center"});
  // Fence line
  s.addShape(pres.shapes.LINE, {x:2.7, y:bpY, w:0, h:0.6, line:{color:C.red, width:1.5, dashType:"dash"}});
  s.addText("🔴 ALERTE !", {x:2.68, y:bpY+0.12, w:0.7, h:0.2, fontSize:8, fontFace:"Calibri", color:C.red, bold:true});

  s.addText([
    {text:"Formule : ", options:{bold:true, color:C.orange, fontSize:9}},
    {text:"Fence = Q3 + 1.5 × IQR\n", options:{color:C.text, fontSize:9, breakLine:true}},
    {text:"Q1", options:{bold:true, color:C.orange, fontSize:9}},
    {text:" = 25e percentile des montants historiques\n", options:{color:C.text, fontSize:9, breakLine:true}},
    {text:"Q3", options:{bold:true, color:C.orange, fontSize:9}},
    {text:" = 75e percentile — IQR = Q3 − Q1\n\n", options:{color:C.text, fontSize:9, breakLine:true}},
    {text:"Exemple : ", options:{bold:true, color:C.orange, fontSize:9}},
    {text:"historique 20€→100€\nQ1=45, Q3=85, IQR=40\nFence = 85 + 60 = 145€\nMontant 9800€ → ALERTE !", options:{color:C.text, fontSize:9}},
  ], {
    x:0.38, y:bpY+0.82, w:2.75, h:1.95,
    fontFace:"Calibri", valign:"top",
  });

  // ── MÉTHODE 2 : Z-SCORE ────────────────────────────────────────────────────
  s.addShape(pres.shapes.RECTANGLE, {
    x:3.53, y:1.1, w:2.95, h:3.68,
    fill:{color:"f8faff"}, line:{color:C.blue, width:1.5},
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x:3.53, y:1.1, w:2.95, h:0.48,
    fill:{color:C.blue}, line:{color:C.blue, width:0},
  });
  s.addText("📈  Méthode 2 : Z-Score", {
    x:3.61, y:1.1, w:2.79, h:0.48,
    fontSize:12, fontFace:"Calibri", bold:true, color:C.white, valign:"middle", margin:0,
  });
  s.addText("Écart normalisé par rapport à la moyenne client", {
    x:3.61, y:1.62, w:2.79, h:0.3,
    fontSize:9, fontFace:"Calibri", color:C.blue, italic:true,
  });

  // Bell curve simplifié avec rectangles de hauteur croissante
  const bellX = 3.65, bellY = 2.08, bellW = 0.22;
  const heights = [0.05,0.12,0.25,0.4,0.52,0.6,0.58,0.45,0.28,0.14,0.06];
  const bellColors = ["dc2626","dc2626","d97706","d97706","16a34a","16a34a","16a34a","d97706","d97706","dc2626","dc2626"];
  heights.forEach((h, i) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x:bellX+i*bellW, y:bellY+(0.62-h), w:bellW-0.02, h,
      fill:{color:bellColors[i], transparency:40}, line:{color:bellColors[i], width:0},
    });
  });
  // Labels on bell
  s.addText("Zone normale", {x:3.9, y:2.72, w:1.35, h:0.2, fontSize:8, fontFace:"Calibri", color:C.green, align:"center"});
  s.addText("Z>2.5", {x:3.62, y:2.75, w:0.45, h:0.18, fontSize:8, fontFace:"Calibri", color:C.orange, bold:true});
  s.addText("Z>2.5", {x:5.45, y:2.75, w:0.45, h:0.18, fontSize:8, fontFace:"Calibri", color:C.orange, bold:true});
  s.addText("Z>3.5", {x:3.62, y:2.95, w:0.45, h:0.18, fontSize:8, fontFace:"Calibri", color:C.red, bold:true});

  s.addText([
    {text:"Formule : ", options:{bold:true, color:C.blue, fontSize:9}},
    {text:"Z = (montant − moyenne) / écart-type\n\n", options:{color:C.text, fontSize:9, breakLine:true}},
    {text:"Z < 2.5", options:{bold:true, color:C.green, fontSize:9}},
    {text:" → Normal, pas d'alarme\n", options:{color:C.text, fontSize:9, breakLine:true}},
    {text:"Z > 2.5", options:{bold:true, color:C.orange, fontSize:9}},
    {text:" → Signal modéré (+0.15)\n", options:{color:C.text, fontSize:9, breakLine:true}},
    {text:"Z > 3.5", options:{bold:true, color:C.red, fontSize:9}},
    {text:" → Signal fort (+0.35)\n\n", options:{color:C.text, fontSize:9, breakLine:true}},
    {text:"Exemple : ", options:{bold:true, color:C.blue, fontSize:9}},
    {text:"moy=86€, std=21€\nMontant 500€\nZ=(500-86)/21 = 19.7\n→ Très anormal → ALERTE !", options:{color:C.text, fontSize:9}},
  ], {
    x:3.61, y:3.1, w:2.79, h:1.65,
    fontFace:"Calibri", valign:"top",
  });

  // ── MÉTHODE 3 : RATIO ──────────────────────────────────────────────────────
  s.addShape(pres.shapes.RECTANGLE, {
    x:6.75, y:1.1, w:2.95, h:3.68,
    fill:{color:C.greenBg}, line:{color:C.green, width:1.5},
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x:6.75, y:1.1, w:2.95, h:0.48,
    fill:{color:C.green}, line:{color:C.green, width:0},
  });
  s.addText("🔢  Méthode 3 : Ratio", {
    x:6.83, y:1.1, w:2.79, h:0.48,
    fontSize:12, fontFace:"Calibri", bold:true, color:C.white, valign:"middle", margin:0,
  });
  s.addText("Filet de sécurité quand std = 0 (historique uniforme)", {
    x:6.83, y:1.62, w:2.79, h:0.3,
    fontSize:9, fontFace:"Calibri", color:C.green, italic:true,
  });

  // Ratio visual (3 bars comparing)
  const bars = [{v:50,lbl:"Historique\nmoyen 50€"},{v:150,lbl:"3× max\n= 150€"},{v:500,lbl:"Montant\nactuel 500€"}];
  bars.forEach((b, i) => {
    const bx = 6.88+i*0.88;
    const fullH = 1.2;
    const h = (b.v/500)*fullH;
    const colr = i===2?C.red:(i===1?C.orange:C.green);
    s.addShape(pres.shapes.RECTANGLE, {
      x:bx, y:2.78-h+fullH-fullH, w:0.7, h,
      fill:{color:colr, transparency:30}, line:{color:colr, width:1},
    });
    // stack from bottom
    s.addShape(pres.shapes.RECTANGLE, {
      x:bx, y:3.38-h, w:0.7, h,
      fill:{color:colr, transparency:20}, line:{color:colr, width:1},
    });
    s.addText(`${b.v}€`, {
      x:bx, y:3.38-h-0.24, w:0.7, h:0.22,
      fontSize:10, fontFace:"Calibri", bold:true, color:colr, align:"center",
    });
    s.addText(b.lbl, {
      x:bx, y:3.42, w:0.7, h:0.4,
      fontSize:8, fontFace:"Calibri", color:C.muted, align:"center",
    });
  });
  // Arrow 3x
  s.addText("×3", {x:7.82, y:2.9, w:0.5, h:0.35, fontSize:16, fontFace:"Calibri", bold:true, color:C.orange, align:"center"});
  s.addText("×10", {x:8.62, y:2.55, w:0.5, h:0.35, fontSize:14, fontFace:"Calibri", bold:true, color:C.red, align:"center"});

  s.addText([
    {text:"Quand std = 0 : ", options:{bold:true, color:C.green, fontSize:9}},
    {text:"tous les montants historiques sont identiques — IQR et Z-score ne fonctionnent pas.\n\n", options:{color:C.text, fontSize:9, breakLine:true}},
    {text:"Le ratio prend le relais :\n", options:{color:C.text, fontSize:9, breakLine:true}},
    {text:"montant > max × 3", options:{bold:true, color:C.orange, fontSize:9}},
    {text:" → +0.15\n", options:{color:C.text, fontSize:9, breakLine:true}},
    {text:"montant > max × 10", options:{bold:true, color:C.red, fontSize:9}},
    {text:" → +0.55\n\n", options:{color:C.text, fontSize:9, breakLine:true}},
    {text:"Exemple : ", options:{bold:true, color:C.green, fontSize:9}},
    {text:"5 achats de 50€ exactement puis 5000€\nRatio = 100× → +0.55 → ALERTE !", options:{color:C.text, fontSize:9}},
  ], {
    x:6.83, y:3.87, w:2.79, h:0.88,
    fontFace:"Calibri", valign:"top",
  });

  enclair(s, "IQR détecte les extrêmes absolus. Z-Score détecte les écarts relatifs à la moyenne. Ratio prend le relais quand les deux premiers ne peuvent pas calculer. Triple filet de sécurité.");
  footer(s, 6);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 7 — LA CRÉATIVITÉ DERRIÈRE SHIELDAI ULTRA
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.white};
  header(s, "La Créativité — 5 Innovations qui Rendent ShieldAI ULTRA Unique");

  s.addText("Au-delà des algorithmes classiques, ShieldAI ULTRA a été pensé avec 5 choix créatifs qui le distinguent de tout ce qui existe.", {
    x:0.3, y:0.78, w:9.4, h:0.28,
    fontSize:11, fontFace:"Calibri", color:C.muted, align:"center", italic:true,
  });

  const innovations = [
    {
      num:"01", icon:"🧬", title:"Profil ADN par Client",
      color:C.blue, bg:C.blueL,
      problem:"Un système classique applique la même règle à tout le monde. Si le seuil est 500€, Bill Gates ET vous déclenchez la même alarme.",
      solution:"ShieldAI ULTRA construit un profil unique pour chaque client. Votre seuil d'alerte est calculé sur VOS transactions passées — pas sur celles des autres.",
      wow:"→ Si vous dépensez toujours 50€ et payez 5000€, l'alarme sonne. Si vous êtes habitué à 5000€, elle ne sonne pas.",
    },
    {
      num:"02", icon:"🔗", title:"Défense en Profondeur — 7 Verrous Indépendants",
      color:C.orange, bg:C.orangeL,
      problem:"Un seul détecteur peut être contourné. Un fraudeur qui connaît la règle peut l'éviter.",
      solution:"7 signaux totalement indépendants analysent chaque transaction en parallèle. Même si le fraudeur évite 6 signaux, le 7e suffit à déclencher l'alerte.",
      wow:"→ Comme une porte avec 7 serrures différentes. Il suffit qu'une résiste.",
    },
    {
      num:"03", icon:"🐍", title:"Pure Python — La Contrainte Devient une Force",
      color:C.green, bg:C.greenBg,
      problem:"Python 3.14 est incompatible avec numpy et pandas (les bibliothèques standards de data science). Tout le monde a abandonné ces outils.",
      solution:"Nous avons tout réécrit en Python pur : calcul IQR, Z-score, distances géographiques — sans UNE SEULE bibliothèque externe. Code 100% portable.",
      wow:"→ Notre code fonctionne sur n'importe quelle machine avec Python 3.14. Aucune installation requise.",
    },
    {
      num:"04", icon:"💬", title:"L'IA qui Parle — Alertes Auto-Explicatives",
      color:C.navy, bg:"e2e8f0",
      problem:"La plupart des systèmes disent simplement 'FRAUDE'. L'analyste doit alors chercher POURQUOI — ce qui prend du temps et coûte de l'argent.",
      solution:"Chaque alerte inclut automatiquement la raison précise en français : 'Montant 7× la moyenne + déplacement impossible FR→JP en 1h'. L'analyste sait tout d'un coup d'œil.",
      wow:"→ Le système se justifie lui-même. Décision prise en 5 secondes, pas en 5 minutes.",
    },
    {
      num:"05", icon:"🎚️", title:"Sensibilité Ajustable en Temps Réel",
      color:C.red, bg:C.redL,
      problem:"Les systèmes classiques ont un seuil fixe. Pendant le Black Friday, vous avez 10× plus de transactions — le système explose en fausses alertes.",
      solution:"Le curseur de sensibilité (0 → 1) permet d'ajuster le seuil d'alerte EN DIRECT sans redémarrer le système. L'opérateur adapte la vigilance au contexte.",
      wow:"→ Nuit calme : seuil à 0.3 (strict). Black Friday : seuil à 0.7 (souple). Un seul glissement de curseur.",
    },
  ];

  innovations.forEach((innov, i) => {
    const col = i < 3 ? 0 : 1;
    const row = i < 3 ? i : i - 3;
    const x   = 0.3 + col * 4.85;
    const y   = 1.12 + row * 1.22;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w:4.65, h:1.14,
      fill:{color:innov.bg}, line:{color:innov.color, width:1},
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w:0.07, h:1.14,
      fill:{color:innov.color}, line:{color:innov.color, width:0},
    });

    // Number + icon
    s.addText(`${innov.num}`, {
      x:x+0.14, y:y+0.04, w:0.4, h:0.3,
      fontSize:9, fontFace:"Calibri", bold:true, color:innov.color,
    });
    s.addText(innov.icon, {
      x:x+0.14, y:y+0.3, w:0.4, h:0.35,
      fontSize:18, align:"center",
    });

    // Title
    s.addText(innov.title, {
      x:x+0.62, y:y+0.04, w:3.95, h:0.28,
      fontSize:11.5, fontFace:"Calibri", bold:true, color:innov.color,
    });
    // Problem + Solution condensed
    s.addText(`❌ ${innov.problem}`, {
      x:x+0.62, y:y+0.32, w:3.95, h:0.28,
      fontSize:8, fontFace:"Calibri", color:C.muted,
    });
    s.addText(`✅ ${innov.solution}`, {
      x:x+0.62, y:y+0.6, w:3.95, h:0.28,
      fontSize:8, fontFace:"Calibri", color:C.text,
    });
    s.addText(innov.wow, {
      x:x+0.62, y:y+0.86, w:3.95, h:0.24,
      fontSize:8, fontFace:"Calibri", color:innov.color, italic:true, bold:true,
    });
  });

  enclair(s, "Ces 5 innovations ne sont pas des gadgets — chacune résout un problème réel que les systèmes classiques ne peuvent pas résoudre. C'est ça, la créativité technique.");
  footer(s, 7);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 8 — DASHBOARD (wireframe annoté)
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.bg};
  header(s, "Le Dashboard — L'Écran de Contrôle Tout-en-Un");

  s.addText("Tout ce dont l'analyste a besoin est visible sur UNE SEULE page. Aucune formation requise pour comprendre les résultats.", {
    x:0.3, y:0.78, w:9.4, h:0.28,
    fontSize:11, fontFace:"Calibri", color:C.muted, align:"center", italic:true,
  });

  // Dashboard mock header
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:1.1, w:9.4, h:0.45,
    fill:{color:C.navy}, line:{color:C.navy, width:0},
  });
  s.addText("🛡  ShieldAI ULTRA     SYSTEM STATUS: ACTIVE     12:16:28     THREAT LEVEL: CRITICAL", {
    x:0.4, y:1.1, w:9.2, h:0.45,
    fontSize:8.5, fontFace:"Calibri", color:C.white, valign:"middle",
  });

  // Annotation header
  callout(s, "L'heure se met à jour en direct", 6.0, 0.82, 2.3);
  callout(s, "Niveau de menace global calculé auto", 6.0, 1.57, 3.65, C.red);

  // Left sidebar
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:1.55, w:1.65, h:3.25,
    fill:{color:C.slate}, line:{color:C.slate, width:0},
  });
  s.addText([
    {text:"PANNEAU DE CONTRÔLE\n", options:{fontSize:6.5, color:"94a3b8", bold:true, breakLine:true}},
    {text:"Sensibilité : 0.50\n",   options:{fontSize:8,   color:C.white,  breakLine:true}},
    {text:" \n",                     options:{fontSize:4,   breakLine:true}},
    {text:"Scan Complet\n",          options:{fontSize:8,   color:"94a3b8", breakLine:true}},
    {text:"Alertes seulement\n",     options:{fontSize:8,   color:"94a3b8", breakLine:true}},
    {text:"Exporter CSV\n",          options:{fontSize:8,   color:"94a3b8", breakLine:true}},
    {text:"Rafraîchir\n",            options:{fontSize:8,   color:"94a3b8", breakLine:true}},
    {text:" \n",                     options:{fontSize:4,   breakLine:true}},
    {text:"MÉTRIQUES LIVE\n",        options:{fontSize:6.5, color:"94a3b8", bold:true, breakLine:true}},
    {text:"Total TX    50\n",        options:{fontSize:8,   color:C.white,  breakLine:true}},
    {text:"Alertes     10\n",        options:{fontSize:8,   color:"ef4444", breakLine:true}},
    {text:"Critiques    4\n",        options:{fontSize:8,   color:"f97316", breakLine:true}},
    {text:"Risque moy 0.20",         options:{fontSize:8,   color:C.white}},
  ], {
    x:0.38, y:1.6, w:1.5, h:3.15,
    fontFace:"Calibri", valign:"top",
  });

  // Annotation sidebar
  callout(s, "Les boutons de commande — voir slide 7 pour le détail", 0.28, 4.82, 3.7);

  // 4 KPI cards
  const kpis = [
    {label:"TRANSACTIONS", value:"50",    sub:"Analyzed",    color:C.blue,  note:"Nombre total de\npaiements analysés"},
    {label:"FRAUDES",      value:"10",    sub:"20% détectés", color:C.red,   note:"Alertes levées\npar le système"},
    {label:"CRITIQUES",    value:"4",     sub:"Prioritaires", color:C.orange,note:"À traiter\nen urgence"},
    {label:"RISQUE MOY",   value:"0.199", sub:"Score global", color:C.green, note:"Score faible =\nportefeuille sain"},
  ];
  kpis.forEach((k, i) => {
    const x = 2.1 + i*1.73;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y:1.55, w:1.6, h:1.0,
      fill:{color:C.white}, line:{color:C.border, width:1},
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y:1.55, w:1.6, h:0.06,
      fill:{color:k.color}, line:{color:k.color, width:0},
    });
    s.addText(k.label, {
      x:x+0.06, y:1.61, w:1.48, h:0.22,
      fontSize:6.5, fontFace:"Calibri", color:C.muted, bold:true,
    });
    s.addText(k.value, {
      x:x+0.06, y:1.8, w:1.48, h:0.42,
      fontSize:22, fontFace:"Calibri", bold:true, color:k.color,
    });
    s.addText(k.sub, {
      x:x+0.06, y:2.22, w:1.48, h:0.22,
      fontSize:7.5, fontFace:"Calibri", color:C.muted,
    });
    // Annotation flottante sur chaque KPI
    s.addShape(pres.shapes.RECTANGLE, {
      x:x+0.05, y:2.58, w:1.5, h:0.45,
      fill:{color:"fefce8"}, line:{color:C.yellowB, width:0.5},
    });
    s.addText(k.note, {
      x:x+0.08, y:2.59, w:1.44, h:0.43,
      fontSize:7.5, fontFace:"Calibri", color:C.yellowB,
      align:"center", valign:"middle", italic:true,
    });
  });

  // 2 chart placeholder boxes
  [
    {title:"Graphique 1 — Distribution des risques", sub:"Montre où se situent les transactions (faible, moyen, élevé risque)", x:2.1},
    {title:"Graphique 2 — Carte des pays à risque",  sub:"Montre quels pays concentrent le plus de fraudes détectées",         x:5.95},
  ].forEach((c) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x:c.x, y:3.1, w:3.65, h:1.65,
      fill:{color:C.white}, line:{color:C.border, width:1},
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x:c.x, y:3.1, w:3.65, h:0.3,
      fill:{color:C.bg}, line:{color:C.border, width:0},
    });
    s.addText(c.title, {
      x:c.x+0.1, y:3.1, w:3.45, h:0.3,
      fontSize:8, fontFace:"Calibri", bold:true, color:C.text, valign:"middle",
    });
    s.addText(c.sub, {
      x:c.x+0.15, y:3.52, w:3.3, h:0.5,
      fontSize:8.5, fontFace:"Calibri", color:C.muted, align:"center", italic:true,
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x:c.x+0.3, y:4.08, w:3.05, h:0.6,
      fill:{color:C.bg}, line:{color:C.border, width:0.5},
    });
    s.addText("[ Graphique interactif Chart.js ]", {
      x:c.x+0.3, y:4.08, w:3.05, h:0.6,
      fontSize:8.5, fontFace:"Calibri", color:C.muted,
      align:"center", valign:"middle", italic:true,
    });
  });

  // Right AI panel
  s.addShape(pres.shapes.RECTANGLE, {
    x:9.25, y:1.55, w:0.75, h:3.2,
    fill:{color:C.white}, line:{color:C.border, width:1},
  });
  s.addText([
    {text:"ANALYSE\nAUTO\n \n",        options:{fontSize:6.5, bold:true, color:C.navy, breakLine:true}},
    {text:"ALERTE\n10 fraudes\n \n",   options:{fontSize:7,   color:C.red,    breakLine:true}},
    {text:"CRITIQUE\n4 menaces\n \n",  options:{fontSize:7,   color:C.orange, breakLine:true}},
    {text:"BON\nRisque faible",        options:{fontSize:7,   color:C.green}},
  ], {
    x:9.27, y:1.6, w:0.71, h:3.1,
    fontFace:"Calibri", valign:"top", align:"center",
  });
  callout(s, "Le système rédige lui-même ses conclusions en texte clair", 6.0, 4.78, 3.9);

  footer(s, 8);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 6 — LES 4 GRAPHIQUES expliqués
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.white};
  header(s, "Les 4 Graphiques — Comment les Lire en 10 Secondes");

  // Chart 1 — Line
  s.addChart(pres.charts.LINE, [{
    name:"Nb transactions",
    labels:["0-0.2","0.2-0.4","0.4-0.6","0.6-0.8","0.8-1.0"],
    values:[31, 5, 5, 4, 3],
  }], {
    x:0.3, y:0.82, w:4.55, h:2.1,
    showTitle:true, title:"Courbe de Distribution des Risques",
    titleFontSize:10, titleFontBold:true,
    chartColors:["2563eb"],
    chartArea:{fill:{color:"f8faff"}, roundedCorners:true},
    catAxisLabelColor:C.muted, valAxisLabelColor:C.muted,
    valGridLine:{color:"e2e8f0", size:0.5}, catGridLine:{style:"none"},
    lineSize:2.5, lineSmooth:true, showLegend:false,
  });
  // Explanation box under chart 1
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:3.0, w:4.55, h:0.75,
    fill:{color:C.blueL}, line:{color:C.blue, width:1},
  });
  s.addText([
    {text:"📖 Comment lire : ", options:{bold:true, color:C.blue, fontSize:9}},
    {text:"L'axe horizontal = niveau de risque (0 = sûr, 1 = fraude). L'axe vertical = nombre de transactions. ", options:{color:C.text, fontSize:9}},
    {text:"La grande bosse à gauche (31 TX) = la majorité sont normales. Les 3 TX à droite = fraudes critiques.", options:{color:C.red, fontSize:9, bold:true}},
  ], {
    x:0.38, y:3.01, w:4.39, h:0.73,
    fontFace:"Calibri", valign:"top",
  });

  // Chart 2 — Radar
  s.addChart(pres.charts.RADAR, [{
    name:"Risque %",
    labels:["CN","JP","US","BR","AE","TG","ES","FR"],
    values:[100, 65, 30, 45, 55, 75, 20, 15],
  }], {
    x:5.1, y:0.82, w:4.55, h:2.1,
    showTitle:true, title:"Carte Radar — Risque par Pays",
    titleFontSize:10, titleFontBold:true,
    chartColors:["dc2626"],
    chartArea:{fill:{color:"fff8f8"}, roundedCorners:true},
    showLegend:false,
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x:5.1, y:3.0, w:4.55, h:0.75,
    fill:{color:"fef2f2"}, line:{color:C.red, width:1},
  });
  s.addText([
    {text:"📖 Comment lire : ", options:{bold:true, color:C.red, fontSize:9}},
    {text:"Chaque pointe = un pays. ", options:{color:C.text, fontSize:9}},
    {text:"Plus la pointe est longue vers un pays, plus ce pays concentre des fraudes. ", options:{color:C.text, fontSize:9}},
    {text:"CN (Chine) à 100% = toutes les TX de Chine sont suspectes dans nos données.", options:{color:C.red, fontSize:9, bold:true}},
  ], {
    x:5.18, y:3.01, w:4.39, h:0.73,
    fontFace:"Calibri", valign:"top",
  });

  // Chart 3 — Bar
  s.addChart(pres.charts.BAR, [{
    name:"TX count",
    labels:["0-0.2","0.2-0.4","0.4-0.6","0.6-0.8","0.8-1.0"],
    values:[31, 5, 5, 4, 3],
  }], {
    x:0.3, y:3.85, w:4.55, h:1.8,
    showTitle:true, title:"Histogramme des Scores de Fraude",
    titleFontSize:10, titleFontBold:true,
    barDir:"col",
    chartColors:["16a34a","d97706","d97706","dc2626","dc2626"],
    chartArea:{fill:{color:"f8fff8"}, roundedCorners:true},
    catAxisLabelColor:C.muted, valAxisLabelColor:C.muted,
    valGridLine:{color:"e2e8f0", size:0.5}, catGridLine:{style:"none"},
    showValue:true, dataLabelColor:C.text, showLegend:false,
  });
  // Mini legend for bar chart
  [[C.green,"Vert = normal"],[C.orange,"Orange = surveiller"],[C.red,"Rouge = urgent"]].forEach(([col, lbl], i) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x:0.35+i*1.48, y:5.68, w:0.15, h:0.15,
      fill:{color:col}, line:{color:col, width:0},
    });
    s.addText(lbl, {
      x:0.54+i*1.48, y:5.65, w:1.3, h:0.2,
      fontSize:8, fontFace:"Calibri", color:C.muted,
    });
  });

  // Chart 4 — Doughnut
  s.addChart(pres.charts.DOUGHNUT, [{
    name:"Repartition",
    labels:["Sûres","A surveiller","Critiques"],
    values:[40, 6, 4],
  }], {
    x:5.1, y:3.85, w:4.55, h:1.8,
    showTitle:true, title:"Répartition Sûr / Alerte / Critique",
    titleFontSize:10, titleFontBold:true,
    chartColors:["16a34a","d97706","dc2626"],
    chartArea:{fill:{color:"fafafa"}, roundedCorners:true},
    showLegend:true, legendPos:"r", showPercent:true,
  });

  enclair(s, "Ces 4 graphiques se lisent comme un tableau de bord de voiture : vert = tout va bien, orange = attention, rouge = problème urgent.");
  footer(s, 9);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 7 — BOUTONS ET CONTRÔLES annotés
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.white};
  header(s, "Les Boutons — Un Cockpit Simple et Efficace");

  // Intro analogie
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:0.78, w:9.4, h:0.35,
    fill:{color:C.blueL}, line:{color:C.blue, width:0},
  });
  s.addText("✈️  Imaginez le tableau de bord d'un avion de ligne : chaque bouton a une fonction précise. Voici à quoi sert chaque contrôle de ShieldAI ULTRA.", {
    x:0.38, y:0.8, w:9.24, h:0.31,
    fontSize:10, fontFace:"Calibri", color:C.blue, italic:true, valign:"middle", margin:0,
  });

  // Table columns
  const cX = [0.3, 2.55, 5.4, 8.15];
  const cW = [2.18, 2.78, 2.68, 1.55];

  // Column headers
  ["Bouton / Contrôle","Ce qu'il fait exactement","Quand l'utiliser","Qui l'utilise"].forEach((h, i) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x:cX[i], y:1.2, w:cW[i], h:0.45,
      fill:{color:C.navy}, line:{color:C.white, width:1},
    });
    s.addText(h, {
      x:cX[i]+0.06, y:1.2, w:cW[i]-0.12, h:0.45,
      fontSize:10, fontFace:"Calibri", bold:true,
      color:C.white, valign:"middle", margin:0,
    });
  });

  const rows = [
    ["🎚️ Sensitivity\n(curseur 0→1)",
     "Règle la sensibilité du détecteur. Vers 1 = très strict. Vers 0 = plus souple.",
     "Quand on veut être plus ou moins exigeant selon le contexte de risque",
     "Responsable risque"],
    ["🔍 Full Scan",
     "Lance l'analyse complète sur les 50 transactions avec les réglages actuels.",
     "Pour voir la photo complète du portefeuille à un instant T",
     "Analyste fraude"],
    ["🔔 Alerts Only",
     "Cache les transactions normales. N'affiche que les suspectes.",
     "Quand on veut aller droit au problème sans regarder le reste",
     "Enquêteur"],
    ["📥 Export CSV",
     "Télécharge un fichier Excel avec tous les résultats et les raisons.",
     "Pour envoyer le rapport au service juridique ou à la compliance",
     "Manager / Juriste"],
    ["🔄 Refresh",
     "Recharge les données. Simule l'arrivée de nouvelles transactions.",
     "Pour garder les données à jour en temps réel (production)",
     "Opérateur"],
    ["All/Alerts/Critical/Safe",
     "Trie la liste des transactions par niveau de danger.",
     "Pour naviguer rapidement entre les différents niveaux d'alerte",
     "Tout le monde"],
  ];

  const palette = [
    {bg:C.blueL,   ac:C.blue},
    {bg:"f0fdf4",  ac:C.green},
    {bg:C.orangeL, ac:C.orange},
    {bg:C.redL,    ac:C.red},
    {bg:C.bg,      ac:C.slate},
    {bg:"f0fdf4",  ac:C.green},
  ];

  rows.forEach((row, r) => {
    const y = 1.7 + r * 0.54;
    const p = palette[r];
    row.forEach((cell, c) => {
      s.addShape(pres.shapes.RECTANGLE, {
        x:cX[c], y, w:cW[c], h:0.5,
        fill:{color: c===0 ? p.bg : (r%2===0 ? C.white : C.bg)},
        line:{color:C.border, width:0.5},
      });
      if (c===0) {
        s.addShape(pres.shapes.RECTANGLE, {
          x:cX[c], y, w:0.06, h:0.5,
          fill:{color:p.ac}, line:{color:p.ac, width:0},
        });
      }
      s.addText(cell, {
        x:cX[c]+(c===0?0.12:0.08), y:y+0.06,
        w:cW[c]-(c===0?0.18:0.12), h:0.38,
        fontSize:c===0?9.5:9, fontFace:"Calibri",
        bold:c===0, color:c===0?C.text:(c===3?p.ac:C.muted),
        valign:"middle",
      });
    });
  });

  enclair(s, "Ces boutons ne nécessitent aucune compétence technique. Un clic suffit pour filtrer, analyser ou exporter — tout est pensé pour être intuitif.");
  footer(s, 10);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 8 — THREAT ANALYSIS CENTER annoté
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.white};
  header(s, "Centre d'Analyse des Menaces — Lire une Alerte");

  // "Comment lire" intro
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:0.78, w:9.4, h:0.4,
    fill:{color:C.redL}, line:{color:C.red, width:1},
  });
  s.addText([
    {text:"📌 Comment lire : ", options:{bold:true, color:C.red, fontSize:10}},
    {text:"Chaque ligne = une transaction suspecte. Le ", options:{color:C.text, fontSize:10}},
    {text:"% = probabilité de fraude. ", options:{bold:true, color:C.red, fontSize:10}},
    {text:"Les transactions sont triées du plus dangereux (haut) au moins dangereux (bas). La raison exacte est toujours affichée.", options:{color:C.text, fontSize:10}},
  ], {
    x:0.38, y:0.79, w:9.24, h:0.38,
    fontFace:"Calibri", valign:"middle", margin:0,
  });

  const threats = [
    {rank:"#1", id:"tx014", pct:"100%", color:C.red,    bg:"fef2f2", bc:C.red,
     reason:"Montant invalide (nul ou négatif) — aucun achat légitime ne vaut 0€ ou moins",
     action:"Bloquer immédiatement — contacter le client",
     what:"Un fraudeur a tenté de soumettre un montant négatif pour annuler d'autres transactions"},
    {rank:"#2", id:"tx008", pct:"90%",  color:C.red,    bg:"fff0f0", bc:"ef4444",
     reason:"Montant 7× la moyenne + 6 transactions en 1 minute",
     action:"Enquête urgente — gel temporaire du compte",
     what:"Un robot effectue des achats à toute vitesse avec un montant anormalement élevé"},
    {rank:"#3", id:"tx005", pct:"75%",  color:C.orange, bg:"fff7ed", bc:C.orange,
     reason:"Montant hors IQR + sans carte physique + déplacement géo impossible",
     action:"Vérification identité + blocage en attente",
     what:"3 alarmes simultanées : montant suspect, pas de carte, et géographie incohérente"},
    {rank:"#4", id:"tx010", pct:"70%",  color:C.orange, bg:"fffbeb", bc:"f59e0b",
     reason:"Montant élevé + fréquence excessive + commerçant inconnu",
     action:"Surveillance renforcée + notification client",
     what:"Le compte semble compromis — comportement inhabituel sur plusieurs dimensions"},
  ];

  threats.forEach((t, i) => {
    const y = 1.28 + i * 0.88;

    s.addShape(pres.shapes.RECTANGLE, {
      x:0.3, y, w:9.4, h:0.8,
      fill:{color:t.bg}, line:{color:t.bc, width:1},
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x:0.3, y, w:0.08, h:0.8,
      fill:{color:t.color}, line:{color:t.color, width:0},
    });

    // Score badge
    s.addShape(pres.shapes.RECTANGLE, {
      x:9.0, y:y+0.16, w:0.65, h:0.44,
      fill:{color:t.color}, line:{color:t.color, width:0},
    });
    s.addText(t.pct, {
      x:9.0, y:y+0.16, w:0.65, h:0.44,
      fontSize:15, fontFace:"Calibri", bold:true, color:C.white,
      align:"center", valign:"middle", margin:0,
    });

    s.addText(`${t.rank}  ${t.id}`, {
      x:0.5, y:y+0.04, w:1.5, h:0.3,
      fontSize:13, fontFace:"Calibri", bold:true, color:t.color,
    });
    // Reason (what happened)
    s.addText(`⚠️ ${t.reason}`, {
      x:2.1, y:y+0.04, w:6.8, h:0.28,
      fontSize:9.5, fontFace:"Calibri", color:C.text, bold:true,
    });
    // What it means (plain language)
    s.addText(`💬 ${t.what}`, {
      x:0.5, y:y+0.34, w:5.6, h:0.22,
      fontSize:8.5, fontFace:"Calibri", color:C.muted, italic:true,
    });
    // Action to take
    s.addShape(pres.shapes.RECTANGLE, {
      x:6.2, y:y+0.32, w:2.7, h:0.26,
      fill:{color:t.bg}, line:{color:t.bc, width:0.5},
    });
    s.addText(`→ ${t.action}`, {
      x:6.25, y:y+0.33, w:2.6, h:0.24,
      fontSize:8.5, fontFace:"Calibri", color:t.color, bold:true,
      valign:"middle",
    });
  });

  enclair(s, "L'analyste n'a pas à deviner : le système lui dit QUOI s'est passé, POURQUOI c'est suspect, et QUOI faire. Tout est prêt pour agir.");
  footer(s, 11);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 9 — CI 11/11 expliqué simplement
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.white};
  header(s, "Performance — 11/11 Tests Validés par le Jury");

  // Explain what CI tests are
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:0.78, w:9.4, h:0.42,
    fill:{color:C.greenBg}, line:{color:C.green, width:1},
  });
  s.addText([
    {text:"🤖 Qu'est-ce qu'un test CI ? ", options:{bold:true, color:C.green, fontSize:10}},
    {text:"CI = 'Continuous Integration'. Ce sont des tests automatiques que le jury INTELO2026 fait tourner sur notre code. ", options:{color:C.text, fontSize:10}},
    {text:"Passer 11/11 = notre système répond PARFAITEMENT à TOUTES les exigences du concours.", options:{bold:true, color:C.green, fontSize:10}},
  ], {
    x:0.38, y:0.79, w:9.24, h:0.4,
    fontFace:"Calibri", valign:"middle", margin:0,
  });

  // Big score circle
  s.addShape(pres.shapes.OVAL, {
    x:0.3, y:1.28, w:2.85, h:2.85,
    fill:{color:C.greenBg}, line:{color:C.green, width:3},
  });
  s.addText("11/11", {
    x:0.3, y:1.45, w:2.85, h:1.6,
    fontSize:50, fontFace:"Calibri", bold:true, color:C.green,
    align:"center", valign:"middle",
  });
  s.addText("100% validé", {
    x:0.3, y:3.08, w:2.85, h:0.38,
    fontSize:11, fontFace:"Calibri", bold:true, color:C.green, align:"center",
  });
  s.addText("Score parfait INTELO2026", {
    x:0.3, y:3.42, w:2.85, h:0.28,
    fontSize:9, fontFace:"Calibri", color:C.muted, align:"center",
  });

  // Test list with explanations
  const tests = [
    {code:"test_liste_vide",              expl:"Liste vide → retourne [] — ne plante pas"},
    {code:"test_transaction_normale",     expl:"TX légitime → score < 0.5 — pas de fausse alarme"},
    {code:"test_montant_negatif",         expl:"Montant négatif → score 1.0 — fraude certaine"},
    {code:"test_champ_manquant",          expl:"Champ absent → score 1.0 — données incomplètes"},
    {code:"test_zscore_eleve",            expl:"Montant 7× la moyenne → détecté comme suspect"},
    {code:"test_geographie_impossible",   expl:"Paris→Tokyo en 1h → déplacement impossible détecté"},
    {code:"test_frequence_burst",         expl:"5+ TX en 60s → attaque burst détectée"},
    {code:"test_doublon",                 expl:"Même TX deux fois → doublon signalé"},
    {code:"test_devise_inhabituelle",     expl:"Devise inconnue pour ce client → signal levé"},
    {code:"test_montant_tres_eleve",      expl:"100× le maximum historique → fraude évidente"},
    {code:"test_faux_positif",            expl:"TX un peu élevée mais normale → PAS d'alarme"},
  ];

  tests.forEach((t, i) => {
    const col = i < 6 ? 0 : 1;
    const row = i < 6 ? i : i - 6;
    const x   = 3.35 + col * 3.2;
    const y   = 1.28 + row * 0.53;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w:3.05, h:0.48,
      fill:{color:i===10 ? "f0fdf4" : C.bg}, line:{color:C.border, width:0.5},
    });
    // Check mark
    s.addShape(pres.shapes.OVAL, {
      x:x+0.06, y:y+0.1, w:0.28, h:0.28,
      fill:{color:C.green}, line:{color:C.green, width:0},
    });
    s.addText("✓", {
      x:x+0.06, y:y+0.1, w:0.28, h:0.28,
      fontSize:10, fontFace:"Calibri", bold:true, color:C.white,
      align:"center", valign:"middle", margin:0,
    });
    s.addText(t.code, {
      x:x+0.4, y:y+0.03, w:2.58, h:0.2,
      fontSize:8.5, fontFace:"Calibri", bold:true, color:C.text,
    });
    s.addText(t.expl, {
      x:x+0.4, y:y+0.24, w:2.58, h:0.2,
      fontSize:7.5, fontFace:"Calibri", color:C.muted, italic:true,
    });
  });

  // Bottom strip
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:4.85, w:9.4, h:0.35,
    fill:{color:C.greenBg}, line:{color:C.green, width:1},
  });
  s.addText("Zéro numpy / pandas — Pure Python 3.14 — Fonctionne sans aucune bibliothèque externe installée", {
    x:0.38, y:4.87, w:9.24, h:0.31,
    fontSize:9.5, fontFace:"Calibri", color:C.green,
    bold:true, align:"center", margin:0,
  });

  footer(s, 12);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 10 — ARCHITECTURE (flux annoté)
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.bg};
  header(s, "Architecture — Comment le Système Fonctionne de A à Z");

  s.addText("Imaginez une chaîne de montage : les données brutes entrent, et les résultats clairs sortent. Chaque étape enrichit l'information.", {
    x:0.3, y:0.78, w:9.4, h:0.28,
    fontSize:11, fontFace:"Calibri", color:C.muted, align:"center", italic:true,
  });

  const flow = [
    {label:"1. Données CSV / API",
     sub:"Les transactions bancaires brutes arrivent (fichier CSV ou flux API)",
     plain:"= Comme un relevé de compte bancaire qui arrive au système",
     col:C.blue, bg:C.blueL},
    {label:"2. load_transactions() + _clean_row()",
     sub:"Chaque ligne est lue, nettoyée et validée — dates, montants, devises",
     plain:"= Le système nettoie et vérifie que chaque donnée est au bon format",
     col:C.navy, bg:"e2e8f0"},
    {label:"3. detect_fraud() — Les 7 signaux en action",
     sub:"IQR | Z-score | Ratio | Géographie | Fréquence | Doublon | Champs",
     plain:"= Le cerveau analyse : ce paiement est-il normal pour CE client ?",
     col:C.navy, bg:"e2e8f0"},
    {label:"4. API Flask — /api/data  /api/transactions  /api/export",
     sub:"Les résultats sont envoyés au dashboard via des routes web standardisées",
     plain:"= Le messager qui transporte les résultats vers l'écran d'affichage",
     col:C.blue, bg:C.blueL},
    {label:"5. Dashboard Chart.js — Visualisation temps réel",
     sub:"4 graphiques interactifs, filtres, alertes, export — tout s'affiche instantanément",
     plain:"= L'écran de contrôle lisible par tout le monde, même sans formation",
     col:C.green, bg:C.greenL},
  ];

  flow.forEach((item, i) => {
    const y = 1.12 + i * 0.79;
    s.addShape(pres.shapes.RECTANGLE, {
      x:0.35, y, w:6.5, h:0.68,
      fill:{color:item.bg}, line:{color:item.col, width:1.5},
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x:0.35, y, w:0.07, h:0.68,
      fill:{color:item.col}, line:{color:item.col, width:0},
    });
    s.addText(item.label, {
      x:0.5, y:y+0.04, w:6.25, h:0.27,
      fontSize:11, fontFace:"Calibri", bold:true, color:item.col,
    });
    s.addText(item.sub, {
      x:0.5, y:y+0.3, w:6.25, h:0.2,
      fontSize:8.5, fontFace:"Calibri", color:C.muted,
    });
    // Arrow
    if (i < flow.length-1) {
      s.addShape(pres.shapes.LINE, {
        x:3.5, y:y+0.68, w:0, h:0.11,
        line:{color:C.muted, width:1.5},
      });
    }
    // Plain language annotation on right
    s.addShape(pres.shapes.RECTANGLE, {
      x:7.05, y:y+0.08, w:2.6, h:0.5,
      fill:{color:"fefce8"}, line:{color:C.yellowB, width:0.7},
    });
    s.addText(item.plain, {
      x:7.1, y:y+0.09, w:2.5, h:0.48,
      fontSize:8.5, fontFace:"Calibri", color:C.yellowB,
      italic:true, valign:"middle",
    });
  });

  enclair(s, "En résumé : données brutes → nettoyage → analyse → résultats → affichage. Un pipeline complet, automatique et en temps réel.");
  footer(s, 13);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 11 — COMPARAISON avec explications
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.white};
  header(s, "Pourquoi ShieldAI ULTRA Mérite la 1ère Place");

  // Intro
  s.addText("Là où une solution basique dit OUI ou NON selon des règles fixes, ShieldAI ULTRA adapte son analyse à chaque client individuellement — comme un expert humain.", {
    x:0.3, y:0.78, w:9.4, h:0.32,
    fontSize:11, fontFace:"Calibri", color:C.muted, align:"center", italic:true,
  });

  // Table avec 4 colonnes maintenant : Critère / Basique / ShieldAI / Pourquoi ça compte
  const cX = [0.3, 2.55, 5.05, 7.55];
  const cW = [2.18, 2.43, 2.43, 2.18];

  ["Critère","Solution basique","ShieldAI ULTRA","Pourquoi ça compte"].forEach((h, i) => {
    const hcol = i===2 ? C.blue : (i===0 ? C.navy : C.slate);
    s.addShape(pres.shapes.RECTANGLE, {
      x:cX[i], y:1.17, w:cW[i], h:0.45,
      fill:{color:hcol}, line:{color:C.white, width:1},
    });
    s.addText(h, {
      x:cX[i]+0.06, y:1.17, w:cW[i]-0.12, h:0.45,
      fontSize:10, fontFace:"Calibri", bold:true,
      color:C.white, valign:"middle", margin:0,
    });
  });

  const rows = [
    ["Détection",      "Règles fixes statiques", "7 signaux adaptatifs",       "S'adapte à chaque fraudeur, pas seulement aux connus"],
    ["Score CI",       "Partiel ou inconnu",      "11/11 — 100% ✓",            "Le jury confirme : notre système est complet et correct"],
    ["Profils clients","Non — même règle pour tous","Oui — historique unique",  "Votre profil ≠ profil de quelqu'un d'autre"],
    ["Géographie",     "Non",                     "Oui — temps réel",          "Paris + Tokyo en même temps = impossible = fraude"],
    ["Dashboard",      "Non",                     "Oui — 4 graphiques",        "Visualiser = décider plus vite, sans erreur"],
    ["Export rapport", "Non",                     "Oui — CSV en 1 clic",       "Le rapport est prêt pour le service juridique"],
    ["Python 3.14",    "Crash (numpy/pandas)",    "Compatible — 0 erreur",     "Notre code fonctionne sur la version la plus récente"],
    ["Faux positifs",  "Nombreux",                "Calibrés — IQR + seuils",   "Moins de clients bloqués à tort = meilleure expérience"],
  ];

  rows.forEach((row, r) => {
    const y = 1.67 + r * 0.41;
    const bg = r%2===0 ? C.white : C.bg;
    row.forEach((cell, c) => {
      const isGood = c===2 && !["Non","Partiel ou inconnu","Nombreux","Crash (numpy/pandas)"].includes(cell);
      s.addShape(pres.shapes.RECTANGLE, {
        x:cX[c], y, w:cW[c], h:0.37,
        fill:{color: c===2 ? (r%2===0?C.blueL:C.blueMid) : (c===3?C.greenBg:bg)},
        line:{color:C.border, width:0.5},
      });
      s.addText(cell, {
        x:cX[c]+0.07, y:y+0.05, w:cW[c]-0.14, h:0.27,
        fontSize:9, fontFace:"Calibri",
        bold:c===2 && isGood,
        color:c===2?(isGood?C.green:C.muted):(c===3?C.green:C.text),
        valign:"middle",
      });
    });
  });

  // PR link + score
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.3, y:5.0, w:5.9, h:0.35,
    fill:{color:C.blueL}, line:{color:C.blue, width:1},
  });
  s.addText("Soumission : https://github.com/INTELO2026/fraud-challenge/pull/42", {
    x:0.38, y:5.02, w:5.74, h:0.31,
    fontSize:9, fontFace:"Calibri", color:C.blue, bold:true, margin:0, valign:"middle",
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x:6.35, y:5.0, w:3.35, h:0.35,
    fill:{color:C.greenBg}, line:{color:C.green, width:1},
  });
  s.addText("Score CI : 11/11 — 100% ✓ parfait", {
    x:6.43, y:5.02, w:3.19, h:0.31,
    fontSize:9, fontFace:"Calibri", color:C.green, bold:true, margin:0, valign:"middle", align:"center",
  });

  footer(s, 14);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 12 — CONCLUSION avec récapitulatif simple
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = {color:C.navy};

  s.addShape(pres.shapes.OVAL, {
    x:3.6, y:0.15, w:2.8, h:2.8,
    fill:{color:C.blue, transparency:85}, line:{color:C.blue, width:0},
  });
  s.addText("🛡", {
    x:3.65, y:0.2, w:2.7, h:1.8,
    fontSize:72, align:"center", valign:"middle",
  });

  s.addText("ShieldAI ULTRA", {
    x:0.5, y:2.6, w:9.0, h:0.85,
    fontSize:42, fontFace:"Calibri", bold:true, color:C.white,
    align:"center", charSpacing:4,
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x:3.2, y:3.42, w:3.6, h:0.05,
    fill:{color:C.blue}, line:{color:C.blue, width:0},
  });

  s.addText("Ce que vous venez de voir en résumé :", {
    x:0.5, y:3.52, w:9.0, h:0.3,
    fontSize:13, fontFace:"Calibri", color:"94a3b8", align:"center",
  });

  // 3 piliers avec explication complète
  const pillars = [
    {icon:"🎯", title:"PRÉCISION",   col:C.blue,
     sub:"11/11 tests validés\nAucune fraude manquée",
     plain:"Le jury a testé notre code avec 11 scénarios. Nous avons tout réussi."},
    {icon:"🔧", title:"ROBUSTESSE",  col:C.green,
     sub:"Python 3.14 compatible\nZéro bibliothèque externe",
     plain:"Le système fonctionne seul, sans aucun logiciel supplémentaire."},
    {icon:"📊", title:"LISIBILITÉ",  col:C.orange,
     sub:"Dashboard professionnel\nDécision en 5 secondes",
     plain:"Même quelqu'un sans formation technique comprend l'écran."},
  ];

  pillars.forEach((p, i) => {
    const x = 0.55 + i * 3.0;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y:3.88, w:2.75, h:1.5,
      fill:{color:C.white, transparency:88},
      line:{color:p.col, width:1.5},
    });
    s.addText(p.icon, {
      x:x+0.1, y:3.93, w:0.55, h:0.5, fontSize:24, align:"center",
    });
    s.addText(p.title, {
      x:x+0.05, y:4.4, w:2.65, h:0.3,
      fontSize:11, fontFace:"Calibri", bold:true, color:p.col,
      align:"center", charSpacing:1,
    });
    s.addText(p.sub, {
      x:x+0.05, y:4.68, w:2.65, h:0.38,
      fontSize:8.5, fontFace:"Calibri", color:"94a3b8", align:"center",
    });
    s.addText(p.plain, {
      x:x+0.08, y:5.05, w:2.59, h:0.3,
      fontSize:7.5, fontFace:"Calibri", color:"64748b",
      align:"center", italic:true,
    });
  });

  s.addText("MERCI — Questions ?", {
    x:0.5, y:5.4, w:9.0, h:0.4,
    fontSize:20, fontFace:"Calibri", bold:true, color:C.white, align:"center",
  });
}

// ── Write ────────────────────────────────────────────────────────────────────
pres.writeFile({fileName:"C:\\projets\\HACKATHON IT 2026\\ShieldAI_ULTRA_v3_ALGO.pptx"})
  .then(() => console.log("OK — ShieldAI_ULTRA_Presentation.pptx genere avec succes!"))
  .catch(e => { console.error("ERREUR:", e); process.exit(1); });
