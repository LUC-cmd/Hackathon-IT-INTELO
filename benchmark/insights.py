"""Génération automatique d'insights et recommandations — Premium reporting."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Insight:
    title: str
    description: str
    severity: str  # "critical" | "warning" | "info" | "success"
    metric: str
    value: str


def generate_insights(report: dict) -> dict:
    """Analyse le rapport et génère des insights actionnables."""
    insights = []

    savings_pct = report.get("savings_pct", 0)
    quality = report.get("quality", {})

    # Axe 1: Économie de tokens
    if savings_pct >= 75:
        insights.append(Insight(
            title="Compression exceptionnelle",
            description="L'économie de tokens dépasse 75%, bien au-delà du seuil de 70%.",
            severity="success",
            metric="Économie",
            value=f"{savings_pct}%",
        ))
    elif savings_pct >= 70:
        insights.append(Insight(
            title="Objectif atteint",
            description="L'économie de tokens satisfait le critère minimum de 70%.",
            severity="success",
            metric="Économie",
            value=f"{savings_pct}%",
        ))
    elif savings_pct >= 60:
        insights.append(Insight(
            title="Performance acceptable",
            description="L'économie est solide mais pourrait être optimisée davantage.",
            severity="warning",
            metric="Économie",
            value=f"{savings_pct}%",
        ))
    else:
        insights.append(Insight(
            title="Économie insuffisante",
            description="L'économie de tokens ne respecte pas le critère de 70%.",
            severity="critical",
            metric="Économie",
            value=f"{savings_pct}%",
        ))

    # Axe 2: Qualité de réponse
    quality_score = quality.get("score_pct", 0)
    if quality_score >= 90:
        insights.append(Insight(
            title="Qualité excellente",
            description="Excellente qualité malgré la compression.",
            severity="success",
            metric="Qualité",
            value=f"{quality_score}%",
        ))
    elif quality_score >= 80:
        insights.append(Insight(
            title="Qualité maintenue",
            description="La qualité reste au-dessus du seuil de 80%, critère de succès atteint.",
            severity="success",
            metric="Qualité",
            value=f"{quality_score}%",
        ))
    else:
        insights.append(Insight(
            title="Qualité dégradée",
            description="Qualité sous 80%. Vérifier la recherche sémantique.",
            severity="critical",
            metric="Qualité",
            value=f"{quality_score}%",
        ))

    # Axe 3: Croissance contextuelle
    naive_per_turn = report.get("naive", {}).get("per_turn_tokens", [])
    memory_per_turn = report.get("memory", {}).get("per_turn_tokens", [])

    if naive_per_turn and memory_per_turn:
        naive_growth = (naive_per_turn[-1] - naive_per_turn[0]) / max(naive_per_turn[0], 1)
        memory_growth = (memory_per_turn[-1] - memory_per_turn[0]) / max(memory_per_turn[0], 1)

        if abs(memory_growth) < 0.1:
            insights.append(Insight(
                title="Contexte stable",
                description="Le coût contextuel reste quasi-plat sur la durée de la conversation.",
                severity="success",
                metric="Croissance",
                value=f"{memory_growth*100:.1f}%",
            ))
        elif memory_growth > naive_growth * 0.5:
            insights.append(Insight(
                title="Croissance à surveiller",
                description="Le contexte croît. Vérifier que la compression fonctionne.",
                severity="warning",
                metric="Croissance",
                value=f"{memory_growth*100:.1f}%",
            ))

    # Axe 4: Pièges (dépendance contextuelle)
    passed = quality.get("passed", 0)
    total = quality.get("total", 10)
    trap_ratio = passed / max(total, 1)

    if trap_ratio >= 0.8:
        insights.append(Insight(
            title="Dépendance contextuelle maîtrisée",
            description=f"Faits cachés retrouvés : {passed}/{total}.",
            severity="success",
            metric="Pièges",
            value=f"{passed}/{total}",
        ))
    elif trap_ratio >= 0.6:
        insights.append(Insight(
            title="Dépendance contextuelle partielle",
            description="Faits partiellement retrouvés. Améliorer les embeddings.",
            severity="warning",
            metric="Pièges",
            value=f"{passed}/{total}",
        ))
    else:
        insights.append(Insight(
            title="Recherche sémantique défaillante",
            description="La plupart des faits cachés ne sont pas retrouvés. Vérifier embeddings.",
            severity="critical",
            metric="Pièges",
            value=f"{passed}/{total}",
        ))

    # Verdict global
    global_pass = savings_pct >= 70 and quality_score >= 80
    if global_pass:
        insights.append(Insight(
            title="✓ HACKATHON GAGNANT",
            description="Critères victoire OK : économie ≥70% et qualité ≥80%.",
            severity="success",
            metric="Verdict",
            value="VICTOIRE",
        ))
    else:
        gaps = []
        if savings_pct < 70:
            gaps.append(f"économie {savings_pct}% (cible 70%)")
        if quality_score < 80:
            gaps.append(f"qualité {quality_score}% (cible 80%)")
        insights.append(Insight(
            title="Objectif non atteint",
            description=f"Gaps: {', '.join(gaps)}",
            severity="critical",
            metric="Verdict",
            value="À améliorer",
        ))

    return {
        "count": len(insights),
        "insights": [
            {
                "title": i.title,
                "description": i.description,
                "severity": i.severity,
                "metric": i.metric,
                "value": i.value,
            }
            for i in insights
        ],
        "summary": _build_summary(insights),
    }


def _build_summary(insights: list[Insight]) -> str:
    """Résumé en français pour le jury."""
    critical = [i for i in insights if i.severity == "critical"]
    success = [i for i in insights if i.severity == "success"]

    parts = []

    if any(i.metric == "Verdict" and i.severity == "success" for i in insights):
        parts.append("🏆 Hackathon gagnant — Résultats exceptionnels")
    elif len(critical) == 0:
        parts.append("✓ Objectif atteint — Tous les critères sont satisfaits")
    else:
        parts.append(f"⚠️  {len(critical)} point(s) critique(s) à résoudre")

    for insight in success[:2]:
        parts.append(f"  • {insight.title}")

    if len(critical) > 0:
        parts.append("\nPoints critiques:")
        for insight in critical[:3]:
            parts.append(f"  ✗ {insight.title}")

    return "\n".join(parts)
