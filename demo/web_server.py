"""Serveur web live — dashboard, benchmark, mémoire multi-modale."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from benchmark.harness import _seed_trap_session, run_benchmark, save_report
from demo.export_pdf import generate_pdf_report
from memory_mcp.tools import MemoryTools
from fastapi.responses import StreamingResponse
import io

ROOT = Path(__file__).parent.parent
DASHBOARD = ROOT / "dashboard"
RESULTS = ROOT / "benchmark" / "results"

app = FastAPI(title="MemBridge Live", version="2.0.0")
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


@app.get("/")
def index() -> FileResponse:
    return FileResponse(DASHBOARD / "index.html")


@app.get("/pitch")
def pitch() -> FileResponse:
    return FileResponse(DASHBOARD / "pitch.html")


@app.get("/api/benchmark")
def api_benchmark() -> dict:
    report = run_benchmark(turn_count=50)
    save_report(report)
    return report


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


@app.get("/api/timeline")
def api_timeline() -> dict:
    _ensure_demo_session()
    entries = tools.store.list_session(SESSION)
    return {
        "turns": [
            {
                "turn": e.turn,
                "type": (
                    "fact"
                    if "fact" in e.tags
                    else "geo"
                    if "geo" in e.tags
                    else "media"
                    if any(t in e.tags for t in ("audio", "video", "call", "transcript"))
                    else "msg"
                ),
                "preview": e.content[:80],
            }
            for e in entries
        ]
    }


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
        content=f"📷 Image capturée : {body.label} ({len(body.image_b64)} chars b64)",
        tags=["vision", "image", "capture"],
        session=SESSION,
        turn=tools.store.count(SESSION) + 1,
        metadata={"label": body.label, "has_image": bool(body.image_b64)},
    )


@app.get("/api/search")
def api_search(q: str) -> dict:
    _ensure_demo_session()
    return tools.memory_search(query=q, top_k=3, session=SESSION)


@app.get("/api/trap/{trap_id}")
def api_trap(trap_id: int) -> dict:
    _ensure_demo_session()
    traps = json.loads((ROOT / "benchmark" / "trap_questions.json").read_text(encoding="utf-8"))
    if trap_id < 0 or trap_id >= len(traps):
        return {"error": "invalid trap_id"}
    trap = traps[trap_id]
    result = tools.memory_search(trap["query"], top_k=1, session=SESSION)
    return {"trap": trap, "result": result}


@app.get("/api/stats")
def api_stats() -> dict:
    """Advanced performance stats for the current session."""
    _ensure_demo_session()
    stats = tools.memory_stats()
    entries = tools.store.list_session(SESSION)

    return {
        "session": SESSION,
        "entries_count": len(entries),
        "total_embeddings": stats.get("embedding_count", 0),
        "total_searches": stats.get("search_count", 0),
        "avg_search_latency_ms": stats.get("avg_search_ms", 0),
        "memory_usage_kb": stats.get("memory_kb", 0),
        "compression_ratio": stats.get("compression_ratio", 0),
    }


@app.get("/api/export/pdf")
async def api_export_pdf() -> StreamingResponse:
    """Export current report as PDF."""
    path = RESULTS / "report.json"
    if not path.exists():
        report = run_benchmark()
        save_report(report)
    else:
        report = json.loads(path.read_text(encoding="utf-8"))

    pdf_bytes = generate_pdf_report(report)
    if not pdf_bytes:
        return StreamingResponse(
            io.BytesIO(b"PDF generation failed"),
            media_type="text/plain",
            headers={"Content-Disposition": "attachment; filename=error.txt"}
        )

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=MemBridge-Report.pdf"}
    )


app.mount("/dashboard", StaticFiles(directory=DASHBOARD), name="dashboard")


def main() -> None:
    import uvicorn

    uvicorn.run("demo.web_server:app", host="0.0.0.0", port=8765, reload=False)


if __name__ == "__main__":
    main()
