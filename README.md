<p align="center">
  <img src="assets/logo.svg" alt="ShellForge logo" width="180"/>
</p>

<h1 align="center">ShellForge</h1>

<p align="center">
  A modular reverse, bind, and web shell payload generator for authorized security testing.
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/python-3.9%2B-blue">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
  <img alt="Tests" src="https://img.shields.io/badge/tests-pytest-brightgreen">
  <img alt="Platform" src="https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey">
</p>

<p align="center"><strong>Author:</strong> Mostafa Tamime</p>

---

## Table of contents

- [Overview](#overview)
- [Legal notice](#legal-notice)
- [Features](#features)
- [Supported payloads](#supported-payloads)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Command-line reference](#command-line-reference)
- [Usage examples](#usage-examples)
- [Interactive mode](#interactive-mode)
- [Encoding](#encoding)
- [Listener helpers](#listener-helpers)
- [Demo](#demo)
- [Architecture](#architecture)
- [Extending ShellForge](#extending-shellforge)
- [Testing](#testing)
- [Roadmap](#roadmap)
- [License](#license)

---

## Overview

ShellForge is a command-line payload generator for red team engagements, penetration
tests, CTFs, and lab exercises. It produces the standard, well-documented reverse,
bind, and web shell templates you would otherwise copy by hand from references such as
revshells.com, PayloadsAllTheThings, and HackTricks — parameterised with your own IP
and port, and ready to paste, save, or compile.

The goal is speed and consistency during an engagement: one command, one clean payload,
without leaving the terminal. Payloads are printed as plain, copy-safe text (no wrapping
boxes or decoration), so a single mouse-select copies exactly what you need and nothing
else.

**Motivation.** During CTFs and lab pentests, generating the same shells with a different
`LHOST`/`LPORT` each time is repetitive and error-prone. ShellForge centralises those
templates behind a small, scriptable CLI with an optional guided menu.

## Legal notice

> ### Authorized use only
>
> ShellForge is intended **solely** for authorized security testing, red team
> engagements, CTF competitions, lab environments, and personal learning.
>
> - Only run payloads against systems you **own** or have **explicit written permission**
>   to test.
> - Web shells require write access to a target web root and are for authorized testing
>   only.
> - Unauthorized access to computer systems is illegal in most jurisdictions.
>
> You are solely responsible for how you use this tool. The author accepts no liability
> for misuse or damage.

## Features

- **Three payload families** — reverse shells, bind shells, and web shells from one CLI.
- **16 reverse/bind languages and tools** and **11 web shell languages** (see below).
- **Reference-grade templates** — clean `{IP}` / `{PORT}` substitution, no obfuscation.
- **Copy-safe output** — payloads print as plain text with no borders or styling.
- **File output** — save `.ps1`, `.c`, `.java`, `.cs`, `.go`, and web shell files directly.
- **Encoders** — Base64, URL-encoding, and PowerShell `-EncodedCommand` (UTF-16LE).
- **Listener helpers** — generates matching `nc`, `rlwrap`, `socat`, and Metasploit
  `multi/handler` commands.
- **Interactive menu** — guided prompts with input validation for IP, port, and options.
- **Modular design** — add a language by dropping a file in `generators/` and registering it.
- **Tested** — pytest suite covering every generator, encoder, and CLI path.

## Supported payloads

### Reverse & bind shells

| Language / tool | Key(s) | Reverse | Bind | File output |
|-----------------|--------|:-------:|:----:|:-----------:|
| Bash            | `bash` | ✅ | ✅ | — |
| Python 2 / 3    | `python`, `python3` | ✅ | ✅ | — |
| Perl            | `perl` | ✅ | ✅ | — |
| PHP             | `php` | ✅ | ✅ | — |
| Ruby            | `ruby` | ✅ | ✅ | — |
| Netcat          | `nc`, `nc-mkfifo` | ✅ | ✅ | — |
| socat           | `socat` | ✅ | ✅ | — |
| PowerShell      | `powershell` | ✅ | ✅ | `.ps1` |
| Java            | `java` | ✅ | ✅ | `.java` |
| C#              | `csharp` | ✅ | ✅ | `.cs` |
| C               | `c` | ✅ | ✅ | `.c` |
| Go              | `golang` | ✅ | ✅ | `.go` |
| Lua             | `lua` | ✅ | ✅ | — |
| AWK             | `awk` | ✅ | ✅ | — |

Use `-l all` to emit every reverse/bind language at once.

### Web shells

| Language | Key | Extension | Variants |
|----------|-----|-----------|----------|
| PHP | `php` | `.php` | minimal, full |
| PHP 5 | `php5` | `.php5` | minimal, full |
| ASP (classic) | `asp` | `.asp` | minimal, full |
| ASP.NET | `aspx` | `.aspx` | minimal, full |
| JSP | `jsp` | `.jsp` | minimal, full |
| JSPX | `jspx` | `.jspx` | minimal, full |
| Perl CGI | `perl` | `.pl` | minimal, full |
| Python CGI | `python` | `.py` | minimal, full |
| Ruby CGI | `ruby` | `.rb` | minimal, full |
| ColdFusion | `cfm` | `.cfm` | minimal, full |
| Node.js | `nodejs` | `.js` | minimal, full |

- **minimal** — the smallest functional one-liner, ideal for a quick upload.
- **full** — a browser-interactive version with a command form, output pane, and basic
  error handling.

## Installation

**Requirements:** Python 3.9 or newer.

```bash
git clone https://github.com/<your-user>/shellforge.git
cd shellforge
pip install -r requirements.txt
```

> On Windows, use `py` instead of `python` if `python` resolves to the Microsoft Store stub.

Optional editable install (exposes a `shellforge` entry point):

```bash
pip install -e .
```

## Quick start

```bash
# Guided interactive menu
python shellforge.py

# Bash reverse shell
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l bash

# PHP web shell (browser form) saved to a file
python shellforge.py -t webshell -l php --variant full -o shell.php
```

## Command-line reference

```
python shellforge.py [-t TYPE] [-i IP] [-p PORT] [-l LANG] [--variant VARIANT]
                     [--encode ENCODING] [-o OUTPUT] [--listener] [-m]
                     [--list-langs] [--no-banner] [--version]
```

| Option | Argument | Description |
|--------|----------|-------------|
| `-t`, `--type` | `reverse` \| `bind` \| `webshell` | Payload family to generate. |
| `-i`, `--ip` | IP address | Attacker/callback host. Required for `reverse`. |
| `-p`, `--port` | port | Listening/callback port. Required for `reverse`/`bind`. |
| `-l`, `--lang` | language key \| `all` | Target language/tool. See [supported payloads](#supported-payloads). |
| `--variant` | `minimal` \| `full` | Web shell variant. Default: `minimal`. |
| `--encode` | `none` \| `base64` \| `urlencode` \| `ps-encoded` | Encoding applied to the payload. Default: `none`. |
| `-o`, `--output` | path | Write the payload to a file (recommended for web shells and compiled languages). |
| `--listener` | — | Also print matching listener commands. |
| `-m`, `--interactive` | — | Launch the guided interactive menu. |
| `--list-langs` | — | List supported languages (web shell languages when combined with `-t webshell`). |
| `--no-banner` | — | Suppress the banner and disclaimer. |
| `--version` | — | Print version and exit. |

Running with **no arguments** is equivalent to `--interactive`.

## Usage examples

**Reverse shell (bash):**

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l bash
```

**Bind shell (Python 3):**

```bash
python shellforge.py -t bind -p 5555 -l python3
```

**PowerShell reverse shell saved as a script:**

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 443 -l powershell -o reverse.ps1
```

**Compile-ready C reverse shell:**

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l c -o reverse.c
# gcc -o reverse reverse.c && ./reverse
```

**Every language at once:**

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l all
```

**Web shells:**

```bash
python shellforge.py -t webshell -l php  --variant full    -o shell.php
python shellforge.py -t webshell -l aspx --variant minimal -o shell.aspx
python shellforge.py -t webshell --list-langs
```

More end-to-end walkthroughs: [`examples/usage_examples.md`](examples/usage_examples.md).

## Interactive mode

Run `python shellforge.py` (or `-m`) for a prompted workflow. It validates input and
re-prompts on invalid values rather than crashing.

```
[?] Select shell type:
  [1] Reverse shell
  [2] Bind shell
  [3] Web shell
```

- **Reverse / bind** — prompts for language, IP (reverse only), port, encoding, optional
  listener output, and optional file save.
- **Web shell** — prompts for language, variant (minimal/full), and output path; no
  IP/port needed.

After each payload the menu offers to generate another or exit.

## Encoding

Apply an encoding to any generated payload with `--encode`:

| Encoding | Description | Typical use |
|----------|-------------|-------------|
| `none` | Raw payload (default). | Direct paste. |
| `base64` | Base64 of the UTF-8 payload. | Wrapping in a decode-and-run stub. |
| `urlencode` | Percent-encoding. | Delivery via URL parameters. |
| `ps-encoded` | UTF-16LE + Base64, wrapped as `powershell -EncodedCommand`. | Windows one-liners. |

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l bash --encode base64
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l powershell --encode ps-encoded
```

## Listener helpers

Add `--listener` to print catch commands alongside the payload:

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l bash --listener
```

Generates `nc -lvnp`, `rlwrap nc -lvnp`, a full-TTY `socat` listener, and a Metasploit
`multi/handler` one-liner for the chosen port.

## Demo

Tested end-to-end on a lab setup: Kali (attacker) and a Windows target VM — generating a
PowerShell reverse shell through the interactive menu and catching it with netcat.

**Interactive mode — selecting shell type and options**

![Interactive menu](docs/screenshots/01-interactive-menu.png)

**Generated PowerShell reverse shell payload with listener commands**

![Payload and listener output](docs/screenshots/02-payload-output.png)

**Payload pasted into a live PowerShell session on the target**

![Payload executed on target](docs/screenshots/03-payload-executed.png)

**Shell caught — running `whoami /priv` on the target through the reverse connection**

![Reverse shell session](docs/screenshots/04-shell-session.png)

## Architecture

```
shellforge/
├── shellforge.py              # CLI entrypoint, argument parsing, dispatch
├── interactive.py             # Guided menu mode
├── generators/                # One module per language/tool
│   ├── base.py                # PayloadGenerator abstract base class
│   ├── bash_sh.py, python_lang.py, ... 
│   └── webshell.py            # Web shell generators (minimal / full)
├── encoders/
│   └── encode.py              # Base64 / URL / PowerShell encoders
├── listeners/
│   └── listener_helper.py     # nc / rlwrap / socat / msfconsole helpers
├── assets/logo.svg
├── docs/screenshots/          # Demo screenshots
├── examples/usage_examples.md
└── tests/                     # pytest suite
```

Reverse/bind generators implement a common `PayloadGenerator` interface
(`reverse()`, `bind()`, `file_extension()`); file-capable languages add
`reverse_script()` / `bind_script()`. Web shell generators expose `minimal()` and
`full()`. The CLI resolves a language key to a generator via the `LANGUAGES` and
`WEBSHELL_LANGUAGES` registries.

## Extending ShellForge

Add a new reverse/bind language in two steps:

1. Create `generators/mylang.py` implementing the `PayloadGenerator` interface:

```python
from generators.base import PayloadGenerator

class MyLangGenerator(PayloadGenerator):
    def reverse(self, ip: str, port: int) -> str:
        return f"..."  # payload with {ip}:{port}

    def bind(self, port: int) -> str:
        return f"..."

    def file_extension(self) -> str:
        return ".ext"
```

2. Register it in the `LANGUAGES` dict in `shellforge.py`:

```python
LANGUAGES = {
    # ...
    "mylang": MyLangGenerator(),
}
```

Web shell languages follow the same pattern in `generators/webshell.py`.

## Testing

```bash
pip install pytest
pytest -q
```

The suite verifies that every generator produces non-empty output with the correct
`IP`/`PORT` substitution, that encoders round-trip correctly, that web shells contain a
valid command-execution primitive, and that both CLI and interactive entry points behave
as expected.

## Roadmap

- Windows `cmd` / `mshta` / `certutil` delivery one-liners alongside the PowerShell generator.
- Optional TTY-upgrade cheat sheet printed after a Linux reverse shell (`python pty`, `stty raw`, …).
- A `--format raw|commented` flag to emit either a bare payload or a payload with a short compile/run header.

## License

Released under the [MIT License](LICENSE).

---

<p align="center"><strong>ShellForge</strong> · Author: Mostafa Tamime</p>
