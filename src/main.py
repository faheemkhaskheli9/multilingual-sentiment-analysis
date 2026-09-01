"""CLI for the multilingual preprocessing pipeline.

    python -m src.main preprocess --text "No me gusta este producto"
    python -m src.main preprocess --text "I love this!" --lang en
    python -m src.main preprocess --file examples/sample_reviews.jsonl
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from src.preprocessing import PreprocessConfig, Preprocessor, ProcessedDoc


def _emit(doc: ProcessedDoc, source: str | None = None) -> None:
    payload = {
        "language": doc.language,
        "normalized_text": doc.normalized_text,
        "tokens": doc.tokens,
    }
    if source is not None:
        payload["source"] = source
    print(json.dumps(payload, ensure_ascii=False))


def _cmd_preprocess(args: argparse.Namespace) -> int:
    pre = Preprocessor(
        PreprocessConfig(remove_stopwords=args.remove_stopwords)
    )
    if args.text is not None:
        _emit(pre.process(args.text, args.lang))
        return 0

    path = Path(args.file)
    if not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 1
    n = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        _emit(pre.process(row["text"], row.get("lang")), source=row.get("id"))
        n += 1
    print(f"# processed {n} row(s)", file=sys.stderr)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="multilingual-sentiment", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("preprocess", help="Normalize + tokenize text (EN/ES).")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--text")
    g.add_argument("--file")
    p.add_argument("--lang", choices=["en", "es"], help="Force language instead of detecting.")
    p.add_argument("--remove-stopwords", action="store_true")
    p.set_defaults(func=_cmd_preprocess)
    return parser


def main(argv: list[str] | None = None) -> int:
    # Multilingual output: force UTF-8 on consoles that default to a legacy
    # code page (e.g. Windows cp1252) so accented text is not mangled.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
        except (AttributeError, ValueError):  # pragma: no cover - non-reconfigurable stream
            pass
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
