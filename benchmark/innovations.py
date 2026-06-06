"""Advanced innovations - features that make MemBridge stand out."""

from __future__ import annotations


def generate_heatmap(report: dict) -> dict:
    """Crée une heatmap de performance tour par tour."""
    naive_per_turn = report.get("naive", {}).get("per_turn_tokens", [])
    memory_per_turn = report.get("memory", {}).get("per_turn_tokens", [])

    heatmap_data = []
    for i, (naive, memory) in enumerate(zip(naive_per_turn, memory_per_turn)):
        efficiency = 1 - (memory / max(naive, 1))  # 0-1 range
        heatmap_data.append(
            {
                "turn": i + 1,
                "naive": naive,
                "memory": memory,
                "efficiency": round(efficiency * 100, 1),
                "savings": naive - memory,
            }
        )

    return {
        "data": heatmap_data,
        "max_efficiency": max((d["efficiency"] for d in heatmap_data), default=0),
        "avg_efficiency": sum(d["efficiency"] for d in heatmap_data) / max(len(heatmap_data), 1),
    }


def predict_performance(report: dict, future_turns: int = 10) -> dict:
    """Prédit les tokens si on continue plus longtemps."""
    naive_per_turn = report.get("naive", {}).get("per_turn_tokens", [])
    memory_per_turn = report.get("memory", {}).get("per_turn_tokens", [])

    if not naive_per_turn or not memory_per_turn:
        return {"error": "Not enough data"}

    # Simple linear regression
    def predict_trend(data: list[float], future_steps: int) -> list[float]:
        n = len(data)
        if n < 2:
            return [data[0]] * future_steps

        # Calculate trend
        x = list(range(n))
        y = data
        x_mean = sum(x) / n
        y_mean = sum(y) / n

        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))

        slope = numerator / max(denominator, 1)
        intercept = y_mean - slope * x_mean

        predictions = []
        for i in range(future_steps):
            pred = slope * (n + i) + intercept
            predictions.append(max(pred, 0))  # No negative tokens

        return predictions

    naive_pred = predict_trend(naive_per_turn, future_turns)
    memory_pred = predict_trend(memory_per_turn, future_turns)

    current_turn = len(naive_per_turn)
    predictions = []
    for i, (n, m) in enumerate(zip(naive_pred, memory_pred)):
        predictions.append(
            {
                "turn": current_turn + i + 1,
                "naive_predicted": round(n),
                "memory_predicted": round(m),
                "projected_savings": round(n - m),
            }
        )

    return {
        "current_turn": current_turn,
        "predictions": predictions,
        "note": "Based on observed trends",
    }


def generate_smart_recommendations(report: dict) -> list[dict]:
    """Génère des recommandations intelligentes."""
    recommendations = []

    savings_pct = report.get("savings_pct", 0)
    quality_score = report.get("quality", {}).get("score_pct", 0)

    # Recommandation 1: Économie
    if savings_pct >= 75:
        recommendations.append(
            {
                "category": "Economy",
                "icon": "🚀",
                "title": "Outstanding Compression",
                "suggestion": "Your compression is exceptional. Share your strategy with the team!",
                "priority": "low",
            }
        )
    elif savings_pct < 70:
        recommendations.append(
            {
                "category": "Economy",
                "icon": "⚙️",
                "title": "Optimize Summarization",
                "suggestion": (
                    "Improve your summarization logic to save more tokens. "
                    "Try LLM-based summarization."
                ),
                "priority": "high",
            }
        )

    # Recommandation 2: Qualité
    if quality_score >= 90:
        recommendations.append(
            {
                "category": "Quality",
                "icon": "⭐",
                "title": "Perfect Quality",
                "suggestion": "Your quality is perfect. Focus on maximizing savings now.",
                "priority": "low",
            }
        )
    elif quality_score < 80:
        recommendations.append(
            {
                "category": "Quality",
                "icon": "🔍",
                "title": "Improve Search Accuracy",
                "suggestion": (
                    "Use better embeddings or increase search depth "
                    "to improve trap question accuracy."
                ),
                "priority": "high",
            }
        )

    # Recommandation 3: Performance
    naive_per_turn = report.get("naive", {}).get("per_turn_tokens", [])
    if naive_per_turn and len(naive_per_turn) > 1:
        growth = (naive_per_turn[-1] - naive_per_turn[0]) / max(naive_per_turn[0], 1)
        if growth > 0.5:
            recommendations.append(
                {
                    "category": "Performance",
                    "icon": "📈",
                    "title": "High Token Growth",
                    "suggestion": (
                        "Token usage is growing too fast. "
                        "Consider pruning old memories or increasing compression."
                    ),
                    "priority": "medium",
                }
            )

    # Recommandation 4: Architecture
    insights = report.get("insights", {}).get("insights", [])
    if len(insights) >= 4:
        recommendations.append(
            {
                "category": "Architecture",
                "icon": "🏗️",
                "title": "Solid Foundation",
                "suggestion": (
                    "Your architecture is solid. Consider adding caching or multi-level memory."
                ),
                "priority": "low",
            }
        )

    return recommendations


def create_comparison_snapshot(report: dict, previous_reports: list[dict] = None) -> dict:
    """Crée un snapshot pour comparaison avec runs précédents."""
    current = {
        "timestamp": report.get("timestamp", "now"),
        "savings": report.get("savings_pct", 0),
        "quality": report.get("quality", {}).get("score_pct", 0),
        "tokens_naive": report.get("naive", {}).get("total_tokens", 0),
        "tokens_memory": report.get("memory", {}).get("total_tokens", 0),
    }

    comparison = {
        "current": current,
        "improvements": {},
    }

    if previous_reports and len(previous_reports) > 0:
        previous = previous_reports[-1]  # Last run
        comparison["improvements"] = {
            "savings_delta": round(current["savings"] - previous.get("savings", 0), 1),
            "quality_delta": round(current["quality"] - previous.get("quality", 0), 1),
            "tokens_saved_delta": (current["tokens_naive"] - current["tokens_memory"])
            - (previous.get("tokens_naive", 0) - previous.get("tokens_memory", 0)),
        }

    return comparison


def calculate_efficiency_metrics(report: dict) -> dict:
    """Calcule des métriques d'efficacité avancées."""
    naive_per_turn = report.get("naive", {}).get("per_turn_tokens", [])
    memory_per_turn = report.get("memory", {}).get("per_turn_tokens", [])

    if not naive_per_turn or not memory_per_turn:
        return {}

    # Variance (stabilité)
    naive_mean = sum(naive_per_turn) / len(naive_per_turn)
    memory_mean = sum(memory_per_turn) / len(memory_per_turn)

    naive_variance = sum((x - naive_mean) ** 2 for x in naive_per_turn) / len(naive_per_turn)
    memory_variance = sum((x - memory_mean) ** 2 for x in memory_per_turn) / len(memory_per_turn)

    # Efficiency ratio
    efficiency_ratio = naive_variance / max(memory_variance, 1)

    # Peak vs Average
    naive_peak = max(naive_per_turn)
    memory_peak = max(memory_per_turn)

    return {
        "naive_variance": round(naive_variance, 1),
        "memory_variance": round(memory_variance, 1),
        "stability_ratio": round(efficiency_ratio, 2),
        "peak_reduction": round(((naive_peak - memory_peak) / naive_peak) * 100, 1),
        "consistency_score": round(100 - (memory_variance / max(memory_mean, 1)), 1),
    }
