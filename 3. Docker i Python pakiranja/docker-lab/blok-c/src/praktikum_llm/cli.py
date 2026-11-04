"""Command line interface for talking to a local Ollama model."""
import argparse
import signal
import sys

from dotenv import find_dotenv, load_dotenv

from praktikum_llm import __version__, client


def cmd_status(args: argparse.Namespace) -> int:
    if client.is_running():
        print(f"Ollama is running at {client.get_base_url()}")
        return 0
    print(f"Ollama is NOT running at {client.get_base_url()}", file=sys.stderr)
    return 1


def cmd_models(args: argparse.Namespace) -> int:
    for name in client.list_models():
        print(name)
    return 0


def cmd_ask(args: argparse.Namespace) -> int:
    messages = client.build_messages(args.question, system=args.system)
    print(client.chat(messages, model=args.model))
    return 0


def cmd_chat(args: argparse.Namespace) -> int:
    history: list[dict] = []
    print("Type your message, empty line to quit.")
    while True:
        question = input("> ").strip()
        if not question:
            return 0
        messages = client.build_messages(question, system=args.system, history=history)
        answer = client.chat(messages, model=args.model)
        print(answer)
        history += [{"role": "user", "content": question}, {"role": "assistant", "content": answer}]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="llm", description="Talk to a local Ollama model.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--model", default=None, help="model name (default: OLLAMA_MODEL or llama3.2:1b)")
    parser.add_argument("--system", default=None, help="optional system prompt")
    subcommands = parser.add_subparsers(dest="command", required=True)

    subcommands.add_parser("status", help="check that Ollama is running").set_defaults(handler=cmd_status)
    subcommands.add_parser("models", help="list locally installed models").set_defaults(handler=cmd_models)

    ask = subcommands.add_parser("ask", help="ask one question")
    ask.add_argument("question", help="the question to ask")
    ask.set_defaults(handler=cmd_ask)

    subcommands.add_parser("chat", help="interactive chat with history").set_defaults(handler=cmd_chat)
    return parser


def _exit_on_sigterm(signum, frame) -> None:
    # `docker stop` sends SIGTERM to PID 1. Python ignores it there unless a handler exists.
    raise SystemExit(128 + signum)


def main() -> int:
    signal.signal(signal.SIGTERM, _exit_on_sigterm)
    # usecwd=True: look for .env in the current directory, not next to the installed package.
    load_dotenv(find_dotenv(usecwd=True))
    args = build_parser().parse_args()
    try:
        return args.handler(args)
    except client.OllamaError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
