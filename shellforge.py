"""
ShellForge — reverse & bind shell payload generator CLI.

Authorized penetration testing / red team / CTF use only.

Author: Mostafa Tamime
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from encoders.encode import apply_encoding
from generators.awk import AwkGenerator
from generators.bash_sh import BashGenerator
from generators.base import PayloadGenerator
from generators.c_lang import CGenerator
from generators.csharp import CsharpGenerator
from generators.golang import GolangGenerator
from generators.java_lang import JavaGenerator
from generators.lua import LuaGenerator
from generators.netcat import NetcatGenerator, NetcatMkfifoGenerator
from generators.perl_lang import PerlGenerator
from generators.php_lang import PhpGenerator
from generators.python_lang import Python3Generator, PythonGenerator
from generators.ruby_lang import RubyGenerator
from generators.powershell import PowershellGenerator
from generators.socat import SocatGenerator
from listeners.listener_helper import print_listeners

try:
    from rich.console import Console
    from rich.panel import Panel

    RICH = True
    console = Console()
except ImportError:  # pragma: no cover
    RICH = False
    console = None  # type: ignore[assignment]

LEGAL_DISCLAIMER = (
    "AUTHORIZED USE ONLY — ShellForge is intended solely for authorized "
    "security testing, red team engagements, CTF competitions, and lab "
    "environments. Unauthorized use against systems you do not own or lack "
    "explicit written permission to test is illegal."
)

AUTHOR = "Mostafa Tamime"
VERSION = "1.0.0"

# ASCII banner matching assets/logo.svg (anvil + spark + prompt)
BANNER = r"""
                 *
                /|\
               * | *
            .-----------.
           /   >_        \
          (_______________ )
             ||       ||
             ||_______||
              '-------'
             SHELLFORGE
