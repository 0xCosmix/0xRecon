#!/usr/bin/env python3
"""
0xRecon GUI v3.0 — Advanced OSINT Framework
by 0xCosmix
Full edition: all modules, phishing tab, sessions, themes, Word/PDF export
"""

import sys, os, socket, ssl, json, re, time, threading, math, hashlib
from datetime import datetime
from pathlib import Path

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    import dns.resolver
    HAS_DNS = True
except ImportError:
    HAS_DNS = False

try:
    import whois
    HAS_WHOIS = True
except ImportError:
    HAS_WHOIS = False

try:
    import networkx as nx
    HAS_NX = True
except ImportError:
    HAS_NX = False

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.enums import TA_CENTER
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

try:
    from docx import Document
    from docx.shared import Pt, RGBColor, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

# Sessions folder
SESSIONS_DIR = Path.home() / ".0xrecon" / "sessions"
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

# Sherlock username list (top sites)
SHERLOCK_SITES = {
    "GitHub": "https://github.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "TryHackMe": "https://tryhackme.com/p/{}",
    "HackTheBox": "https://app.hackthebox.com/users/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Twitch": "https://www.twitch.tv/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "Telegram": "https://t.me/{}",
    "Medium": "https://medium.com/@{}",
    "Dev.to": "https://dev.to/{}",
    "Gitlab": "https://gitlab.com/{}",
    "Keybase": "https://keybase.io/{}",
    "Pastebin": "https://pastebin.com/u/{}",
    "HackerNews": "https://news.ycombinator.com/user?id={}",
    "ProductHunt": "https://www.producthunt.com/@{}",
    "Fiverr": "https://www.fiverr.com/{}",
    "Gravatar": "https://en.gravatar.com/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "Codecademy": "https://www.codecademy.com/profiles/{}",
    "HackerOne": "https://hackerone.com/{}",
    "Bugcrowd": "https://bugcrowd.com/{}",
    "DockerHub": "https://hub.docker.com/u/{}",
    "NPM": "https://www.npmjs.com/~{}",
    "PyPI": "https://pypi.org/user/{}",
}

# ═══════════════════════════════════════════════════════════════════════════════
# THEMES
# ═══════════════════════════════════════════════════════════════════════════════

THEMES = {
    "dark": {
        "bg": "#050a0e",
        "surface": "#0a1520",
        "border": "#0f2535",
        "accent": "#00ff88",
        "accent2": "#00ccff",
        "danger": "#ff4444",
        "text": "#c8d8e4",
        "muted": "#4a6478",
        "terminal_bg": "#020608",
    },
    "light": {
        "bg": "#f0f4f8",
        "surface": "#ffffff",
        "border": "#d0dce8",
        "accent": "#008844",
        "accent2": "#0066cc",
        "danger": "#cc2222",
        "text": "#1a2a3a",
        "muted": "#8a9aaa",
        "terminal_bg": "#e8eef4",
    },
    "matrix": {
        "bg": "#000000",
        "surface": "#001400",
        "border": "#003300",
        "accent": "#00ff00",
        "accent2": "#00cc00",
        "danger": "#ff0000",
        "text": "#00dd00",
        "muted": "#006600",
        "terminal_bg": "#000800",
    },
}

def build_stylesheet(theme):
    t = THEMES[theme]
    return f"""
QMainWindow, QWidget {{
    background-color: {t['bg']};
    color: {t['text']};
    font-family: 'Consolas', 'Courier New', monospace;
}}
QTabWidget::pane {{
    border: 1px solid {t['border']};
    background: {t['bg']};
}}
QTabBar::tab {{
    background: {t['surface']};
    color: {t['muted']};
    padding: 8px 18px;
    border: 1px solid {t['border']};
    border-bottom: none;
    font-family: 'Consolas', monospace;
    font-size: 11px;
    letter-spacing: 2px;
}}
QTabBar::tab:selected {{
    background: {t['bg']};
    color: {t['accent']};
    border-top: 2px solid {t['accent']};
}}
QTabBar::tab:hover {{ color: {t['accent2']}; }}
QLineEdit {{
    background: {t['terminal_bg']};
    border: 1px solid {t['border']};
    border-radius: 2px;
    padding: 8px 12px;
    color: {t['accent']};
    font-family: 'Consolas', monospace;
    font-size: 13px;
}}
QLineEdit:focus {{ border: 1px solid {t['accent']}; }}
QPushButton {{
    background: {t['surface']};
    border: 1px solid {t['border']};
    border-radius: 2px;
    padding: 8px 18px;
    color: {t['text']};
    font-family: 'Consolas', monospace;
    font-size: 11px;
    letter-spacing: 2px;
}}
QPushButton:hover {{
    border: 1px solid {t['accent']};
    color: {t['accent']};
}}
QPushButton#btnScan {{
    background: {t['accent']};
    color: #000;
    border: none;
    font-weight: bold;
    font-size: 12px;
    padding: 10px 28px;
}}
QPushButton#btnScan:hover {{ background: {t['accent2']}; }}
QPushButton#btnDanger {{
    background: {t['terminal_bg']};
    border: 1px solid {t['danger']};
    color: {t['danger']};
}}
QPushButton#btnDanger:hover {{ background: {t['danger']}; color: #fff; }}
QPushButton#btnBlue {{
    background: {t['terminal_bg']};
    border: 1px solid {t['accent2']};
    color: {t['accent2']};
}}
QPushButton#btnBlue:hover {{ background: {t['accent2']}; color: #000; }}
QTextEdit {{
    background: {t['terminal_bg']};
    border: 1px solid {t['border']};
    border-radius: 2px;
    color: {t['text']};
    font-family: 'Consolas', monospace;
    font-size: 12px;
    padding: 8px;
}}
QProgressBar {{
    background: {t['surface']};
    border: 1px solid {t['border']};
    border-radius: 2px;
    height: 4px;
    color: transparent;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 {t['accent']}, stop:1 {t['accent2']});
    border-radius: 2px;
}}
QTreeWidget {{
    background: {t['terminal_bg']};
    border: 1px solid {t['border']};
    color: {t['text']};
    font-family: 'Consolas', monospace;
    font-size: 12px;
    alternate-background-color: {t['surface']};
}}
QTreeWidget::item:selected {{ background: {t['surface']}; color: {t['accent']}; }}
QHeaderView::section {{
    background: {t['surface']};
    border: 1px solid {t['border']};
    padding: 5px;
    color: {t['accent2']};
    font-family: 'Consolas', monospace;
    font-size: 11px;
    letter-spacing: 1px;
}}
QScrollBar:vertical {{
    background: {t['bg']};
    width: 8px;
}}
QScrollBar::handle:vertical {{
    background: {t['border']};
    border-radius: 4px;
    min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{ background: {t['accent']}; }}
QScrollBar:horizontal {{
    background: {t['bg']};
    height: 8px;
}}
QScrollBar::handle:horizontal {{
    background: {t['border']};
    border-radius: 4px;
}}
QGroupBox {{
    border: 1px solid {t['border']};
    border-radius: 2px;
    margin-top: 12px;
    padding-top: 8px;
    font-family: 'Consolas', monospace;
    font-size: 10px;
    color: {t['muted']};
    letter-spacing: 2px;
}}
QGroupBox::title {{
    color: {t['accent']};
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}}
QCheckBox {{
    color: {t['muted']};
    font-family: 'Consolas', monospace;
    font-size: 11px;
    spacing: 8px;
}}
QCheckBox:checked {{ color: {t['accent']}; }}
QCheckBox::indicator {{
    width: 14px; height: 14px;
    border: 1px solid {t['border']};
    background: {t['terminal_bg']};
}}
QCheckBox::indicator:checked {{
    background: {t['accent']};
    border: 1px solid {t['accent']};
}}
QComboBox {{
    background: {t['surface']};
    border: 1px solid {t['border']};
    padding: 5px 10px;
    color: {t['text']};
    font-family: 'Consolas', monospace;
}}
QStatusBar {{
    background: {t['surface']};
    border-top: 1px solid {t['border']};
    color: {t['muted']};
    font-family: 'Consolas', monospace;
    font-size: 10px;
}}
QSplitter::handle {{ background: {t['border']}; }}
QGraphicsView {{
    background: {t['terminal_bg']};
    border: 1px solid {t['border']};
}}
QListWidget {{
    background: {t['terminal_bg']};
    border: 1px solid {t['border']};
    color: {t['text']};
    font-family: 'Consolas', monospace;
    font-size: 11px;
}}
QListWidget::item:selected {{ background: {t['surface']}; color: {t['accent']}; }}
QTableWidget {{
    background: {t['terminal_bg']};
    border: 1px solid {t['border']};
    color: {t['text']};
    font-family: 'Consolas', monospace;
    font-size: 11px;
    gridline-color: {t['border']};
}}
QTableWidget::item:selected {{ background: {t['surface']}; color: {t['accent']}; }}
"""

