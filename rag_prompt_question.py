import argparse
import json
import sys
from pathlib import Path

from rag.generate import generate_answer


def main() -> int:
    parser = argparse.ArgumentParser(description="Guardá el prompt del RAG en question.md.")
    parser.add_argument("pregunta", nargs="?", help="Pregunta para el RAG. Si se omite, se lee de stdin.")
    args = parser.parse_args()

    question = args.pregunta if args.pregunta is not None else sys.stdin.readline()
    question = question.strip()
    if not question:
        print("Ingresá una pregunta como argumento o por stdin.", file=sys.stderr)
        return 1

    messages = generate_answer(question)
    prompt = json.dumps(messages, ensure_ascii=False, indent=2)
    Path("question.md").write_text(f"{prompt}\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
