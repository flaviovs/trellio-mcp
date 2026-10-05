import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="MCP server for Trello")
    parser.add_argument(
        "command",
        nargs="?",
        choices=("auth",),
        help="run the interactive authentication flow",
    )
    parser.add_argument(
        "--transport",
        choices=("stdio", "streamable-http", "sse"),
        default="stdio",
        help="MCP transport (default: stdio)",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="HTTP bind host (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8096,
        help="HTTP bind port (default: 8096)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == "auth":
        from trello_mcp.auth import auth_command

        auth_command()
    else:
        from trello_mcp import server

        server.settings.host = args.host
        server.settings.port = args.port
        server.run(transport=args.transport)


if __name__ == "__main__":
    main()
