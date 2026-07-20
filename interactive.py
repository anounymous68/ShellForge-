"""
Interactive menu mode for ShellForge.

Walks the user through shell type, language, IP/port, encoding, and
output options without requiring CLI flags.

Author: Mostafa Tamime
"""

from __future__ import annotations

import ipaddress
import re
import sys
from pathlib import Path
from types import ModuleType
from typing import Optional


ENCODE_CHOICES = {
    1: "none",
    2: "base64",
    3: "urlencode",
    4: "ps-encoded",
}


def _resolve_sf(sf: Optional[ModuleType] = None) -> ModuleType:
    """Return the loaded shellforge module (works when run as __main__)."""
    if sf is not None:
        return sf
    if "shellforge" in sys.modules:
        return sys.modules["shellforge"]
    # Running as `python shellforge.py` — caller should pass sf=sys.modules[__name__]
    main = sys.modules.get("__main__")
    if main is not None and hasattr(main, "LANGUAGES"):
        return main
    import shellforge as loaded  # noqa: WPS433

    return loaded


def _info(sf: ModuleType, msg: str) -> None:
    if getattr(sf, "RICH", False) and getattr(sf, "console", None):
        sf.console.print(f"[bold cyan][?][/] {msg}")
    else:
        print(f"[?] {msg}")


def _prompt(message: str) -> str:
    try:
        return input(message).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        raise SystemExit(0) from None


def _prompt_choice(sf: ModuleType, message: str, valid: set[int]) -> int:
    """Prompt until the user enters an integer in *valid*."""
    while True:
        raw = _prompt(message)
        if not raw.isdigit():
            sf._warn(f"Enter a number from {min(valid)}–{max(valid)}.")
            continue
        choice = int(raw)
        if choice not in valid:
            sf._warn(f"Enter a number from {min(valid)}–{max(valid)}.")
            continue
        return choice


def validate_ip(raw: str) -> bool:
    """Return True if *raw* is a valid IP or a simple lab hostname."""
    if not raw:
        return False
    try:
        ipaddress.ip_address(raw)
        return True
    except ValueError:
        return bool(
            re.fullmatch(r"[A-Za-z0-9._-]+", raw) and any(c.isalpha() for c in raw)
        )


def validate_port(raw: str) -> Optional[int]:
    """Return port int if valid (1–65535), else None."""
    if not raw.isdigit():
        return None
    port = int(raw)
    if 1 <= port <= 65535:
        return port
    return None


def _prompt_ip(sf: ModuleType, message: str = "Attacker IP: ") -> str:
    while True:
        raw = _prompt(message)
        if validate_ip(raw):
            return raw
        sf._warn(f"Invalid IP address: {raw!r}. Try again (e.g. 10.10.14.5).")


def _prompt_port(sf: ModuleType, message: str = "Port: ") -> int:
    while True:
        raw = _prompt(message)
        port = validate_port(raw)
        if port is not None:
            return port
        sf._warn("Port must be an integer between 1 and 65535.")


def _prompt_yes_no(
    sf: ModuleType,
    message: str,
    *,
    yes: int = 1,
    no: int = 2,
) -> bool:
    return _prompt_choice(sf, message, {yes, no}) == yes


def _ask_again(sf: ModuleType) -> bool:
    print()
    return _prompt_yes_no(
        sf,
        "Generate another? [1] Yes  [2] No: ",
        yes=1,
        no=2,
    )


def run_interactive(
    show_banner: bool = True,
    sf: Optional[ModuleType] = None,
) -> int:
    """
    Run the interactive ShellForge menu loop.

    Returns a process exit code (0 on normal exit).
    """
    sf = _resolve_sf(sf)
    from encoders.encode import apply_encoding
    from listeners.listener_helper import print_listeners

    if show_banner:
        sf._print_banner()

    lang_names = list(sf.LANGUAGES.keys())

    while True:
        print()
        _info(sf, "Select shell type:")
        print("  [1] Reverse shell")
        print("  [2] Bind shell")
        shell_type = (
            "reverse" if _prompt_choice(sf, "Choice: ", {1, 2}) == 1 else "bind"
        )

        print()
        _info(sf, "Select language:")
        for idx, name in enumerate(lang_names, start=1):
            print(f"  [{idx}] {name}")
        lang_idx = _prompt_choice(
            sf,
            "Choice: ",
            set(range(1, len(lang_names) + 1)),
        )
        lang = lang_names[lang_idx - 1]
        generator = sf.LANGUAGES[lang]

        ip: Optional[str] = None
        if shell_type == "reverse":
            print()
            ip = _prompt_ip(sf)

        print()
        port = _prompt_port(sf)

        print()
        _info(sf, "Encode payload?")
        print("  [1] None")
        print("  [2] Base64")
        print("  [3] URL-encode")
        print("  [4] PowerShell -EncodedCommand")
        encode = ENCODE_CHOICES[
            _prompt_choice(sf, "Choice: ", set(ENCODE_CHOICES))
        ]

        print()
        show_listener = _prompt_yes_no(
            sf,
            "Show listener command? [1] Yes  [2] No: ",
            yes=1,
            no=2,
        )

        print()
        save_file = _prompt_yes_no(
            sf,
            "Save to file? [1] No  [2] Yes: ",
            yes=2,
            no=1,
        )
        output_path: Optional[Path] = None
        if save_file:
            while True:
                path_raw = _prompt("File path: ")
                if path_raw:
                    output_path = Path(path_raw)
                    break
                sf._warn("Path cannot be empty.")

        to_file = output_path is not None
        try:
            payload = sf.get_payload(
                generator,
                lang,
                shell_type,
                ip,
                port,
                to_file=to_file,
            )
            payload = apply_encoding(payload, encode)
        except Exception as exc:  # noqa: BLE001
            sf._warn(str(exc))
            if not _ask_again(sf):
                return 0
            continue

        label = f"{shell_type.upper()} | {lang}"
        if encode != "none":
            label += f" | encode={encode}"

        if output_path is not None:
            saved = sf.save_payload(output_path, payload, generator.file_extension())
            sf._ok(f"Payload written to {saved}")

        print()
        sf._print_payload(label, payload)

        if show_listener:
            print()
            print_listeners(
                port,
                shell_type=shell_type,
                ip=ip or "0.0.0.0",
            )

        if not _ask_again(sf):
            return 0