"""
BANNER_PLAIN = BANNER

# Language registry — drop a new generator module in generators/ and add it here.
LANGUAGES: dict[str, PayloadGenerator] = {
    "bash": BashGenerator(),
    "python": PythonGenerator(),
    "python3": Python3Generator(),
    "perl": PerlGenerator(),
    "php": PhpGenerator(),
    "ruby": RubyGenerator(),
    "nc": NetcatGenerator(),
    "nc-mkfifo": NetcatMkfifoGenerator(),
    "socat": SocatGenerator(),
    "powershell": PowershellGenerator(),
    "java": JavaGenerator(),
    "csharp": CsharpGenerator(),
    "c": CGenerator(),
    "golang": GolangGenerator(),
    "lua": LuaGenerator(),
    "awk": AwkGenerator(),
}

# Languages that prefer multi-line file output when --output is given
FILE_ORIENTED = {"powershell", "c", "java", "csharp", "golang"}


def _print_banner() -> None:
    """Print the ShellForge anvil logo banner + legal notice."""
    if RICH and console:
        # Spark / wordmark in terminal green; anvil body in light gray
        console.print(
            "                 [bold #3DDC97]*[/]\n"
            "                [bold #3DDC97]/|\\[/]\n"
            "               [bold #3DDC97]*[/] | [bold #3DDC97]*[/]\n"
            "            [white].-----------.[/]\n"
            "           [white]/   [bold black on white] >_ [/]       \\[/]\n"
            "          [white](_______________ )[/]\n"
            "             [white]||       ||[/]\n"
            "             [white]||_______||[/]\n"
            "              [white]'-------'[/]\n"
            "             [bold #3DDC97]SHELLFORGE[/]"
        )
        console.print(
            f"  v{VERSION}  ·  {AUTHOR}  ·  authorized use only",
            style="dim",
        )
        console.print()
        console.print(
            Panel(
                LEGAL_DISCLAIMER,
                title="[bold red]AUTHORIZED USE ONLY[/]",
                border_style="red",
            )
        )
        console.print()
    else:
        print(BANNER_PLAIN)
        print(f"  v{VERSION}  ·  {AUTHOR}  ·  authorized use only")
        print()
        print("=" * 72)
        print(LEGAL_DISCLAIMER)
        print("=" * 72)
        print()


def _print_payload(label: str, payload: str) -> None:
    if RICH and console:
        console.print(f"[bold cyan][{label}][/]")
        console.print(Panel(payload, border_style="green", expand=False))
    else:
        print(f"[{label}]")
        print(payload)
        print()


def _warn(msg: str) -> None:
    if RICH and console:
        console.print(f"[bold yellow][!][/] {msg}")
    else:
        print(f"[!] {msg}")


def _ok(msg: str) -> None:
    if RICH and console:
        console.print(f"[bold green][+][/] {msg}")
    else:
        print(f"[+] {msg}")


def list_languages() -> None:
    """Print supported language keys."""
    langs = sorted(LANGUAGES.keys())
    if RICH and console:
        console.print("[bold]Supported languages:[/]")
        console.print(", ".join(langs) + ", all")
    else:
        print("Supported languages:")
        print(", ".join(langs) + ", all")


def get_payload(
    generator: PayloadGenerator,
    lang: str,
    shell_type: str,
    ip: Optional[str],
    port: int,
    to_file: bool,
) -> str:
    """Generate payload, preferring script form for file-oriented langs."""
    wants_script = to_file and lang in FILE_ORIENTED and hasattr(
        generator, f"{shell_type}_script"
    )

    if shell_type == "reverse":
        if not ip:
            raise ValueError("IP is required for reverse shells")
        if wants_script:
            return generator.reverse_script(ip, port)  # type: ignore[attr-defined]
        return generator.reverse(ip, port)

    if shell_type == "bind":
        if wants_script:
            return generator.bind_script(port)  # type: ignore[attr-defined]
        return generator.bind(port)

    raise ValueError(f"Unknown shell type: {shell_type}")


def save_payload(path: Path, payload: str, extension: str) -> Path:
    """Write payload to *path*, appending *extension* if path has no suffix."""
    out = path
    if not out.suffix:
        out = out.with_suffix(extension)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(payload, encoding="utf-8")
    return out


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shellforge",
        description=(
            "ShellForge — reverse & bind shell payload generator "
            f"(Author: {AUTHOR})"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l bash\n"
            "  python shellforge.py -t bind -p 5555 -l python3 --listener\n"
            "  python shellforge.py -t reverse -i 10.10.14.5 -p 443 -l powershell -o rev.ps1\n"
            "  python shellforge.py --list-langs\n"
        ),
    )
    parser.add_argument(
        "-t",
        "--type",
        choices=["reverse", "bind"],
        help="Shell type: reverse or bind",
    )
    parser.add_argument(
        "-i",
        "--ip",
        help="Attacker IP (required for reverse shells)",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        help="Port number (required for payload generation)",
    )
    parser.add_argument(
        "-l",
        "--lang",
        default="bash",
        help="Language/tool (or 'all'). Use --list-langs to see options.",
    )
    parser.add_argument(
        "--encode",
        choices=["none", "base64", "urlencode", "ps-encoded"],
        default="none",
        help="Encoding to apply to the payload (default: none)",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Optional file path to save the payload",
    )
    parser.add_argument(
        "--listener",
        action="store_true",
        help="Print matching listener commands for this port/type",
    )
    parser.add_argument(
        "--list-langs",
        action="store_true",
        help="List all supported languages and exit",
    )
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Skip banner and legal disclaimer",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"ShellForge {VERSION} by {AUTHOR}",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.no_banner and not args.list_langs:
        _print_banner()

    if args.list_langs:
        list_languages()
        return 0

    if args.type is None or args.port is None:
        parser.error("--type/-t and --port/-p are required (unless --list-langs)")

    if args.type == "reverse" and not args.ip:
        parser.error("--ip/-i is required for reverse shells")

    lang_key = args.lang.lower()
    if lang_key == "all":
        targets = list(LANGUAGES.items())
    elif lang_key in LANGUAGES:
        targets = [(lang_key, LANGUAGES[lang_key])]
    else:
        _warn(f"Unknown language '{args.lang}'. Use --list-langs.")
        return 1

    output_path = Path(args.output) if args.output else None

    for name, generator in targets:
        try:
            to_file = output_path is not None and lang_key != "all"
            payload = get_payload(
                generator,
                name,
                args.type,
                args.ip,
                args.port,
                to_file=to_file or (output_path is not None and name in FILE_ORIENTED),
            )
            payload = apply_encoding(payload, args.encode)
        except Exception as exc:  # noqa: BLE001
            _warn(f"{name}: {exc}")
            continue

        label = f"{args.type.upper()} | {name}"
        if args.encode != "none":
            label += f" | encode={args.encode}"

        if output_path and lang_key != "all":
            saved = save_payload(output_path, payload, generator.file_extension())
            _ok(f"Payload written to {saved}")
            _print_payload(label, payload)
        elif output_path and lang_key == "all":
            # Save each language to a sibling file
            stem = output_path.stem or "payload"
            parent = output_path.parent
            per_file = parent / f"{stem}_{name}{generator.file_extension()}"
            # For file-oriented langs, regenerate with script form
            if name in FILE_ORIENTED:
                payload = get_payload(
                    generator, name, args.type, args.ip, args.port, to_file=True
                )
                payload = apply_encoding(payload, args.encode)
            per_file.write_text(payload, encoding="utf-8")
            _ok(f"{name} -> {per_file}")
        else:
            _print_payload(label, payload)

    if args.listener:
        print_listeners(
            args.port,
            shell_type=args.type,
            ip=args.ip or "0.0.0.0",
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