# ═══════════════════════════════════════════════════════════════════════════════
# WORKER — DOMAIN SCAN
# ═══════════════════════════════════════════════════════════════════════════════

class ScanWorker(QThread):
    log    = pyqtSignal(str, str)
    result = pyqtSignal(str, dict)
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, target, modules):
        super().__init__()
        self.target  = target
        self.modules = modules
        self.results = {}

    def run(self):
        total = len(self.modules)
        for i, mod in enumerate(self.modules):
            self.progress.emit(int(i / total * 100))
            fn = getattr(self, f"scan_{mod}", None)
            if fn:
                try:
                    data = fn()
                    self.results[mod] = data
                    self.result.emit(mod, data)
                except Exception as e:
                    self.log.emit(f"[ERR] {mod}: {e}", "#ff4444")
        self.progress.emit(100)
        self.finished.emit()

    def scan_dns(self):
        self.log.emit("// DNS Lookup...", "#00ccff")
        out = {}
        for rtype in ["A","AAAA","MX","NS","TXT","CNAME","SOA"]:
            try:
                ans = dns.resolver.resolve(self.target, rtype, lifetime=5)
                out[rtype] = [str(r) for r in ans]
                self.log.emit(f"  [{rtype}] {out[rtype][0][:60]}", "#00ff88")
            except: pass
        return out

    def scan_ip(self):
        self.log.emit("// IP & Geolocation...", "#00ccff")
        try:
            ip = socket.gethostbyname(self.target)
            self.log.emit(f"  [IP] {ip}", "#00ff88")
            r  = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
            r["resolved_ip"] = ip
            self.log.emit(f"  [GEO] {r.get('city','?')}, {r.get('country','?')} — ISP: {r.get('isp','?')}", "#00ff88")
            return r
        except Exception as e:
            self.log.emit(f"  [ERR] {e}", "#ff4444")
            return {}

    def scan_whois(self):
        self.log.emit("// WHOIS...", "#00ccff")
        try:
            w = whois.whois(self.target)
            out = {
                "registrar":        str(w.registrar or "N/A"),
                "creation_date":    str(w.creation_date or "N/A"),
                "expiration_date":  str(w.expiration_date or "N/A"),
                "updated_date":     str(w.updated_date or "N/A"),
                "name_servers":     str(w.name_servers or "N/A"),
                "emails":           str(w.emails or "N/A"),
                "country":          str(w.country or "N/A"),
                "org":              str(w.org or "N/A"),
            }
            self.log.emit(f"  [WHOIS] {out['registrar'][:50]}", "#00ff88")
            return out
        except Exception as e:
            self.log.emit(f"  [ERR] {e}", "#ff4444")
            return {}

    def scan_http(self):
        self.log.emit("// HTTP Headers...", "#00ccff")
        for scheme in ["https","http"]:
            try:
                r = requests.get(f"{scheme}://{self.target}", timeout=8,
                                 headers={"User-Agent":"Mozilla/5.0"},
                                 allow_redirects=True)
                hdrs = dict(r.headers)
                missing = [h for h in ["x-frame-options","strict-transport-security",
                                        "content-security-policy","x-content-type-options"]
                           if h not in [k.lower() for k in hdrs]]
                self.log.emit(f"  [HTTP] {r.status_code} {scheme.upper()} — {len(r.content)} bytes", "#00ff88")
                if missing:
                    self.log.emit(f"  [WARN] Missing security headers: {', '.join(missing)}", "#ffaa00")
                return {"status_code": r.status_code, "final_url": str(r.url),
                        "headers": hdrs, "missing_security": missing,
                        "content_length": len(r.content)}
            except: continue
        return {}

    def scan_ssl(self):
        self.log.emit("// SSL Certificate...", "#00ccff")
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=self.target) as s:
                s.settimeout(5)
                s.connect((self.target, 443))
                cert = s.getpeercert()
            subj   = dict(x[0] for x in cert.get("subject",[]))
            issuer = dict(x[0] for x in cert.get("issuer",[]))
            out = {
                "subject_cn":  subj.get("commonName","N/A"),
                "issuer":      issuer.get("organizationName","N/A"),
                "valid_from":  cert.get("notBefore","N/A"),
                "valid_until": cert.get("notAfter","N/A"),
                "sans":        [s[1] for s in cert.get("subjectAltName",[])[:15]],
            }
            self.log.emit(f"  [SSL] {out['issuer']} — valid until {out['valid_until']}", "#00ff88")
            return out
        except Exception as e:
            self.log.emit(f"  [ERR] {e}", "#ff4444")
            return {}

    def scan_ports(self):
        self.log.emit("// Port Scan...", "#00ccff")
        PORTS = {21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",
                 80:"HTTP",110:"POP3",143:"IMAP",443:"HTTPS",
                 465:"SMTPS",587:"SMTP-TLS",993:"IMAPS",995:"POP3S",
                 3306:"MySQL",3389:"RDP",5432:"PostgreSQL",
                 6379:"Redis",8080:"HTTP-Alt",8443:"HTTPS-Alt",27017:"MongoDB"}
        try:
            ip = socket.gethostbyname(self.target)
        except: return {}
        open_ports = {}
        for port, svc in PORTS.items():
            try:
                s = socket.socket(); s.settimeout(1)
                if s.connect_ex((ip, port)) == 0:
                    open_ports[port] = svc
                    self.log.emit(f"  [OPEN] {port}/{svc}", "#00ff88")
                s.close()
            except: pass
        self.log.emit(f"  [{len(open_ports)} open ports]", "#00ccff")
        return open_ports

    def scan_subdomains(self):
        self.log.emit("// Subdomain Discovery...", "#00ccff")
        subs = ["www","mail","ftp","api","dev","staging","test","admin","portal",
                "shop","cloud","cdn","app","mobile","static","assets","docs",
                "support","git","vpn","smtp","ns1","ns2","blog","forum",
                "wiki","status","remote","webmail","secure","mx","pop"]
        found = {}
        for sub in subs:
            try:
                ip = socket.gethostbyname(f"{sub}.{self.target}")
                found[f"{sub}.{self.target}"] = ip
                self.log.emit(f"  [SUB] {sub}.{self.target} → {ip}", "#00ff88")
            except: pass
        self.log.emit(f"  [{len(found)} subdomains found]", "#00ccff")
        return found

    def scan_tech(self):
        self.log.emit("// Tech Detection...", "#00ccff")
        sigs = {
            "WordPress":  ["wp-content","wp-includes"],
            "Drupal":     ["Drupal","sites/default"],
            "Joomla":     ["Joomla","/components/com_"],
            "React":      ["react","__REACT","_react"],
            "Vue.js":     ["vue.js","__vue__","vuejs"],
            "Angular":    ["angular","ng-version"],
            "Next.js":    ["__NEXT_DATA__","_next"],
            "jQuery":     ["jquery"],
            "Bootstrap":  ["bootstrap"],
            "Cloudflare": ["cloudflare","cf-ray","__cfduid"],
            "Nginx":      ["nginx"],
            "Apache":     ["apache"],
            "PHP":        ["php","x-powered-by: php"],
            "ASP.NET":    ["asp.net","x-aspnet"],
            "Laravel":    ["laravel_session"],
            "Django":     ["csrftoken","django"],
            "Shopify":    ["shopify","myshopify"],
            "Wix":        ["wix.com","_wix_"],
            "Squarespace":["squarespace"],
        }
        try:
            r = requests.get(f"https://{self.target}", timeout=8,
                            headers={"User-Agent":"Mozilla/5.0"})
            content = r.text.lower() + str(r.headers).lower()
            found = [t for t,s in sigs.items() if any(x.lower() in content for x in s)]
            for t in found:
                self.log.emit(f"  [TECH] {t}", "#00ff88")
            return {"technologies": found}
        except Exception as e:
            self.log.emit(f"  [ERR] {e}", "#ff4444")
            return {}

    def scan_breach(self):
        self.log.emit("// Breach Check (HaveIBeenPwned)...", "#00ccff")
        try:
            r = requests.get(
                f"https://haveibeenpwned.com/api/v3/breacheddomain/{self.target}",
                headers={"User-Agent":"0xRecon-OSINT"},
                timeout=10
            )
            if r.status_code == 200:
                breaches = r.json()
                self.log.emit(f"  [BREACH] {len(breaches)} breaches found!", "#ff4444")
                return {"count": len(breaches), "breaches": breaches}
            else:
                self.log.emit("  [BREACH] No breaches found", "#00ff88")
                return {"count": 0, "breaches": []}
        except Exception as e:
            self.log.emit(f"  [ERR] {e}", "#ff4444")
            return {}

    def scan_wayback(self):
        self.log.emit("// Wayback Machine...", "#00ccff")
        try:
            r = requests.get(
                f"http://archive.org/wayback/available?url={self.target}",
                timeout=10
            )
            data = r.json()
            snap = data.get("archived_snapshots", {}).get("closest", {})
            if snap:
                self.log.emit(f"  [WB] Available: {snap.get('timestamp','?')}", "#00ff88")
                return {"available": True, "timestamp": snap.get("timestamp"),
                        "url": snap.get("url"), "status": snap.get("status")}
            else:
                self.log.emit("  [WB] No snapshots found", "#ffaa00")
                return {"available": False}
        except Exception as e:
            self.log.emit(f"  [ERR] {e}", "#ff4444")
            return {}

    def scan_virustotal(self):
        self.log.emit("// VirusTotal (public)...", "#00ccff")
        try:
            r = requests.get(
                f"https://www.virustotal.com/vtapi/v2/url/report",
                params={"apikey": "demo", "resource": self.target},
                timeout=10
            )
            if r.status_code == 200:
                data = r.json()
                pos = data.get("positives", 0)
                total = data.get("total", 0)
                if pos > 0:
                    self.log.emit(f"  [VT] ⚠ {pos}/{total} engines flagged!", "#ff4444")
                else:
                    self.log.emit(f"  [VT] Clean (0/{total})", "#00ff88")
                return data
            else:
                self.log.emit("  [VT] API unavailable (no key)", "#ffaa00")
                return {"note": "Add VirusTotal API key for full results"}
        except Exception as e:
            self.log.emit(f"  [ERR] {e}", "#ff4444")
            return {}

    def scan_robots(self):
        self.log.emit("// Robots & Sitemap...", "#00ccff")
        out = {}
        for path in ["/robots.txt", "/sitemap.xml", "/sitemap_index.xml"]:
            try:
                r = requests.get(f"https://{self.target}{path}", timeout=5,
                                headers={"User-Agent":"Mozilla/5.0"})
                if r.status_code == 200:
                    out[path] = r.text[:3000]
                    self.log.emit(f"  [FOUND] {path}", "#00ff88")
            except: pass
        return out

