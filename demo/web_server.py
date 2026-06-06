"""Serveur web live — dashboard, benchmark SSE, mémoire multi-modale."""

from __future__ import annotations

import io
import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from benchmark.harness import _seed_trap_session, run_benchmark, save_report
from benchmark.live import stream_benchmark
from benchmark.scoring_advanced import calculate_score, save_leaderboard_entry, get_leaderboard
from demo.export_pdf import generate_pdf_report
from memory_mcp.tools import MemoryTools

ROOT = Path(__file__).parent.parent
DASHBOARD = ROOT / "dashboard"
RESULTS = ROOT / "benchmark" / "results"

app = FastAPI(title="MemBridge Live", version="3.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

tools = MemoryTools()
SESSION = "live-demo"
_seeded = False


def _ensure_demo_session() -> None:
    global _seeded
    if not _seeded:
        _seed_trap_session(tools, SESSION)
        _seeded = True


class LocateBody(BaseModel):
    latitude: float
    longitude: float
    label: str = "Démo jury"


class TranscribeBody(BaseModel):
    transcript: str
    source: str = "audio"
    language: str = "fr"


class VisionBody(BaseModel):
    image_b64: str = ""
    label: str = "Capture caméra"


class StoreBody(BaseModel):
    content: str
    tags: list[str] = []


class ForgetBody(BaseModel):
    query: str | None = None
    tag: str | None = "noise"


class TranslateBody(BaseModel):
    text: str
    target_lang: str = "en"


class ShareBody(BaseModel):
    from_session: str = "live-demo"
    to_session: str = "agent-2"
    query: str = "contrat client premium"


@app.get("/")
def index() -> FileResponse:
    return FileResponse(DASHBOARD / "index.html")


@app.get("/home")
def home() -> FileResponse:
    return FileResponse(DASHBOARD / "home.html")


@app.get("/pitch")
def pitch() -> FileResponse:
    return FileResponse(DASHBOARD / "pitch.html")


@app.get("/presentation")
def presentation() -> FileResponse:
    return FileResponse(DASHBOARD / "presentation.html")


@app.get("/premium")
def premium() -> FileResponse:
    return FileResponse(DASHBOARD / "premium.html")


@app.get("/leaderboard")
def leaderboard() -> FileResponse:
    return FileResponse(DASHBOARD / "leaderboard.html")


@app.get("/memory-graph")
def memory_graph() -> FileResponse:
    return FileResponse(DASHBOARD / "memory-graph.html")


@app.get("/interactive")
def interactive() -> FileResponse:
    return FileResponse(DASHBOARD / "interactive.html")


@app.get("/battle")
def battle() -> FileResponse:
    return FileResponse(DASHBOARD / "battle.html")


@app.get("/api/benchmark")
def api_benchmark(turns: int = 50) -> dict:
    report = run_benchmark(turn_count=max(10, min(turns, 100)))
    save_report(report)

    # Add score and save to leaderboard
    report["score"] = calculate_score(report)
    leaderboard_result = save_leaderboard_entry(report)
    report["leaderboard_rank"] = leaderboard_result["rank"]

    return report


@app.get("/api/benchmark/live")
def api_benchmark_live() -> StreamingResponse:
    """SSE — benchmark tour par tour pour démo jury."""

    def generate():
        for chunk in stream_benchmark(turn_count=50):
            yield chunk

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/api/report")
def api_report() -> dict:
    path = RESULTS / "report.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    report = run_benchmark()
    save_report(report)
    return report


@app.get("/api/memory")
def api_memory() -> dict:
    _ensure_demo_session()
    entries = tools.store.list_session(SESSION)
    return {
        "session": SESSION,
        "count": len(entries),
        "entries": [
            {
                "id": e.id,
                "turn": e.turn,
                "content": e.content[:120],
                "tags": e.tags,
                "metadata": e.metadata or {},
            }
            for e in entries
        ],
        "summary": tools.memory_summarize(session=SESSION),
    }


@app.get("/api/memory/graph")
def api_memory_graph() -> dict:
    """Graphe des souvenirs pour visualisation."""
    _ensure_demo_session()
    entries = tools.store.list_session(SESSION)
    nodes = [
        {
            "id": e.id,
            "label": f"t{e.turn}",
            "type": (
                "fact"
                if "fact" in e.tags
                else "geo"
                if "geo" in e.tags
                else "media"
                if any(t in e.tags for t in ("audio", "video", "vision", "transcript"))
                else "msg"
            ),
            "preview": e.content[:50],
        }
        for e in entries[:40]
    ]
    edges = [{"from": nodes[i]["id"], "to": nodes[i + 1]["id"]} for i in range(len(nodes) - 1)]
    return {"nodes": nodes, "edges": edges}


@app.post("/api/locate")
def api_locate(body: LocateBody) -> dict:
    _ensure_demo_session()
    return tools.memory_locate(
        session=SESSION,
        latitude=body.latitude,
        longitude=body.longitude,
        label=body.label,
        turn=tools.store.count(SESSION) + 1,
    )


@app.post("/api/transcribe")
def api_transcribe(body: TranscribeBody) -> dict:
    _ensure_demo_session()
    return tools.memory_transcribe(
        session=SESSION,
        transcript=body.transcript,
        source=body.source,
        language=body.language,
        turn=tools.store.count(SESSION) + 1,
    )


@app.post("/api/vision")
def api_vision(body: VisionBody) -> dict:
    _ensure_demo_session()
    return tools.memory_store(
        content=f"📷 Image : {body.label}",
        tags=["vision", "image", "capture"],
        session=SESSION,
        turn=tools.store.count(SESSION) + 1,
        metadata={"label": body.label},
    )


@app.get("/api/search")
def api_search(q: str) -> dict:
    _ensure_demo_session()
    return tools.memory_search(query=q, top_k=3, session=SESSION)


@app.post("/api/store")
def api_store(body: StoreBody) -> dict:
    _ensure_demo_session()
    return tools.memory_store(
        content=body.content,
        tags=body.tags or ["demo"],
        session=SESSION,
        turn=tools.store.count(SESSION) + 1,
    )


@app.get("/api/summarize")
def api_summarize() -> dict:
    _ensure_demo_session()
    return tools.memory_summarize(session=SESSION)


@app.get("/api/stats")
def api_stats() -> dict:
    _ensure_demo_session()
    return tools.memory_stats()


@app.post("/api/forget")
def api_forget(body: ForgetBody) -> dict:
    _ensure_demo_session()
    return tools.memory_forget(
        session=SESSION,
        query=body.query,
        tag=body.tag,
    )


@app.post("/api/translate")
def api_translate(body: TranslateBody) -> dict:
    return tools.memory_translate(text=body.text, target_lang=body.target_lang)


@app.get("/api/timeline")
def api_timeline() -> dict:
    _ensure_demo_session()
    return tools.memory_timeline(session=SESSION)


@app.post("/api/share")
def api_share(body: ShareBody) -> dict:
    _ensure_demo_session()
    return tools.memory_share(
        from_session=body.from_session,
        to_session=body.to_session,
        query=body.query,
    )


@app.post("/api/seed")
def api_seed() -> dict:
    """Recharge la session démo avec les faits pièges."""
    global _seeded
    _seeded = False
    _ensure_demo_session()
    entries = tools.store.list_session(SESSION)
    return {"seeded": True, "session": SESSION, "count": len(entries)}


@app.get("/api/leaderboard")
def api_leaderboard() -> dict:
    """Retourne le leaderboard avec top 20 scores."""
    leaderboard = get_leaderboard()
    return {
        "entries": leaderboard,
        "count": len(leaderboard),
        "top_score": leaderboard[0]["score"]["total"] if leaderboard else 0,
    }


@app.get("/api/export/pdf")
def api_export_pdf() -> StreamingResponse:
    path = RESULTS / "report.json"
    if path.exists():
        report = json.loads(path.read_text(encoding="utf-8"))
    else:
        report = run_benchmark()
        save_report(report)

    pdf_bytes = generate_pdf_report(report)
    if not pdf_bytes:
        return StreamingResponse(
            io.BytesIO(b"Install: pip install reportlab"),
            media_type="text/plain",
        )

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=MemBridge-Report.pdf"},
    )


app.mount("/dashboard", StaticFiles(directory=DASHBOARD), name="dashboard")


def main() -> None:
    import uvicorn

    uvicorn.run("demo.web_server:app", host="0.0.0.0", port=8765, reload=False)


if __name__ == "__main__":
    main()
