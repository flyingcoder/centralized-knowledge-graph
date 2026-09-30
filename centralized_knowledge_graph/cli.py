from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def cursor_config_path(scope: str) -> Path:
    if scope == "project":
        return Path.cwd() / ".cursor" / "mcp.json"
    return Path.home() / ".cursor" / "mcp.json"


def load_config(path: Path) -> dict:
    if not path.exists():
        return {"mcpServers": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Cursor MCP config must be a JSON object: {path}")
    data.setdefault("mcpServers", {})
    if not isinstance(data["mcpServers"], dict):
        raise SystemExit(f"'mcpServers' must be an object: {path}")
    return data


def install_cursor(scope: str, command: str, server_name: str, url: str | None) -> Path:
    path = cursor_config_path(scope)
    path.parent.mkdir(parents=True, exist_ok=True)
    config = load_config(path)

    if url:
        server = {"url": url}
    else:
        server = {"command": command, "args": ["serve"]}

    config["mcpServers"][server_name] = server
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="centralized-knowledge-graph",
        description="Install the Centralized Knowledge Graph MCP into Cursor.",
    )
    sub = parser.add_subparsers(dest="action", required=True)

    install = sub.add_parser("install", help="Configure the MCP server in Cursor.")
    install.add_argument(
        "--scope",
        choices=("user", "project"),
        default="user",
        help="Install for the current user or current project.",
    )
    install.add_argument(
        "--name",
        default="centralized-knowledge-graph",
        help="MCP server name shown to Cursor.",
    )
    install.add_argument(
        "--command",
        default=os.environ.get(
            "CKG_MCP_COMMAND", "centralized-knowledge-graph"
        ),
        help="Local executable Cursor should launch.",
    )
    install.add_argument(
        "--url",
        default=os.environ.get("CKG_MCP_URL"),
        help="Optional remote MCP URL. If supplied, Cursor uses URL transport.",
    )

    args = parser.parse_args()

    if args.action == "install":
        path = install_cursor(args.scope, args.command, args.name, args.url)
        print(f"Installed '{args.name}' into {path}")
        print("Restart Cursor or reload MCP servers to pick up the configuration.")


if __name__ == "__main__":
    main()