# ═══════════════════════════════════════════════════════════════════════════════
# WORKER — SHERLOCK
# ═══════════════════════════════════════════════════════════════════════════════

class SherlockWorker(QThread):
    found    = pyqtSignal(str, str)  # site, url
    notfound = pyqtSignal(str)
    progress = pyqtSignal(int)
    finished = pyqtSignal(dict)

    def __init__(self, username):
        super().__init__()
        self.username = username
        self.results  = {}

    def run(self):
        sites  = list(SHERLOCK_SITES.items())
        total  = len(sites)
        for i, (site, url_tmpl) in enumerate(sites):
            self.progress.emit(int(i / total * 100))
            url = url_tmpl.format(self.username)
            try:
                r = requests.get(url, timeout=6,
                                 headers={"User-Agent":"Mozilla/5.0"},
                                 allow_redirects=True)
                if r.status_code == 200 and self.username.lower() in r.text.lower():
                    self.results[site] = url
                    self.found.emit(site, url)
                else:
                    self.notfound.emit(site)
            except:
                self.notfound.emit(site)
        self.progress.emit(100)
        self.finished.emit(self.results)

# ═══════════════════════════════════════════════════════════════════════════════
# GRAPH
# ═══════════════════════════════════════════════════════════════════════════════

class GraphWidget(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.nodes = {}

    def wheelEvent(self, event):
        factor = 1.15 if event.angleDelta().y() > 0 else 0.87
        self.scale(factor, factor)

    def clear_graph(self):
        self.scene.clear()
        self.nodes = {}

    def add_node(self, label, x, y, color="#00ff88", size=40):
        ellipse = self.scene.addEllipse(
            x-size/2, y-size/2, size, size,
            QPen(QColor(color), 2),
            QBrush(QColor(color).darker(400))
        )
        text = self.scene.addText(label[:18])
        text.setDefaultTextColor(QColor(color))
        text.setFont(QFont("Consolas", 7))
        text.setPos(x - text.boundingRect().width()/2, y + size/2 + 2)
        self.nodes[label] = (x, y)

    def add_edge(self, a, b, color="#0f2535"):
        if a in self.nodes and b in self.nodes:
            x1,y1 = self.nodes[a]
            x2,y2 = self.nodes[b]
            self.scene.addLine(x1,y1,x2,y2, QPen(QColor(color),1,Qt.PenStyle.DashLine))

    def build(self, target, results):
        self.clear_graph()
        cx, cy = 500, 350
        self.add_node(target, cx, cy, "#00ff88", 55)
        colors_map = {
            "dns":"#ffaa00","ip":"#00ccff","whois":"#ff88ff",
            "ssl":"#88ffaa","ports":"#ff4444","tech":"#aaffff",
            "subdomains":"#ffff88","breach":"#ff6644",
            "wayback":"#88aaff","virustotal":"#ff8800","robots":"#cccccc",
        }
        n = len([k for k,v in results.items() if v])
        if n == 0: return
        for i, (mod, data) in enumerate([x for x in results.items() if x[1]]):
            angle = math.radians(i * 360 / n)
            r = 200
            mx = cx + r * math.cos(angle)
            my = cy + r * math.sin(angle)
            col = colors_map.get(mod, "#4a6478")
            self.add_node(f"[{mod}]", mx, my, col, 32)
            self.add_edge(target, f"[{mod}]", col)
            # Sub-nodes
            if mod == "ip" and "resolved_ip" in data:
                sx = cx + (r+110)*math.cos(angle)
                sy = cy + (r+110)*math.sin(angle)
                self.add_node(data["resolved_ip"], sx, sy, "#00ccff", 22)
                self.add_edge(f"[{mod}]", data["resolved_ip"], "#00ccff")
            if mod == "subdomains" and data:
                for j,(sub,ip) in enumerate(list(data.items())[:5]):
                    sa = math.radians(i*360/n + (j-2)*12)
                    sr = r + 130
                    sx = cx + sr*math.cos(sa)
                    sy = cy + sr*math.sin(sa)
                    label = sub.split(".")[0]
                    self.add_node(label, sx, sy, "#ffff88", 18)
                    self.add_edge(f"[{mod}]", label, "#ffff88")

# ═══════════════════════════════════════════════════════════════════════════════
# LOG WIDGET
# ═══════════════════════════════════════════════════════════════════════════════

class LogWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setFont(QFont("Consolas", 11))

    def log(self, text, color="#c8d8e4"):
        self.moveCursor(QTextCursor.MoveOperation.End)
        safe = text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        self.insertHtml(f'<span style="color:{color};font-family:Consolas,monospace;">{safe}<br></span>')
        self.moveCursor(QTextCursor.MoveOperation.End)

    def banner(self, target):
        self.clear()
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log("═"*58, "#0f2535")
        self.log("  0xRECON v3.0 — OSINT FRAMEWORK", "#00ff88")
        self.log("  by 0xCosmix", "#4a6478")
        self.log("═"*58, "#0f2535")
        self.log(f"  TARGET : {target}", "#00ccff")
        self.log(f"  TIME   : {ts}", "#4a6478")
        self.log("═"*58, "#0f2535")
        self.log("", "")

# ═══════════════════════════════════════════════════════════════════════════════
# RESULTS TREE
# ═══════════════════════════════════════════════════════════════════════════════

class ResultsTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHeaderLabels(["Field", "Value"])
        self.setColumnWidth(0, 200)
        self.setAlternatingRowColors(True)

    def populate(self, results):
        self.clear()
        for mod, data in results.items():
            if not data: continue
            root = QTreeWidgetItem([f"// {mod.upper()}", ""])
            root.setForeground(0, QColor("#00ff88"))
            root.setFont(0, QFont("Consolas", 10, QFont.Weight.Bold))
            self._fill(root, data)
            self.addTopLevelItem(root)
            root.setExpanded(True)

    def _fill(self, parent, data, depth=0):
        if depth > 3: return
        if isinstance(data, dict):
            for k,v in data.items():
                if isinstance(v, (dict,list)) and v:
                    child = QTreeWidgetItem([str(k), ""])
                    child.setForeground(0, QColor("#00ccff"))
                    parent.addChild(child)
                    self._fill(child, v, depth+1)
                else:
                    child = QTreeWidgetItem([str(k), str(v)[:120]])
                    child.setForeground(0, QColor("#4a6478"))
                    child.setForeground(1, QColor("#c8d8e4"))
                    parent.addChild(child)
        elif isinstance(data, list):
            for item in data[:30]:
                child = QTreeWidgetItem(["", str(item)[:120]])
                child.setForeground(1, QColor("#c8d8e4"))
                parent.addChild(child)

# ═══════════════════════════════════════════════════════════════════════════════
# PDF EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

def export_pdf(target, results, path, analyst="0xCosmix"):
    if not HAS_PDF: return False
    try:
        doc = SimpleDocTemplate(path, pagesize=A4,
                               leftMargin=2*cm, rightMargin=2*cm,
                               topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        s_title = ParagraphStyle('T', parent=styles['Title'], fontSize=22,
                                 textColor=colors.HexColor('#00ff88'),
                                 fontName='Courier-Bold', alignment=TA_CENTER)
        s_sub   = ParagraphStyle('S', parent=styles['Normal'], fontSize=9,
                                 textColor=colors.HexColor('#4a6478'),
                                 fontName='Courier', alignment=TA_CENTER)
        s_sec   = ParagraphStyle('Se', parent=styles['Heading2'], fontSize=12,
                                 textColor=colors.HexColor('#00ccff'),
                                 fontName='Courier-Bold', spaceBefore=12, spaceAfter=4)

        story = []
        story.append(Paragraph("0xRECON v3.0", s_title))
        story.append(Paragraph("OSINT Analysis Report", s_sub))
        story.append(Spacer(1, 0.3*cm))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f2535')))
        story.append(Spacer(1, 0.3*cm))

        meta = [["TARGET", target], ["ANALYST", analyst],
                ["DATE", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                ["TOOL", "0xRecon v3.0 — github.com/0xCosmix"]]
        t = Table(meta, colWidths=[4*cm,13*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(0,-1),colors.HexColor('#0a1520')),
            ('TEXTCOLOR',(0,0),(0,-1),colors.HexColor('#00ff88')),
            ('TEXTCOLOR',(1,0),(1,-1),colors.HexColor('#c8d8e4')),
            ('FONTNAME',(0,0),(-1,-1),'Courier'),
            ('FONTSIZE',(0,0),(-1,-1),9),
            ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#0f2535')),
            ('PADDING',(0,0),(-1,-1),6),
            ('BACKGROUND',(1,0),(1,-1),colors.HexColor('#020608')),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.5*cm))

        for mod, data in results.items():
            if not data: continue
            story.append(Paragraph(f"// {mod.upper()}", s_sec))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#0f2535')))
            if isinstance(data, dict):
                rows = [[str(k).upper(), str(v)[:150]] for k,v in data.items()
                        if not isinstance(v,(dict,list)) or not v]
                if rows:
                    dt = Table(rows, colWidths=[5*cm,12*cm])
                    dt.setStyle(TableStyle([
                        ('BACKGROUND',(0,0),(0,-1),colors.HexColor('#0a1520')),
                        ('TEXTCOLOR',(0,0),(0,-1),colors.HexColor('#4a6478')),
                        ('TEXTCOLOR',(1,0),(1,-1),colors.HexColor('#c8d8e4')),
                        ('FONTNAME',(0,0),(-1,-1),'Courier'),
                        ('FONTSIZE',(0,0),(-1,-1),8),
                        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#0f2535')),
                        ('PADDING',(0,0),(-1,-1),5),
                        ('BACKGROUND',(1,0),(1,-1),colors.HexColor('#020608')),
                        ('ROWBACKGROUNDS',(0,0),(-1,-1),
                         [colors.HexColor('#020608'),colors.HexColor('#050a0e')]),
                    ]))
                    story.append(dt)
            story.append(Spacer(1, 0.3*cm))

        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f2535')))
        story.append(Paragraph("0xRecon v3.0 — github.com/0xCosmix/security-research", s_sub))
        doc.build(story)
        return True
    except Exception as e:
        print(f"PDF error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# WORD EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

def export_word(target, results, path, analyst="0xCosmix"):
    if not HAS_DOCX: return False
    try:
        doc = Document()
        # Title
        title = doc.add_heading("0xRECON v3.0 — OSINT Report", 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_paragraph(f"Target: {target} | Analyst: {analyst} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        doc.add_paragraph("─"*60)
        for mod, data in results.items():
            if not data: continue
            doc.add_heading(f"// {mod.upper()}", level=2)
            if isinstance(data, dict):
                tbl = doc.add_table(rows=1, cols=2)
                tbl.style = 'Table Grid'
                tbl.rows[0].cells[0].text = "FIELD"
                tbl.rows[0].cells[1].text = "VALUE"
                for k,v in data.items():
                    row = tbl.add_row().cells
                    row[0].text = str(k)
                    row[1].text = str(v)[:200]
            doc.add_paragraph("")
        doc.add_paragraph("─"*60)
        doc.add_paragraph("Generated by 0xRecon v3.0 — github.com/0xCosmix/security-research")
        doc.save(path)
        return True
    except Exception as e:
        print(f"Word error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# PHISHING TAB
# ═══════════════════════════════════════════════════════════════════════════════

class PhishingTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15,15,15,15)

        # Header
        hdr = QLabel("// PHISHING ANALYSIS REPORTS")
        hdr.setStyleSheet("color:#ff4444; font-size:13px; letter-spacing:3px; font-family:Consolas;")
        layout.addWidget(hdr)

        # Toolbar
        bar = QHBoxLayout()
        self.btn_add = QPushButton("+ NEW REPORT")
        self.btn_add.setObjectName("btnDanger")
        self.btn_add.clicked.connect(self.add_report)
        bar.addWidget(self.btn_add)

        self.btn_export = QPushButton("⬇ EXPORT MD")
        self.btn_export.setObjectName("btnBlue")
        self.btn_export.clicked.connect(self.export_md)
        bar.addWidget(self.btn_export)
        bar.addStretch()
        layout.addLayout(bar)

        # Report list
        self.report_list = QListWidget()
        self.report_list.setMaximumHeight(160)
        self.report_list.itemClicked.connect(self.load_report)
        layout.addWidget(self.report_list)

        # Form
        form = QGroupBox("REPORT EDITOR")
        form_layout = QGridLayout(form)

        labels = ["Domain", "Date", "Analyst", "Verdict", "Target Victims", "IP/Infrastructure"]
        self.fields = {}
        for i, lbl in enumerate(labels):
            form_layout.addWidget(QLabel(f"// {lbl.upper()}"), i, 0)
            le = QLineEdit()
            le.setPlaceholderText(lbl)
            self.fields[lbl] = le
            form_layout.addWidget(le, i, 1)

        layout.addWidget(form)

        # Summary
        layout.addWidget(QLabel("// TECHNICAL SUMMARY"))
        self.summary = QTextEdit()
        self.summary.setPlaceholderText("Describe the phishing campaign, techniques, IOCs...")
        self.summary.setMaximumHeight(120)
        layout.addWidget(self.summary)

        # IOCs
        layout.addWidget(QLabel("// IOCs (one per line)"))
        self.iocs = QTextEdit()
        self.iocs.setPlaceholderText("104.21.1.240\nvelspin.cc\nhttps://...")
        self.iocs.setMaximumHeight(80)
        layout.addWidget(self.iocs)

        # Tools
        layout.addWidget(QLabel("// TOOLS USED"))
        self.tools_field = QLineEdit()
        self.tools_field.setPlaceholderText("Wireshark, Burp Suite, 0xRecon")
        layout.addWidget(self.tools_field)

        # Save
        self.btn_save = QPushButton("💾  SAVE REPORT")
        self.btn_save.setObjectName("btnScan")
        self.btn_save.clicked.connect(self.save_report)
        layout.addWidget(self.btn_save)

        self.reports = {}
        self.current_id = None
        self.load_all()

    def load_all(self):
        self.reports = {}
        self.report_list.clear()
        for f in SESSIONS_DIR.glob("phishing_*.json"):
            try:
                with open(f) as fp:
                    r = json.load(fp)
                rid = f.stem.replace("phishing_","")
                self.reports[rid] = r
                self.report_list.addItem(f"🔴 {r.get('Domain','?')} — {r.get('Date','?')}")
            except: pass

    def add_report(self):
        self.current_id = None
        for f in self.fields.values(): f.clear()
        self.summary.clear()
        self.iocs.clear()
        self.tools_field.clear()
        self.fields["Date"].setText(datetime.now().strftime("%Y-%m-%d"))
        self.fields["Analyst"].setText("0xCosmix")

    def load_report(self, item):
        idx = self.report_list.row(item)
        rid = list(self.reports.keys())[idx]
        r = self.reports[rid]
        self.current_id = rid
        for lbl, le in self.fields.items():
            le.setText(r.get(lbl,""))
        self.summary.setPlainText(r.get("summary",""))
        self.iocs.setPlainText(r.get("iocs",""))
        self.tools_field.setText(r.get("tools",""))

    def save_report(self):
        domain = self.fields["Domain"].text().strip()
        if not domain:
            QMessageBox.warning(self,"0xRecon","Enter a domain!")
            return
        rid = self.current_id or hashlib.md5(f"{domain}{time.time()}".encode()).hexdigest()[:8]
        r = {lbl: le.text() for lbl,le in self.fields.items()}
        r["summary"] = self.summary.toPlainText()
        r["iocs"]    = self.iocs.toPlainText()
        r["tools"]   = self.tools_field.text()
        r["created"] = datetime.now().isoformat()
        with open(SESSIONS_DIR / f"phishing_{rid}.json", "w") as f:
            json.dump(r, f, indent=2)
        self.current_id = rid
        self.load_all()
        QMessageBox.information(self,"0xRecon","Report saved!")

    def export_md(self):
        idx = self.report_list.currentRow()
        if idx < 0:
            QMessageBox.warning(self,"0xRecon","Select a report first!")
            return
        rid = list(self.reports.keys())[idx]
        r = self.reports[rid]
        domain = r.get("Domain","unknown")
        md = f"""# 🔍 Phishing Analysis — {domain}

| Field | Value |
|-------|-------|
| **Date** | {r.get('Date','')} |
| **Analyst** | {r.get('Analyst','')} |
| **Target** | {domain} |
| **Verdict** | 🔴 {r.get('Verdict','')} |
| **Target Victims** | {r.get('Target Victims','')} |
| **Infrastructure** | {r.get('IP/Infrastructure','')} |

## 📋 Summary
{r.get('summary','')}

## 🎯 IOCs
```
{r.get('iocs','')}
```

## 🛠️ Tools Used
{r.get('tools','')}

---
*Report by {r.get('Analyst','0xCosmix')} — 0xRecon v3.0*
"""
        path, _ = QFileDialog.getSaveFileName(self,"Export",
            f"phishing_{domain.replace('.','_')}.md","Markdown (*.md)")
        if path:
            with open(path,"w") as f: f.write(md)
            QMessageBox.information(self,"0xRecon",f"Exported: {path}")

# ═══════════════════════════════════════════════════════════════════════════════
# SHERLOCK TAB
# ═══════════════════════════════════════════════════════════════════════════════

class SherlockTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15,15,15,15)

        hdr = QLabel("// USERNAME OSINT — SHERLOCK")
        hdr.setStyleSheet("color:#00ccff; font-size:13px; letter-spacing:3px; font-family:Consolas;")
        layout.addWidget(hdr)

        inp = QHBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username to search...")
        self.username_input.returnPressed.connect(self.start_search)
        inp.addWidget(self.username_input)

        self.btn_search = QPushButton("▶ SEARCH")
        self.btn_search.setObjectName("btnScan")
        self.btn_search.clicked.connect(self.start_search)
        inp.addWidget(self.btn_search)
        layout.addLayout(inp)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        # Results table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["STATUS","PLATFORM","URL"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 150)
        layout.addWidget(self.table)

        self.status_lbl = QLabel("")
        self.status_lbl.setStyleSheet("color:#4a6478; font-family:Consolas; font-size:10px;")
        layout.addWidget(self.status_lbl)

        self.found_count = 0
        self.worker = None

    def start_search(self):
        username = self.username_input.text().strip()
        if not username: return
        self.table.setRowCount(0)
        self.found_count = 0
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.btn_search.setEnabled(False)
        self.btn_search.setText("// SEARCHING...")
        self.status_lbl.setText(f"Searching {username} on {len(SHERLOCK_SITES)} platforms...")

        self.worker = SherlockWorker(username)
        self.worker.found.connect(self.on_found)
        self.worker.notfound.connect(self.on_notfound)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def on_found(self, site, url):
        self.found_count += 1
        row = self.table.rowCount()
        self.table.insertRow(row)
        status = QTableWidgetItem("✓ FOUND")
        status.setForeground(QColor("#00ff88"))
        self.table.setItem(row, 0, status)
        self.table.setItem(row, 1, QTableWidgetItem(site))
        url_item = QTableWidgetItem(url)
        url_item.setForeground(QColor("#00ccff"))
        self.table.setItem(row, 2, url_item)

    def on_notfound(self, site):
        pass  # Don't clutter table with not-found

    def on_finished(self, results):
        self.btn_search.setEnabled(True)
        self.btn_search.setText("▶ SEARCH")
        self.progress.setVisible(False)
        self.status_lbl.setText(f"✓ Done — {self.found_count} profiles found on {len(SHERLOCK_SITES)} platforms")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN WINDOW
# ═══════════════════════════════════════════════════════════════════════════════

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("0xRecon v3.0 — OSINT Framework by 0xCosmix")
        self.setMinimumSize(1280, 820)
        self.resize(1500, 950)
        self.results = {}
        self.current_target = ""
        self.current_theme = "dark"
        self.worker = None
        self._build_ui()
        self._apply_theme("dark")

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        ml = QVBoxLayout(central)
        ml.setContentsMargins(0,0,0,0)
        ml.setSpacing(0)

        ml.addWidget(self._header())

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self._left_panel())
        splitter.addWidget(self._right_panel())
        splitter.setSizes([320, 1180])
        ml.addWidget(splitter)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("// Ready — Enter target domain or IP")

        self.prog_bar = QProgressBar()
        self.prog_bar.setVisible(False)
        self.prog_bar.setMaximumWidth(220)
        self.statusbar.addPermanentWidget(self.prog_bar)

    def _header(self):
        hdr = QFrame()
        hdr.setFixedHeight(72)
        hdr.setStyleSheet("""
            QFrame { background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 #050a0e, stop:0.5 #0a1520, stop:1 #050a0e);
                border-bottom: 1px solid #0f2535; }
        """)
        lay = QHBoxLayout(hdr)
        lay.setContentsMargins(20,0,20,0)

        logo = QLabel("&gt; 0xRECON")
        logo.setStyleSheet("color:#00ff88;font-family:Consolas,monospace;font-size:24px;font-weight:bold;letter-spacing:4px;")
        lay.addWidget(logo)

        ver = QLabel("// v3.0 FULL EDITION")
        ver.setStyleSheet("color:#4a6478;font-family:Consolas,monospace;font-size:11px;letter-spacing:3px;")
        lay.addWidget(ver)
        lay.addStretch()

        # Theme toggle
        for name, label in [("dark","◉ DARK"), ("light","◉ LIGHT"), ("matrix","◉ MATRIX")]:
            btn = QPushButton(label)
            btn.setFixedSize(90, 28)
            btn.setStyleSheet("font-size:9px;letter-spacing:1px;")
            btn.clicked.connect(lambda _, n=name: self._apply_theme(n))
            lay.addWidget(btn)

        by = QLabel("  by 0xCosmix  ")
        by.setStyleSheet("color:#4a6478;font-family:Consolas,monospace;font-size:10px;letter-spacing:2px;")
        lay.addWidget(by)
        return hdr

    def _left_panel(self):
        left = QWidget()
        left.setMaximumWidth(320)
        left.setMinimumWidth(280)
        left.setStyleSheet("background:#0a1520; border-right:1px solid #0f2535;")
        lay = QVBoxLayout(left)
        lay.setContentsMargins(14,14,14,14)
        lay.setSpacing(8)

        lbl = QLabel("// TARGET")
        lbl.setStyleSheet("color:#4a6478;font-size:10px;letter-spacing:3px;")
        lay.addWidget(lbl)

        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("domain.com or IP address")
        self.target_input.returnPressed.connect(self.start_scan)
        lay.addWidget(self.target_input)

        # Modules
        mod_group = QGroupBox("MODULES")
        mod_lay = QVBoxLayout(mod_group)
        mod_lay.setSpacing(4)
        self.mod_checks = {}
        modules = [
            ("dns","DNS Lookup",True),
            ("ip","IP & Geolocation",True),
            ("whois","WHOIS",True),
            ("http","HTTP Headers",True),
            ("ssl","SSL Certificate",True),
            ("ports","Port Scan",True),
            ("subdomains","Subdomain Discovery",True),
            ("tech","Tech Detection",True),
            ("breach","Breach Check (HIBP)",False),
            ("wayback","Wayback Machine",True),
            ("virustotal","VirusTotal",False),
            ("robots","Robots & Sitemap",True),
        ]
        for key, label, default in modules:
            cb = QCheckBox(label)
            cb.setChecked(default)
            self.mod_checks[key] = cb
            mod_lay.addWidget(cb)
        lay.addWidget(mod_group)

        sel = QHBoxLayout()
        for label, val in [("ALL",True),("NONE",False)]:
            b = QPushButton(label)
            b.setFixedHeight(26)
            b.clicked.connect(lambda _,v=val: [cb.setChecked(v) for cb in self.mod_checks.values()])
            sel.addWidget(b)
        lay.addLayout(sel)

        self.btn_scan = QPushButton("▶  SCAN")
        self.btn_scan.setObjectName("btnScan")
        self.btn_scan.setFixedHeight(44)
        self.btn_scan.clicked.connect(self.start_scan)
        lay.addWidget(self.btn_scan)

        # Export
        exp_lbl = QLabel("// EXPORT")
        exp_lbl.setStyleSheet("color:#4a6478;font-size:10px;letter-spacing:3px;margin-top:8px;")
        lay.addWidget(exp_lbl)

        for label, obj, fn in [
            ("⬇ PDF REPORT","btnBlue",self.export_pdf),
            ("⬇ WORD REPORT","btnBlue",self.export_word),
            ("⬇ JSON","","self.export_json"),
            ("💾 SAVE SESSION","","self.save_session"),
            ("📂 LOAD SESSION","","self.load_session"),
        ]:
            b = QPushButton(label)
            if obj: b.setObjectName(obj)
            b.setFixedHeight(32)
            if callable(fn):
                b.clicked.connect(fn)
            else:
                b.clicked.connect(getattr(self, fn.replace("self.","")))
            lay.addWidget(b)

        btn_clear = QPushButton("✕  CLEAR ALL")
        btn_clear.setObjectName("btnDanger")
        btn_clear.setFixedHeight(32)
        btn_clear.clicked.connect(self.clear_all)
        lay.addWidget(btn_clear)

        lay.addStretch()

        info = QLabel("⚠ Passive analysis only\nAuthorized targets only\n100% Legal")
        info.setStyleSheet("color:#4a6478;font-family:Consolas,monospace;font-size:9px;"
                          "border:1px solid #0f2535;padding:8px;border-radius:2px;")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(info)
        return left

    def _right_panel(self):
        self.right_tabs = QTabWidget()

        # Terminal
        self.log_widget = LogWidget()
        self.log_widget.log("  0xRECON v3.0 — Full Edition Ready", "#00ff88")
        self.log_widget.log("  Enter target and press SCAN", "#4a6478")
        self.right_tabs.addTab(self.log_widget, "TERMINAL")

        # Results
        self.results_tree = ResultsTree()
        self.right_tabs.addTab(self.results_tree, "RESULTS")

        # Graph
        self.graph_widget = GraphWidget()
        self.right_tabs.addTab(self.graph_widget, "GRAPH")

        # JSON
        self.json_widget = QTextEdit()
        self.json_widget.setReadOnly(True)
        self.json_widget.setFont(QFont("Consolas",10))
        self.json_widget.setPlaceholderText("// Raw JSON output")
        self.right_tabs.addTab(self.json_widget, "JSON")

        # Sherlock
        self.sherlock_tab = SherlockTab()
        self.right_tabs.addTab(self.sherlock_tab, "SHERLOCK")

        # Phishing
        self.phishing_tab = PhishingTab()
        self.right_tabs.addTab(self.phishing_tab, "PHISHING")

        return self.right_tabs

    def _apply_theme(self, name):
        self.current_theme = name
        QApplication.instance().setStyleSheet(build_stylesheet(name))

    # ── SCAN ────────────────────────────────────────────────────────────────

    def start_scan(self):
        target = self.target_input.text().strip()
        target = re.sub(r'^https?://', '', target).strip("/")
        if not target:
            self.statusbar.showMessage("// Error: Enter a target")
            return
        self.current_target = target
        self.results = {}
        selected = [k for k,cb in self.mod_checks.items() if cb.isChecked()]
        if not selected:
            self.statusbar.showMessage("// Error: Select at least one module")
            return

        self.log_widget.banner(target)
        self.btn_scan.setEnabled(False)
        self.btn_scan.setText("// SCANNING...")
        self.prog_bar.setVisible(True)
        self.prog_bar.setValue(0)
        self.right_tabs.setCurrentIndex(0)

        self.worker = ScanWorker(target, selected)
        self.worker.log.connect(lambda t,c: self.log_widget.log(t,c))
        self.worker.result.connect(self.on_result)
        self.worker.progress.connect(self.prog_bar.setValue)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()
        self.statusbar.showMessage(f"// Scanning {target} — {len(selected)} modules")

    def on_result(self, module, data):
        self.results[module] = data

    def on_finished(self):
        self.btn_scan.setEnabled(True)
        self.btn_scan.setText("▶  SCAN")
        self.prog_bar.setVisible(False)
        self.log_widget.log("", "")
        self.log_widget.log("═"*58, "#0f2535")
        self.log_widget.log(f"  SCAN COMPLETE — {len(self.results)} modules — {self.current_target}", "#00ff88")
        self.log_widget.log("═"*58, "#0f2535")
        self.results_tree.populate(self.results)
        self.graph_widget.build(self.current_target, self.results)
        self.json_widget.setPlainText(json.dumps(self.results, indent=2, default=str))
        self.statusbar.showMessage(f"// Complete — {len(self.results)} modules — {self.current_target}")

    # ── EXPORT ──────────────────────────────────────────────────────────────

    def export_pdf(self):
        if not self.results:
            QMessageBox.warning(self,"0xRecon","Run a scan first!"); return
        path,_ = QFileDialog.getSaveFileName(self,"Export PDF",
            f"0xrecon_{self.current_target}_{datetime.now().strftime('%Y%m%d')}.pdf",
            "PDF (*.pdf)")
        if path:
            ok = export_pdf(self.current_target, self.results, path)
            if ok: QMessageBox.information(self,"0xRecon",f"PDF saved:\n{path}")
            else: QMessageBox.warning(self,"0xRecon","PDF export failed. Install reportlab.")

    def export_word(self):
        if not self.results:
            QMessageBox.warning(self,"0xRecon","Run a scan first!"); return
        path,_ = QFileDialog.getSaveFileName(self,"Export Word",
            f"0xrecon_{self.current_target}_{datetime.now().strftime('%Y%m%d')}.docx",
            "Word (*.docx)")
        if path:
            ok = export_word(self.current_target, self.results, path)
            if ok: QMessageBox.information(self,"0xRecon",f"Word saved:\n{path}")
            else: QMessageBox.warning(self,"0xRecon","Word export failed. Install python-docx.")

    def export_json(self):
        if not self.results:
            QMessageBox.warning(self,"0xRecon","Run a scan first!"); return
        path,_ = QFileDialog.getSaveFileName(self,"Export JSON",
            f"0xrecon_{self.current_target}_{datetime.now().strftime('%Y%m%d')}.json",
            "JSON (*.json)")
        if path:
            with open(path,"w") as f:
                json.dump(self.results, f, indent=2, default=str)
            QMessageBox.information(self,"0xRecon",f"JSON saved:\n{path}")

    def save_session(self):
        if not self.results:
            QMessageBox.warning(self,"0xRecon","Nothing to save!"); return
        session = {
            "target": self.current_target,
            "timestamp": datetime.now().isoformat(),
            "results": self.results
        }
        fname = SESSIONS_DIR / f"session_{self.current_target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(fname,"w") as f:
            json.dump(session, f, indent=2, default=str)
        QMessageBox.information(self,"0xRecon",f"Session saved:\n{fname}")
        self.statusbar.showMessage(f"// Session saved: {fname.name}")

    def load_session(self):
        path,_ = QFileDialog.getOpenFileName(self,"Load Session",
            str(SESSIONS_DIR),"JSON (*.json)")
        if path:
            with open(path) as f:
                session = json.load(f)
            self.current_target = session.get("target","")
            self.results = session.get("results",{})
            self.target_input.setText(self.current_target)
            self.results_tree.populate(self.results)
            self.graph_widget.build(self.current_target, self.results)
            self.json_widget.setPlainText(json.dumps(self.results, indent=2, default=str))
            self.log_widget.log(f"// Session loaded: {self.current_target}", "#00ff88")
            self.statusbar.showMessage(f"// Session loaded: {self.current_target}")

    def clear_all(self):
        self.results = {}
        self.current_target = ""
        self.log_widget.clear()
        self.results_tree.clear()
        self.graph_widget.clear_graph()
        self.json_widget.clear()
        self.target_input.clear()
        self.log_widget.log("  0xRECON v3.0 — Ready", "#00ff88")
        self.log_widget.log("  Enter target and press SCAN", "#4a6478")
        self.statusbar.showMessage("// Cleared — Ready")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    p = QPalette()
    p.setColor(QPalette.ColorRole.Window,          QColor("#050a0e"))
    p.setColor(QPalette.ColorRole.WindowText,      QColor("#c8d8e4"))
    p.setColor(QPalette.ColorRole.Base,            QColor("#020608"))
    p.setColor(QPalette.ColorRole.AlternateBase,   QColor("#0a1520"))
    p.setColor(QPalette.ColorRole.Text,            QColor("#c8d8e4"))
    p.setColor(QPalette.ColorRole.Button,          QColor("#0a1520"))
    p.setColor(QPalette.ColorRole.ButtonText,      QColor("#c8d8e4"))
    p.setColor(QPalette.ColorRole.Highlight,       QColor("#00ff88"))
    p.setColor(QPalette.ColorRole.HighlightedText, QColor("#000000"))
    app.setPalette(p)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
