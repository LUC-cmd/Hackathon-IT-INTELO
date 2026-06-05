const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, AlignmentType, BorderStyle, WidthType, ShadingType, HeadingLevel, PageBreak, ExternalHyperlink, LevelFormat } = require('docx');
const fs = require('fs');

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial", color: "1F4E78" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: "2E75B6" },
        paragraph: { spacing: { before: 180, after: 100 }, outlineLevel: 1 } },
    ]
  },
  numbering: {
    config: [
      { reference: "bullets", levels: [
          { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
        ]
      },
      { reference: "numbers", levels: [
          { level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
        ]
      }
    ]
  },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    children: [
      new Paragraph({ spacing: { before: 600 }, alignment: AlignmentType.CENTER, children: [new TextRun({ text: "LOMÉ BUSINESS SCHOOL", bold: true, size: 32, color: "1F4E78" })] }),
      new Paragraph({ spacing: { after: 400 }, alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Hackathon IT 2026 - Version Premium", bold: true, size: 28, color: "C00000" })] }),

      new PageBreak(),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Bienvenue au Défi!")] }),
      new Paragraph({ spacing: { after: 200 }, children: [new TextRun("Ce hackathon te pousse à résoudre un vrai problème : la détection de fraude financière, un défi qui coûte 35+ milliards par an aux institutions.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Format Officiel")] }),
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [3000, 6360],
        rows: [
          new TableRow({ children: [
            new TableCell({ borders, shading: { fill: "D5E8F0", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "Durée", bold: true })] })] }),
            new TableCell({ borders, children: [new Paragraph({ children: [new TextRun("4 heures")] })] }),
          ]}),
          new TableRow({ children: [
            new TableCell({ borders, shading: { fill: "D5E8F0", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "Langage", bold: true })] })] }),
            new TableCell({ borders, children: [new Paragraph({ children: [new TextRun("Python obligatoire")] })] }),
          ]}),
          new TableRow({ children: [
            new TableCell({ borders, shading: { fill: "D5E8F0", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "Tests", bold: true })] })] }),
            new TableCell({ borders, children: [new Paragraph({ children: [new TextRun("11 tests publics + tests cachés")] })] }),
          ]}),
        ]
      }),

      new Paragraph({ spacing: { after: 300 } }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Bonnes Pratiques pour Dominer")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("1. Profil Client Solide")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("Construis un historique par client avec moyennes et écarts-types")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 200 }, children: [new TextRun("Stocke les pays visités et patterns de transaction")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("2. Heuristiques Intelligentes")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("Montant > moyenne + 3 sigma = signal fort de fraude")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("5 transactions en 1 minute = suspect")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 200 }, children: [new TextRun("Deux pays éloignés en temps insuffisant = impossible physiquement")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("3. Justifications Pertinentes")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 300 }, children: [new TextRun("Raison doit être lisible et utile pour un opérateur")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Pièges Mortels")] }),
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [2500, 6860],
        rows: [
          new TableRow({ children: [
            new TableCell({ borders, shading: { fill: "C00000", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "Erreur", bold: true, color: "FFFFFF" })] })] }),
            new TableCell({ borders, shading: { fill: "C00000", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "Conséquence", bold: true, color: "FFFFFF" })] })] }),
          ]}),
          new TableRow({ children: [
            new TableCell({ borders, children: [new Paragraph({ children: [new TextRun("Réponses en dur")] })] }),
            new TableCell({ borders, children: [new Paragraph({ children: [new TextRun("Tests cachés échouent = 0 points")] })] }),
          ]}),
          new TableRow({ children: [
            new TableCell({ borders, children: [new Paragraph({ children: [new TextRun("Code qui plante")] })] }),
            new TableCell({ borders, children: [new Paragraph({ children: [new TextRun("Disqualification")] })] }),
          ]}),
          new TableRow({ children: [
            new TableCell({ borders, children: [new Paragraph({ children: [new TextRun("Ignorer données manquantes")] })] }),
            new TableCell({ borders, children: [new Paragraph({ children: [new TextRun("Erreur sur données réelles")] })] }),
          ]}),
        ]
      }),

      new Paragraph({ spacing: { before: 300, after: 300 } }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Système de Notation")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Niveau 1 - Fondamentaux (Tests 1-4)")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("Format sortie correct")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 200 }, children: [new TextRun("Anomalies évidentes détectées (montants négatifs, champs manquants)")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Niveau 2 - Logique Métier (Tests 5-9)")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("Montants anormaux vs historique client")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("Fréquence transactions suspecte")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 200 }, children: [new TextRun("Incohérences géographiques")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Niveau 3 - Finesse (Tests 10-11)")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("Éviter faux positifs excessifs")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 200 }, children: [new TextRun("Gérer cas limites intelligemment")] }),

      new Paragraph({ spacing: { before: 200, after: 200 }, border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: "FFCC00" } }, children: [new TextRun({ text: "Tests cachés existent - ne hardcode pas!", bold: true, color: "C00000" })] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Bonus : Interface Streamlit")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("Facultatif mais très utile en cas d'égalité")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("Upload CSV et visualisations")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 300 }, children: [new TextRun("Tableau filtrable avec explications")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Critères Tiebreaker")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("1. Lisibilité du code")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("2. Pertinence justifications")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 300 }, children: [new TextRun("3. Qualité interface bonus")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Checklist Avant Submission")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("Tests locaux passent ✓")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("Format sortie valide ✓")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("Code robuste aux données manquantes ✓")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("Justifications claires ✓")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("Pas de hardcoding ✓")] }),

      new Paragraph({ spacing: { before: 400 }, alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Bonne chance! 🚀🍀", bold: true, size: 28, color: "C00000" })] }),
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("HACKATHON_IT_2026_PREMIUM.docx", buffer);
  console.log("✅ Document créé avec succès!");
});
