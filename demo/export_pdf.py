"""Générateur de rapport PDF premium — design professionnel MemBridge."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )

    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


def generate_pdf_report(report: dict, output_path: Path | None = None) -> bytes | None:
    """Génère un rapport PDF premium à partir du report JSON."""
    if not HAS_REPORTLAB:
        return None

    if output_path is None:
        output_path = Path("/tmp/membridge-report.pdf")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Document setup
    doc = SimpleDocTemplate(
        str(output_path), pagesize=A4, topMargin=0.5 * inch, bottomMargin=0.5 * inch
    )
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=28,
        textColor=colors.HexColor("#C44F28"),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
    )

    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=colors.HexColor("#2F5242"),
        spaceAfter=12,
        spaceBefore=12,
        fontName="Helvetica-Bold",
    )

    # Header
    story.append(Paragraph("MemBridge", title_style))
    story.append(Paragraph("Rapport de Benchmark — Mémoire Partagée IA", styles["Normal"]))
    story.append(
        Paragraph(f"<i>{datetime.now().strftime('%d %B %Y à %H:%M')}</i>", styles["Normal"])
    )
    story.append(Spacer(1, 0.3 * inch))

    # Executive summary
    savings_pct = report.get("savings_pct", 0)
    quality_score = report.get("quality", {}).get("score_pct", 0)
    is_winner = savings_pct >= 70 and quality_score >= 80

    summary_color = colors.HexColor("#10b981") if is_winner else colors.HexColor("#f59e0b")
    story.append(Paragraph("Verdict", heading_style))

    verdict_text = (
        "✓ HACKATHON GAGNANT — Critères victoire atteints"
        if is_winner
        else "⚠️  Objectif non atteint"
    )
    story.append(
        Paragraph(f"<b style='color:{summary_color.hexval()}'>{verdict_text}</b>", styles["Normal"])
    )
    story.append(Spacer(1, 0.2 * inch))

    # Metrics table
    story.append(Paragraph("Métriques Clés", heading_style))
    naive_tokens = report.get("naive", {}).get("total_tokens", 0)
    memory_tokens = report.get("memory", {}).get("total_tokens", 0)
    tokens_saved = report.get("tokens_saved", 0)
    euros_saved = report.get("euros_saved", 0)

    metrics_data = [
        ["Métrique", "Naïf", "MemBridge", "Écart"],
        ["Tokens totaux", f"{naive_tokens:,}", f"{memory_tokens:,}", f"-{tokens_saved:,}"],
        [
            "Coût estimé (€)",
            f"{naive_tokens * 0.15 / 1_000_000:.4f}",
            f"{memory_tokens * 0.15 / 1_000_000:.4f}",
            f"-{euros_saved:.4f}",
        ],
        ["Qualité (pièges)", f"{report.get('quality', {}).get('passed', 0)}/10", "N/A", "N/A"],
        ["Économie", "—", "—", f"-{savings_pct}%"],
    ]

    metrics_table = Table(metrics_data, colWidths=[2 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch])
    metrics_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#C44F28")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]
        )
    )
    story.append(metrics_table)
    story.append(Spacer(1, 0.3 * inch))

    # Questions pièges
    story.append(Paragraph("Questions Pièges — Résultats Détaillés", heading_style))
    trap_details = report.get("quality", {}).get("details", [])
    trap_data = [["#", "Question", "Attendu", "Résultat"]]
    for i, trap in enumerate(trap_details[:10], 1):
        result = "✓ Réussi" if trap.get("passed") else "✗ Échoué"
        trap_data.append(
            [
                str(i),
                trap.get("query", "—")[:30],
                trap.get("expected", "—")[:30],
                result,
            ]
        )

    trap_table = Table(trap_data, colWidths=[0.4 * inch, 2 * inch, 2 * inch, 1.2 * inch])
    trap_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F5242")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ]
        )
    )
    story.append(trap_table)
    story.append(Spacer(1, 0.3 * inch))

    # Insights
    insights = report.get("insights", {})
    if insights.get("insights"):
        story.append(Paragraph("Insights Automatiques", heading_style))
        for insight in insights.get("insights", [])[:5]:
            severity_color = {
                "success": "#10b981",
                "warning": "#f59e0b",
                "critical": "#ef4444",
            }.get(insight.get("severity"), "#000000")
            title = insight.get("title", "")
            desc = insight.get("description", "")
            story.append(
                Paragraph(
                    f"<b style='color:#{severity_color}'>{title}</b> — {desc}",
                    styles["Normal"],
                )
            )
        story.append(Spacer(1, 0.2 * inch))

    # Footer
    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Paragraph(
            "<i>MemBridge — Rapport généré automatiquement | Hackathon INTELO 2026</i>",
            ParagraphStyle(
                "Footer",
                parent=styles["Normal"],
                fontSize=8,
                alignment=TA_CENTER,
                textColor=colors.grey,
            ),
        )
    )

    # Build PDF
    try:
        doc.build(story)
        return output_path.read_bytes() if output_path.exists() else None
    except Exception as e:
        print(f"PDF generation error: {e}")
        return None
