"""Advanced scoring & leaderboard system - shows how good your run is."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json


def calculate_score(report: dict) -> dict:
    """Calcule un score premium basé sur plusieurs dimensions."""

    savings_pct = report.get("savings_pct", 0)
    quality_score = report.get("quality", {}).get("score_pct", 0)

    # CRITÈRES DE SCORING
    # 1. Économie (40 points max)
    economy_score = min(40, (savings_pct / 70) * 40) if savings_pct >= 70 else (savings_pct / 70) * 30

    # 2. Qualité (30 points max)
    quality_points = min(30, (quality_score / 80) * 30) if quality_score >= 80 else (quality_score / 80) * 20

    # 3. Stabilité (20 points max)
    naive_per_turn = report.get("naive", {}).get("per_turn_tokens", [])
    memory_per_turn = report.get("memory", {}).get("per_turn_tokens", [])

    stability_score = 0
    if memory_per_turn:
        # Check si la courbe stagne (bon) ou croît (mauvais)
        first_half = sum(memory_per_turn[:len(memory_per_turn)//2]) / max(len(memory_per_turn)//2, 1)
        second_half = sum(memory_per_turn[len(memory_per_turn)//2:]) / max(len(memory_per_turn) - len(memory_per_turn)//2, 1)
        growth_rate = (second_half / max(first_half, 1)) - 1

        if growth_rate < 0.05:  # Quasi-plat = excellent
            stability_score = 20
        elif growth_rate < 0.2:  # Faible croissance = bon
            stability_score = 15
        elif growth_rate < 0.5:  # Croissance modérée
            stability_score = 10
        else:  # Croissance trop forte
            stability_score = 5

    # 4. Bonus innovation (10 points)
    innovation_bonus = 0
    insights = report.get("insights", {}).get("insights", [])
    if len(insights) >= 4:  # Si insights détaillés
        innovation_bonus = 10

    total_score = economy_score + quality_points + stability_score + innovation_bonus

    return {
        "total": round(total_score, 1),
        "max": 100,
        "grade": grade_from_score(total_score),
        "breakdown": {
            "economy": round(economy_score, 1),
            "quality": round(quality_points, 1),
            "stability": round(stability_score, 1),
            "innovation": innovation_bonus,
        },
        "percentile": get_percentile(total_score),
        "message": get_grade_message(total_score),
    }


def grade_from_score(score: float) -> str:
    """Convertit un score en grade (A+, A, B+, etc)."""
    if score >= 95: return "S+"
    if score >= 90: return "A+"
    if score >= 85: return "A"
    if score >= 80: return "B+"
    if score >= 70: return "B"
    if score >= 60: return "C"
    return "F"


def get_percentile(score: float) -> str:
    """Montre où tu es dans le classement."""
    if score >= 95: return "Top 1%"
    if score >= 90: return "Top 5%"
    if score >= 85: return "Top 10%"
    if score >= 80: return "Top 25%"
    return "Below average"


def get_grade_message(score: float) -> str:
    """Message motivant basé sur le score."""
    if score >= 95:
        return "🏆 LEGENDARY! You've mastered token compression!"
    elif score >= 90:
        return "⭐ EXCELLENT! Outstanding performance."
    elif score >= 85:
        return "✨ GREAT! Very solid implementation."
    elif score >= 80:
        return "👍 GOOD! Meet the requirements."
    elif score >= 70:
        return "⚠️ FAIR! Room for improvement."
    else:
        return "📈 KEEP GOING! You'll get there."


def save_leaderboard_entry(report: dict, run_id: str = None) -> dict:
    """Enregistre un run dans la leaderboard."""

    if run_id is None:
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    score = calculate_score(report)

    entry = {
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "score": score,
        "metrics": {
            "tokens_naive": report.get("naive", {}).get("total_tokens", 0),
            "tokens_memory": report.get("memory", {}).get("total_tokens", 0),
            "savings_pct": report.get("savings_pct", 0),
            "quality_score": report.get("quality", {}).get("score_pct", 0),
        },
    }

    # Save to leaderboard file
    leaderboard_path = Path("benchmark/results/leaderboard.json")
    leaderboard_path.parent.mkdir(parents=True, exist_ok=True)

    if leaderboard_path.exists():
        leaderboard = json.loads(leaderboard_path.read_text())
    else:
        leaderboard = []

    leaderboard.append(entry)
    leaderboard = sorted(leaderboard, key=lambda x: x["score"]["total"], reverse=True)[:20]  # Top 20

    leaderboard_path.write_text(json.dumps(leaderboard, indent=2))

    return {
        "entry": entry,
        "rank": next((i + 1 for i, e in enumerate(leaderboard) if e["run_id"] == run_id), None),
        "total_entries": len(leaderboard),
    }


def get_leaderboard() -> list[dict]:
    """Retourne les top 20 runs."""
    leaderboard_path = Path("benchmark/results/leaderboard.json")
    if leaderboard_path.exists():
        return json.loads(leaderboard_path.read_text())
    return []
