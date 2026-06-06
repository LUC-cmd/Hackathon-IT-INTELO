"""Serveur MCP MemBridge — 4 outils core + bonus différenciants."""

from __future__ import annotations

import asyncio
import json

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from memory_mcp.tools import MemoryTools

app = Server("memory-mcp")
tools_handler = MemoryTools()

BONUS_TOOLS = [
    Tool(
        name="memory_forget",
        description="Oubli intelligent — purge souvenirs obsolètes ou redondants.",
        inputSchema={
            "type": "object",
            "properties": {
                "session": {"type": "string"},
                "query": {"type": "string", "description": "Similarité pour cibler l'oubli"},
                "tag": {"type": "string", "description": "Tag à purger (ex: noise)"},
                "top_k": {"type": "integer", "default": 5},
            },
            "required": ["session"],
        },
    ),
    Tool(
        name="memory_locate",
        description="Mémorise un contexte géographique (lat/lon + label).",
        inputSchema={
            "type": "object",
            "properties": {
                "session": {"type": "string"},
                "latitude": {"type": "number"},
                "longitude": {"type": "number"},
                "label": {"type": "string"},
                "turn": {"type": "integer", "default": 0},
            },
            "required": ["session", "latitude", "longitude"],
        },
    ),
    Tool(
        name="memory_transcribe",
        description="Stocke une transcription audio/vidéo/appel dans la mémoire.",
        inputSchema={
            "type": "object",
            "properties": {
                "session": {"type": "string"},
                "transcript": {"type": "string"},
                "source": {
                    "type": "string",
                    "enum": ["audio", "video", "call"],
                    "default": "audio",
                },
                "language": {"type": "string", "default": "fr"},
                "turn": {"type": "integer", "default": 0},
            },
            "required": ["session", "transcript"],
        },
    ),
    Tool(
        name="memory_translate",
        description="Traduction légère FR↔EN pour agents multilingues.",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "target_lang": {"type": "string", "enum": ["fr", "en"], "default": "en"},
            },
            "required": ["text"],
        },
    ),
    Tool(
        name="memory_share",
        description="Partage de mémoire entre agents/sessions (multi-agent).",
        inputSchema={
            "type": "object",
            "properties": {
                "from_session": {"type": "string"},
                "to_session": {"type": "string"},
                "query": {"type": "string"},
                "top_k": {"type": "integer", "default": 3},
            },
            "required": ["from_session", "to_session", "query"],
        },
    ),
    Tool(
        name="memory_timeline",
        description="Chronologie des souvenirs (fait, géo, média, message).",
        inputSchema={
            "type": "object",
            "properties": {
                "session": {"type": "string", "default": "default"},
            },
        },
    ),
]


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="memory_store",
            description="Stocke un fragment de mémoire avec tags optionnels.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Contenu à mémoriser"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags"},
                    "session": {"type": "string", "description": "ID de session"},
                    "turn": {"type": "integer", "description": "Numéro de tour"},
                    "metadata": {"type": "object", "description": "Métadonnées (geo, source…)"},
                },
                "required": ["content"],
            },
        ),
        Tool(
            name="memory_search",
            description="Recherche sémantique dans la mémoire.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Requête de recherche"},
                    "top_k": {
                        "type": "integer",
                        "description": "Nombre de résultats",
                        "default": 5,
                    },
                    "session": {"type": "string", "description": "Filtrer par session"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="memory_summarize",
            description="Résume compressé de l'historique d'une session.",
            inputSchema={
                "type": "object",
                "properties": {
                    "session": {"type": "string", "description": "ID de session"},
                    "max_chars": {
                        "type": "integer",
                        "description": "Taille max du résumé",
                        "default": 500,
                    },
                },
            },
        ),
        Tool(
            name="memory_stats",
            description="Retourne les statistiques de consommation de tokens.",
            inputSchema={"type": "object", "properties": {}},
        ),
        *BONUS_TOOLS,
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "memory_store":
        result = tools_handler.memory_store(
            content=arguments["content"],
            tags=arguments.get("tags"),
            session=arguments.get("session", "default"),
            turn=arguments.get("turn", 0),
            metadata=arguments.get("metadata"),
        )
    elif name == "memory_search":
        result = tools_handler.memory_search(
            query=arguments["query"],
            top_k=arguments.get("top_k", 5),
            session=arguments.get("session"),
        )
    elif name == "memory_summarize":
        result = tools_handler.memory_summarize(
            session=arguments.get("session", "default"),
            max_chars=arguments.get("max_chars", 500),
        )
    elif name == "memory_stats":
        result = tools_handler.memory_stats()
    elif name == "memory_forget":
        result = tools_handler.memory_forget(
            session=arguments["session"],
            query=arguments.get("query"),
            tag=arguments.get("tag"),
            top_k=arguments.get("top_k", 5),
        )
    elif name == "memory_locate":
        result = tools_handler.memory_locate(
            session=arguments["session"],
            latitude=arguments["latitude"],
            longitude=arguments["longitude"],
            label=arguments.get("label", ""),
            turn=arguments.get("turn", 0),
        )
    elif name == "memory_transcribe":
        result = tools_handler.memory_transcribe(
            session=arguments["session"],
            transcript=arguments["transcript"],
            source=arguments.get("source", "audio"),
            language=arguments.get("language", "fr"),
            turn=arguments.get("turn", 0),
        )
    elif name == "memory_translate":
        result = tools_handler.memory_translate(
            text=arguments["text"],
            target_lang=arguments.get("target_lang", "en"),
        )
    elif name == "memory_share":
        result = tools_handler.memory_share(
            from_session=arguments["from_session"],
            to_session=arguments["to_session"],
            query=arguments["query"],
            top_k=arguments.get("top_k", 3),
        )
    elif name == "memory_timeline":
        result = tools_handler.memory_timeline(session=arguments.get("session", "default"))
    else:
        raise ValueError(f"Outil inconnu : {name}")

    return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]


async def run_server() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


def main() -> None:
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
