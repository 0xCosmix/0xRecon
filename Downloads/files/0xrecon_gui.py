#!/usr/bin/env python3
"""
0xRecon GUI — Advanced OSINT Framework
by 0xCosmix
Version 2.0 | Cross-platform | PyQt6
"""

import sys
import os
import socket
import ssl
import json
import re
import time
import threading
import subprocess
from datetime import datetime

# ── PyQt6 ────────────────────────────────────────────────────────────────────
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLineEdit, QPushButton, QTextEdit, QLabel, QFrame,
    QProgressBar, QSplitter, QScrollArea, QGridLayout, QGroupBox,
    QCheckBox, QComboBox, QFileDialog, QStatusBar, QTreeWidget,
    QTreeWidgetItem, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem,
    QGraphicsLineItem, QGraphicsTextItem, QMessageBox
)
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QTimer, QPointF, QRectF, QObject
)
from PyQt6.QtGui import (
    QFont, QColor, QPalette, QTextCursor, QLinearGradient,
    QPainter, QPen, QBrush, QPixmap, QIcon, QFontDatabase
)

# ── Other libs ────────────────────────────────────────────────────────────────
try:
    import requests
    import dns.resolver
    import whois
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

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
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

# ═══════════════════════════════════════════════════════════════════════════════
# THEME
# ═══════════════════════════════════════════════════════════════════════════════

DARK_THEME = """
QMainWindow, QWidget {
    background-color: #050a0e;
    color: #c8d8e4;
    font-family: 'Consolas', 'Courier New', monospace;
}

QTabWidget::pane {
    border: 1px solid #0f2535;
    background: #050a0e;
}

QTabBar::tab {
    background: #0a1520;
    color: #4a6478;
    padding: 8px 20px;
    border: 1px solid #0f2535;
    border-bottom: none;
    font-family: 'Consolas', monospace;
    font-size: 11px;
    letter-spacing: 2px;
}

QTabBar::tab:selected {
    background: #050a0e;
    color: #00ff88;
    border-top: 2px solid #00ff88;
}

QTabBar::tab:hover {
    color: #00ccff;
}

QLineEdit {
    background: #020608;
    border: 1px solid #0f2535;
    border-radius: 2px;
    padding: 8px 12px;
    color: #00ff88;
    font-family: 'Consolas', monospace;
    font-size: 13px;
    selection-background-color: #00ff88;
    selection-color: #000;
}

QLineEdit:focus {
    border: 1px solid #00ff88;
}

QPushButton {
    background: #0a1520;
    border: 1px solid #0f2535;
    border-radius: 2px;
    padding: 8px 20px;
    color: #c8d8e4;
    font-family: 'Consolas', monospace;
    font-size: 11px;
    letter-spacing: 2px;
}

QPushButton:hover {
    border: 1px solid #00ff88;
    color: #00ff88;
    background: #0a1f14;
}

QPushButton:pressed {
    background: #001a0a;
}

QPushButton#btnScan {
    background: #00ff88;
    color: #000;
    border: none;
    font-weight: bold;
    font-size: 12px;
    padding: 10px 30px;
}

QPushButton#btnScan:hover {
    background: #00cc6e;
}

QPushButton#btnDanger {
    background: #1a0505;
    border: 1px solid #ff4444;
    color: #ff4444;
}

QPushButton#btnDanger:hover {
    background: #ff4444;
    color: #fff;
}

QPushButton#btnBlue {
    background: #050a1a;
    border: 1px solid #00ccff;
    color: #00ccff;
}

QPushButton#btnBlue:hover {
    background: #00ccff;
    color: #000;
}

QTextEdit {
    background: #020608;
    border: 1px solid #0f2535;
    border-radius: 2px;
    color: #c8d8e4;
    font-family: 'Consolas', monospace;
    font-size: 12px;
    padding: 8px;
}

QProgressBar {
    background: #0a1520;
    border: 1px solid #0f2535;
    border-radius: 2px;
    height: 4px;
    text-align: center;
    color: transparent;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #00ff88, stop:1 #00ccff);
    border-radius: 2px;
}

QTreeWidget {
    background: #020608;
    border: 1px solid #0f2535;
    color: #c8d8e4;
    font-family: 'Consolas', monospace;
    font-size: 12px;
}

QTreeWidget::item:selected {
    background: #0a1520;
    color: #00ff88;
}

QTreeWidget::item:hover {
    background: #0a1520;
}

QHeaderView::section {
    background: #0a1520;
    border: 1px solid #0f2535;
    padding: 5px;
    color: #00ccff;
    font-family: 'Consolas', monospace;
    font-size: 11px;
    letter-spacing: 1px;
}

QScrollBar:vertical {
    background: #050a0e;
    width: 8px;
}

QScrollBar::handle:vertical {
    background: #0f2535;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #00ff88;
}

QScrollBar:horizontal {
    background: #050a0e;
    height: 8px;
}

QScrollBar::handle:horizontal {
    background: #0f2535;
    border-radius: 4px;
}

QGroupBox {
    border: 1px solid #0f2535;
    border-radius: 2px;
    margin-top: 12px;
    padding-top: 8px;
    font-family: 'Consolas', monospace;
    font-size: 10px;
    color: #4a6478;
    letter-spacing: 2px;
}

QGroupBox::title {
    color: #00ff88;
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

QCheckBox {
    color: #4a6478;
    font-family: 'Consolas', monospace;
    font-size: 11px;
    spacing: 8px;
}

QCheckBox:checked {
    color: #00ff88;
}

QCheckBox::indicator {
    width: 14px;
    height: 14px;
    border: 1px solid #0f2535;
    background: #020608;
}

QCheckBox::indicator:checked {
    background: #00ff88;
    border: 1px solid #00ff88;
}

QComboBox {
    background: #0a1520;
    border: 1px solid #0f2535;
    padding: 5px 10px;
    color: #c8d8e4;
    font-family: 'Consolas', monospace;
}

QComboBox::drop-down {
    border: none;
}

QStatusBar {
    background: #0a1520;
    border-top: 1px solid #0f2535;
    color: #4a6478;
    font-family: 'Consolas', monospace;
    font-size: 10px;
}

QSplitter::handle {
    background: #0f2535;
}

QGraphicsView {
    background: #020608;
    border: 1px solid #0f2535;
}
"""

# ═══════════════════════════════════════════════════════════════════════════════
# WORKER THREAD
# ═══════════════════════════════════════════════════════════════════════════════

class ScanWorker(QThread):
    log = pyqtSignal(str, str)  # message, color
    result = pyqtSignal(str, dict)  # module, data
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, target, modules):
        super().__init__()
        self.target = target
        self.modules = modules
        self.results = {}

    def run(self):
        total = len(self.modules)
        for i, module in enumerate(self.modules):
            self.progress.emit(int((i / total) * 100))
            try:
                fn = getattr(self, f"scan_{module}", None)
                if fn:
                    data = fn()
                    self.results[module] = data
                    self.result.emit(module, data)
            except Exception as e:
                self.log.emit(f"[ERROR] {module}: {e}", "#ff4444")
        self.progress.emit(100)
        self.finished.emit()

    def scan_dns(self):
        self.log.emit("// Running DNS lookup...", "#00ccff")
        records = {}
        for rtype in ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]:
            try:
                answers = dns.resolver.resolve(self.target, rtype, lifetime=5)
                records[rtype] = [str(r) for r in answers]
                self.log.emit(f"  [{rtype}] {', '.join(records[rtype][:2])}", "#00ff88")
            except:
                pass
        return records

    def scan_ip(self):
        self.log.emit("// Resolving IP & Geolocation...", "#00ccff")
        try:
            ip = socket.gethostbyname(self.target)
            self.log.emit(f"  [IP] {ip}", "#00ff88")
            try:
                r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
                data = r.json()
                data["resolved_ip"] = ip
                self.log.emit(f"  [GEO] {data.get('city','?')}, {data.get('country','?')}", "#00ff88")
                return data
            except:
                return {"resolved_ip": ip}
        except Exception as e:
            self.log.emit(f"  [ERR] {e}", "#ff4444")
            return {}

    def scan_whois(self):
        self.log.emit("// Running WHOIS lookup...", "#00ccff")
        try:
            w = whois.whois(self.target)
            result = {
                "registrar": str(w.registrar or "N/A"),
                "creation_date": str(w.creation_date or "N/A"),
                "expiration_date": str(w.expiration_date or "N/A"),
                "name_servers": str(w.name_servers or "N/A"),
                "emails": str(w.emails or "N/A"),
                "country": str(w.country or "N/A"),
            }
            self.log.emit(f"  [WHOIS] Registrar: {result['registrar'][:40]}", "#00ff88")
            return result
        except Exception as e:
            self.log.emit(f"  [ERR] {e}", "#ff4444")
            return {}

    def scan_http(self):
        self.log.emit("// Analyzing HTTP headers...", "#00ccff")
        try:
            r = requests.get(f"https://{self.target}", timeout=8,
                           headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=True)
            headers = dict(r.headers)
            result = {
                "status_code": r.status_code,
                "final_url": str(r.url),
                "headers": headers,
                "content_length": len(r.content),
            }
            self.log.emit(f"  [HTTP] Status {r.status_code} — {len(r.content)} bytes", "#00ff88")

            # Security headers check
            missing = []
            for h in ["x-frame-options", "strict-transport-security",
                      "content-security-policy", "x-content-type-options"]:
                if h not in [k.lower() for k in headers.keys()]:
                    missing.append(h)
            result["missing_security"] = missing
            if missing:
                self.log.emit(f"  [WARN] Missing headers: {', '.join(missing)}", "#ffaa00")
            return result
        except Exception as e:
            self.log.emit(f"  [ERR] {e}", "#ff4444")
            return {}

    def scan_ssl(self):
        self.log.emit("// Checking SSL certificate...", "#00ccff")
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=self.target) as s:
                s.settimeout(5)
                s.connect((self.target, 443))
                cert = s.getpeercert()
            subject = dict(x[0] for x in cert.get("subject", []))
            issuer = dict(x[0] for x in cert.get("issuer", []))
            result = {
                "subject_cn": subject.get("commonName", "N/A"),
                "issuer": issuer.get("organizationName", "N/A"),
                "valid_from": cert.get("notBefore", "N/A"),
                "valid_until": cert.get("notAfter", "N/A"),
                "sans": [s[1] for s in cert.get("subjectAltName", [])[:10]],
            }
            self.log.emit(f"  [SSL] Issued by {result['issuer']}", "#00ff88")
            self.log.emit(f"  [SSL] Valid until {result['valid_until']}", "#00ff88")
            return result
        except Exception as e:
            self.log.emit(f"  [ERR] {e}", "#ff4444")
            return {}

    def scan_ports(self):
        self.log.emit("// Scanning common ports...", "#00ccff")
        common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
            443: "HTTPS", 3306: "MySQL", 3389: "RDP",
            5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt",
            8443: "HTTPS-Alt", 27017: "MongoDB"
        }
        try:
            ip = socket.gethostbyname(self.target)
        except:
            return {}
        open_ports = {}
        for port, service in common_ports.items():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                if s.connect_ex((ip, port)) == 0:
                    open_ports[port] = service
                    self.log.emit(f"  [OPEN] {port}/{service}", "#00ff88")
                s.close()
            except:
                pass
        self.log.emit(f"  [{len(open_ports)} open ports found]", "#00ccff")
        return open_ports

    def scan_subdomains(self):
        self.log.emit("// Discovering subdomains...", "#00ccff")
        common = ["www", "mail", "ftp", "api", "dev", "staging", "test",
                  "admin", "portal", "shop", "cloud", "cdn", "app",
                  "mobile", "static", "assets", "docs", "support", "git",
                  "vpn", "smtp", "ns1", "ns2", "blog", "forum", "wiki"]
        found = {}
        for sub in common:
            target = f"{sub}.{self.target}"
            try:
                ip = socket.gethostbyname(target)
                found[target] = ip
                self.log.emit(f"  [SUB] {target} → {ip}", "#00ff88")
            except:
                pass
        self.log.emit(f"  [{len(found)} subdomains found]", "#00ccff")
        return found

    def scan_tech(self):
        self.log.emit("// Detecting technologies...", "#00ccff")
        signatures = {
            "WordPress": ["wp-content", "wp-includes"],
            "Drupal": ["Drupal", "sites/default"],
            "React": ["react", "__REACT"],
            "Vue.js": ["vue.js", "__vue__"],
            "Angular": ["angular", "ng-version"],
            "jQuery": ["jquery"],
            "Bootstrap": ["bootstrap"],
            "Cloudflare": ["cloudflare", "cf-ray"],
            "Nginx": ["nginx"],
            "Apache": ["apache"],
            "PHP": ["php", "X-Powered-By: PHP"],
            "Next.js": ["__NEXT_DATA__", "_next"],
            "Laravel": ["laravel_session"],
            "Django": ["csrftoken", "django"],
        }
        try:
            r = requests.get(f"https://{self.target}", timeout=8,
                           headers={"User-Agent": "Mozilla/5.0"})
            content = r.text.lower() + str(r.headers).lower()
            found = []
            for tech, sigs in signatures.items():
                if any(s.lower() in content for s in sigs):
                    found.append(tech)
                    self.log.emit(f"  [TECH] {tech} detected", "#00ff88")
            return {"technologies": found}
        except Exception as e:
            self.log.emit(f"  [ERR] {e}", "#ff4444")
            return {}

    def scan_breach(self):
        self.log.emit("// Checking breach databases...", "#00ccff")
        # HaveIBeenPwned domain search (public API)
        try:
            r = requests.get(
                f"https://haveibeenpwned.com/api/v3/breacheddomain/{self.target}",
                headers={"User-Agent": "0xRecon-OSINT-Tool"},
                timeout=10
            )
            if r.status_code == 200:
                breaches = r.json()
                self.log.emit(f"  [BREACH] {len(breaches)} breaches found!", "#ff4444")
                return {"breaches": breaches, "count": len(breaches)}
            elif r.status_code == 404:
                self.log.emit("  [BREACH] No breaches found", "#00ff88")
                return {"breaches": [], "count": 0}
        except Exception as e:
            self.log.emit(f"  [ERR] Breach check: {e}", "#ff4444")
        return {}

    def scan_robots(self):
        self.log.emit("// Checking robots.txt & sitemap...", "#00ccff")
        result = {}
        for path in ["/robots.txt", "/sitemap.xml"]:
            try:
                r = requests.get(f"https://{self.target}{path}", timeout=5,
                               headers={"User-Agent": "Mozilla/5.0"})
                if r.status_code == 200:
                    result[path] = r.text[:2000]
                    self.log.emit(f"  [FOUND] {path}", "#00ff88")
            except:
                pass
        return result

# ═══════════════════════════════════════════════════════════════════════════════
# GRAPH WIDGET
# ═══════════════════════════════════════════════════════════════════════════════

class GraphWidget(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.nodes = {}

    def clear_graph(self):
        self.scene.clear()
        self.nodes = {}

    def add_node(self, label, x, y, color="#00ff88", size=40):
        ellipse = self.scene.addEllipse(
            x - size/2, y - size/2, size, size,
            QPen(QColor(color), 2),
            QBrush(QColor(color).darker(300))
        )
        text = self.scene.addText(label)
        text.setDefaultTextColor(QColor(color))
        text.setFont(QFont("Consolas", 8))
        text.setPos(x - text.boundingRect().width()/2, y + size/2 + 2)
        self.nodes[label] = (x, y)
        return (x, y)

    def add_edge(self, from_label, to_label, color="#0f2535"):
        if from_label in self.nodes and to_label in self.nodes:
            x1, y1 = self.nodes[from_label]
            x2, y2 = self.nodes[to_label]
            line = self.scene.addLine(x1, y1, x2, y2, QPen(QColor(color), 1))

    def build_from_results(self, target, results):
        self.clear_graph()
        cx, cy = 400, 300

        # Center node
        self.add_node(target, cx, cy, "#00ff88", 50)

        angle_step = 360 / max(len(results), 1)
        import math
        radius = 180

        module_colors = {
            "ip": "#00ccff", "dns": "#ffaa00", "whois": "#ff88ff",
            "ssl": "#88ffaa", "ports": "#ff4444", "tech": "#aaffff",
            "subdomains": "#ffff88", "breach": "#ff6644",
        }

        for i, (module, data) in enumerate(results.items()):
            if not data:
                continue
            angle = math.radians(i * angle_step)
            mx = cx + radius * math.cos(angle)
            my = cy + radius * math.sin(angle)
            color = module_colors.get(module, "#4a6478")
            self.add_node(f"[{module}]", mx, my, color, 35)
            self.add_edge(target, f"[{module}]", color)

            # Sub-nodes for important data
            if module == "ip" and "resolved_ip" in data:
                sx = mx + 100 * math.cos(angle)
                sy = my + 100 * math.sin(angle)
                self.add_node(data["resolved_ip"], sx, sy, "#00ccff", 25)
                self.add_edge(f"[{module}]", data["resolved_ip"], "#00ccff")

            if module == "subdomains" and data:
                for j, (sub, ip) in enumerate(list(data.items())[:4]):
                    sa = math.radians(i * angle_step + (j - 2) * 15)
                    sr = radius + 120
                    sx = cx + sr * math.cos(sa)
                    sy = cy + sr * math.sin(sa)
                    self.add_node(sub.split(".")[0], sx, sy, "#ffff88", 20)
                    self.add_edge(f"[{module}]", sub.split(".")[0], "#ffff88")

# ═══════════════════════════════════════════════════════════════════════════════
# LOG WIDGET
# ═══════════════════════════════════════════════════════════════════════════════

class LogWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setFont(QFont("Consolas", 11))

    def append_colored(self, text, color="#c8d8e4"):
        self.moveCursor(QTextCursor.MoveOperation.End)
        self.insertHtml(f'<span style="color:{color}; font-family:Consolas,monospace;">{text}<br></span>')
        self.moveCursor(QTextCursor.MoveOperation.End)

    def append_banner(self, target):
        self.clear()
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.append_colored("=" * 60, "#0f2535")
        self.append_colored(f"  0xRECON v2.0 — OSINT FRAMEWORK", "#00ff88")
        self.append_colored(f"  by 0xCosmix", "#4a6478")
        self.append_colored("=" * 60, "#0f2535")
        self.append_colored(f"  TARGET : {target}", "#00ccff")
        self.append_colored(f"  TIME   : {ts}", "#4a6478")
        self.append_colored("=" * 60, "#0f2535")
        self.append_colored("", "#4a6478")

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
        for module, data in results.items():
            if not data:
                continue
            root = QTreeWidgetItem([f"// {module.upper()}", ""])
            root.setForeground(0, QColor("#00ff88"))
            root.setFont(0, QFont("Consolas", 10, QFont.Weight.Bold))
            self._add_dict(root, data)
            self.addTopLevelItem(root)
            root.setExpanded(True)

    def _add_dict(self, parent, data, depth=0):
        if depth > 3:
            return
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, (dict, list)) and v:
                    child = QTreeWidgetItem([str(k), ""])
                    child.setForeground(0, QColor("#00ccff"))
                    parent.addChild(child)
                    self._add_dict(child, v, depth+1)
                else:
                    child = QTreeWidgetItem([str(k), str(v)[:120]])
                    child.setForeground(0, QColor("#4a6478"))
                    child.setForeground(1, QColor("#c8d8e4"))
                    parent.addChild(child)
        elif isinstance(data, list):
            for item in data[:20]:
                child = QTreeWidgetItem(["", str(item)[:120]])
                child.setForeground(1, QColor("#c8d8e4"))
                parent.addChild(child)
        else:
            child = QTreeWidgetItem(["value", str(data)[:120]])
            child.setForeground(1, QColor("#c8d8e4"))
            parent.addChild(child)

# ═══════════════════════════════════════════════════════════════════════════════
# PDF REPORT GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

def generate_pdf_report(target, results, output_path):
    if not HAS_PDF:
        return False
    try:
        doc = SimpleDocTemplate(output_path, pagesize=A4,
                               leftMargin=2*cm, rightMargin=2*cm,
                               topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=6,
            textColor=colors.HexColor('#00ff88'),
            fontName='Courier-Bold',
            alignment=TA_CENTER
        )
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#4a6478'),
            fontName='Courier',
            alignment=TA_CENTER
        )
        section_style = ParagraphStyle(
            'Section',
            parent=styles['Heading2'],
            fontSize=13,
            textColor=colors.HexColor('#00ccff'),
            fontName='Courier-Bold',
            spaceBefore=15,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#c8d8e4'),
            fontName='Courier',
            spaceAfter=4
        )

        story.append(Paragraph("0xRECON", title_style))
        story.append(Paragraph("OSINT Analysis Report", subtitle_style))
        story.append(Spacer(1, 0.3*cm))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f2535')))
        story.append(Spacer(1, 0.3*cm))

        # Meta table
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        meta_data = [
            ["TARGET", target],
            ["ANALYST", "0xCosmix"],
            ["DATE", ts],
            ["TOOL", "0xRecon v2.0"],
        ]
        meta_table = Table(meta_data, colWidths=[4*cm, 13*cm])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#0a1520')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#00ff88')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#c8d8e4')),
            ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#0f2535')),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#020608')),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 0.5*cm))

        # Results sections
        for module, data in results.items():
            if not data:
                continue
            story.append(Paragraph(f"// {module.upper()}", section_style))
            story.append(HRFlowable(width="100%", thickness=0.5,
                                   color=colors.HexColor('#0f2535')))

            if isinstance(data, dict):
                rows = []
                for k, v in data.items():
                    if isinstance(v, (list, dict)):
                        v = str(v)[:200]
                    rows.append([str(k).upper(), str(v)[:150]])
                if rows:
                    t = Table(rows, colWidths=[5*cm, 12*cm])
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#0a1520')),
                        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#4a6478')),
                        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#c8d8e4')),
                        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
                        ('FONTSIZE', (0, 0), (-1, -1), 8),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#0f2535')),
                        ('PADDING', (0, 0), (-1, -1), 5),
                        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#020608')),
                        ('ROWBACKGROUNDS', (0, 0), (-1, -1),
                         [colors.HexColor('#020608'), colors.HexColor('#050a0e')]),
                    ]))
                    story.append(t)
            story.append(Spacer(1, 0.3*cm))

        # Footer
        story.append(Spacer(1, 0.5*cm))
        story.append(HRFlowable(width="100%", thickness=1,
                               color=colors.HexColor('#0f2535')))
        story.append(Paragraph(
            "Report generated by 0xRecon v2.0 — github.com/0xCosmix/security-research",
            subtitle_style
        ))

        doc.build(story)
        return True
    except Exception as e:
        print(f"PDF error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN WINDOW
# ═══════════════════════════════════════════════════════════════════════════════

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("0xRecon v2.0 — OSINT Framework by 0xCosmix")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        self.results = {}
        self.current_target = ""
        self.worker = None
        self._setup_ui()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = self._build_header()
        main_layout.addWidget(header)

        # Content
        content = QSplitter(Qt.Orientation.Horizontal)

        # Left panel
        left = self._build_left_panel()
        content.addWidget(left)

        # Right panel (tabs)
        right = self._build_right_panel()
        content.addWidget(right)

        content.setSizes([320, 1080])
        main_layout.addWidget(content)

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("// Ready — Enter target and select modules")

        # Progress
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setMaximumWidth(200)
        self.status.addPermanentWidget(self.progress)

    def _build_header(self):
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #050a0e, stop:0.5 #0a1520, stop:1 #050a0e);
                border-bottom: 1px solid #0f2535;
            }
        """)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)

        # Logo
        logo = QLabel("&gt; 0xRECON")
        logo.setStyleSheet("""
            color: #00ff88;
            font-family: 'Consolas', monospace;
            font-size: 22px;
            font-weight: bold;
            letter-spacing: 4px;
        """)
        layout.addWidget(logo)

        subtitle = QLabel("// OSINT FRAMEWORK v2.0")
        subtitle.setStyleSheet("""
            color: #4a6478;
            font-family: 'Consolas', monospace;
            font-size: 11px;
            letter-spacing: 3px;
        """)
        layout.addWidget(subtitle)
        layout.addStretch()

        by = QLabel("by 0xCosmix")
        by.setStyleSheet("""
            color: #4a6478;
            font-family: 'Consolas', monospace;
            font-size: 10px;
            letter-spacing: 2px;
        """)
        layout.addWidget(by)
        return header

    def _build_left_panel(self):
        left = QWidget()
        left.setMaximumWidth(320)
        left.setMinimumWidth(280)
        left.setStyleSheet("background: #0a1520; border-right: 1px solid #0f2535;")
        layout = QVBoxLayout(left)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Target input
        tgt_label = QLabel("// TARGET")
        tgt_label.setStyleSheet("color: #4a6478; font-size: 10px; letter-spacing: 3px;")
        layout.addWidget(tgt_label)

        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("domain.com or IP")
        self.target_input.returnPressed.connect(self.start_scan)
        layout.addWidget(self.target_input)

        # Modules
        modules_group = QGroupBox("MODULES")
        modules_layout = QVBoxLayout(modules_group)
        modules_layout.setSpacing(5)

        self.module_checks = {}
        modules = [
            ("dns", "DNS Lookup", True),
            ("ip", "IP & Geolocation", True),
            ("whois", "WHOIS", True),
            ("http", "HTTP Headers", True),
            ("ssl", "SSL Certificate", True),
            ("ports", "Port Scan", True),
            ("subdomains", "Subdomain Discovery", True),
            ("tech", "Tech Detection", True),
            ("breach", "Breach Check", False),
            ("robots", "Robots & Sitemap", True),
        ]

        for key, label, default in modules:
            cb = QCheckBox(label)
            cb.setChecked(default)
            self.module_checks[key] = cb
            modules_layout.addWidget(cb)

        layout.addWidget(modules_group)

        # Select all / none
        sel_layout = QHBoxLayout()
        btn_all = QPushButton("ALL")
        btn_all.setFixedHeight(28)
        btn_all.clicked.connect(lambda: [cb.setChecked(True) for cb in self.module_checks.values()])
        btn_none = QPushButton("NONE")
        btn_none.setFixedHeight(28)
        btn_none.clicked.connect(lambda: [cb.setChecked(False) for cb in self.module_checks.values()])
        sel_layout.addWidget(btn_all)
        sel_layout.addWidget(btn_none)
        layout.addLayout(sel_layout)

        # Scan button
        self.btn_scan = QPushButton("▶  SCAN")
        self.btn_scan.setObjectName("btnScan")
        self.btn_scan.setFixedHeight(45)
        self.btn_scan.clicked.connect(self.start_scan)
        layout.addWidget(self.btn_scan)

        # Export buttons
        export_label = QLabel("// EXPORT")
        export_label.setStyleSheet("color: #4a6478; font-size: 10px; letter-spacing: 3px; margin-top: 10px;")
        layout.addWidget(export_label)

        btn_pdf = QPushButton("⬇  EXPORT PDF")
        btn_pdf.setObjectName("btnBlue")
        btn_pdf.setFixedHeight(35)
        btn_pdf.clicked.connect(self.export_pdf)
        layout.addWidget(btn_pdf)

        btn_json = QPushButton("⬇  EXPORT JSON")
        btn_json.setFixedHeight(35)
        btn_json.clicked.connect(self.export_json)
        layout.addWidget(btn_json)

        btn_clear = QPushButton("✕  CLEAR")
        btn_clear.setObjectName("btnDanger")
        btn_clear.setFixedHeight(35)
        btn_clear.clicked.connect(self.clear_all)
        layout.addWidget(btn_clear)

        layout.addStretch()

        # Info
        info = QLabel("⚠ Solo analisi passiva\nSolo su sistemi autorizzati\n100% legale")
        info.setStyleSheet("""
            color: #4a6478;
            font-family: 'Consolas', monospace;
            font-size: 9px;
            border: 1px solid #0f2535;
            padding: 8px;
            border-radius: 2px;
        """)
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)

        return left

    def _build_right_panel(self):
        self.tabs = QTabWidget()

        # Tab 1 — Terminal Log
        self.log_widget = LogWidget()
        self.log_widget.append_colored("  0xRECON v2.0 — Ready", "#00ff88")
        self.log_widget.append_colored("  Enter target and press SCAN", "#4a6478")
        self.tabs.addTab(self.log_widget, "TERMINAL")

        # Tab 2 — Results Tree
        self.results_tree = ResultsTree()
        self.tabs.addTab(self.results_tree, "RESULTS")

        # Tab 3 — Graph
        self.graph_widget = GraphWidget()
        self.tabs.addTab(self.graph_widget, "GRAPH")

        # Tab 4 — Raw JSON
        self.json_widget = QTextEdit()
        self.json_widget.setReadOnly(True)
        self.json_widget.setFont(QFont("Consolas", 10))
        self.json_widget.setPlaceholderText("// Raw JSON results appear here after scan")
        self.tabs.addTab(self.json_widget, "JSON")

        return self.tabs

    # ── SCAN ────────────────────────────────────────────────────────────────

    def start_scan(self):
        target = self.target_input.text().strip()
        target = target.replace("https://", "").replace("http://", "").strip("/")
        if not target:
            self.status.showMessage("// Error: Enter a target domain or IP")
            return

        self.current_target = target
        self.results = {}

        selected = [k for k, cb in self.module_checks.items() if cb.isChecked()]
        if not selected:
            self.status.showMessage("// Error: Select at least one module")
            return

        self.log_widget.append_banner(target)
        self.btn_scan.setEnabled(False)
        self.btn_scan.setText("// SCANNING...")
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.tabs.setCurrentIndex(0)

        self.worker = ScanWorker(target, selected)
        self.worker.log.connect(self.on_log)
        self.worker.result.connect(self.on_result)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

        self.status.showMessage(f"// Scanning {target} — {len(selected)} modules active...")

    def on_log(self, text, color):
        self.log_widget.append_colored(text, color)

    def on_result(self, module, data):
        self.results[module] = data

    def on_finished(self):
        self.btn_scan.setEnabled(True)
        self.btn_scan.setText("▶  SCAN")
        self.progress.setVisible(False)

        self.log_widget.append_colored("", "#4a6478")
        self.log_widget.append_colored("=" * 60, "#0f2535")
        self.log_widget.append_colored(f"  SCAN COMPLETE — {len(self.results)} modules", "#00ff88")
        self.log_widget.append_colored("=" * 60, "#0f2535")

        self.results_tree.populate(self.results)
        self.graph_widget.build_from_results(self.current_target, self.results)
        self.json_widget.setPlainText(json.dumps(self.results, indent=2, default=str))

        self.status.showMessage(f"// Scan complete — {len(self.results)} modules — Target: {self.current_target}")

    # ── EXPORT ──────────────────────────────────────────────────────────────

    def export_pdf(self):
        if not self.results:
            QMessageBox.warning(self, "0xRecon", "No results to export. Run a scan first.")
            return
        if not HAS_PDF:
            QMessageBox.warning(self, "0xRecon", "reportlab not installed.\nRun: pip install reportlab")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export PDF Report", f"0xrecon_{self.current_target}_{datetime.now().strftime('%Y%m%d')}.pdf",
            "PDF Files (*.pdf)"
        )
        if path:
            if generate_pdf_report(self.current_target, self.results, path):
                QMessageBox.information(self, "0xRecon", f"PDF exported:\n{path}")
                self.status.showMessage(f"// PDF exported: {path}")
            else:
                QMessageBox.warning(self, "0xRecon", "PDF export failed.")

    def export_json(self):
        if not self.results:
            QMessageBox.warning(self, "0xRecon", "No results to export. Run a scan first.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export JSON", f"0xrecon_{self.current_target}_{datetime.now().strftime('%Y%m%d')}.json",
            "JSON Files (*.json)"
        )
        if path:
            with open(path, "w") as f:
                json.dump(self.results, f, indent=2, default=str)
            QMessageBox.information(self, "0xRecon", f"JSON exported:\n{path}")
            self.status.showMessage(f"// JSON exported: {path}")

    def clear_all(self):
        self.results = {}
        self.current_target = ""
        self.log_widget.clear()
        self.results_tree.clear()
        self.graph_widget.clear_graph()
        self.json_widget.clear()
        self.target_input.clear()
        self.log_widget.append_colored("  0xRECON v2.0 — Ready", "#00ff88")
        self.log_widget.append_colored("  Enter target and press SCAN", "#4a6478")
        self.status.showMessage("// Cleared — Ready for new scan")

# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#050a0e"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#c8d8e4"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#020608"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#0a1520"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#c8d8e4"))
    palette.setColor(QPalette.ColorRole.Button, QColor("#0a1520"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#c8d8e4"))
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#00ff88"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#000000"))
    app.setPalette(palette)
    app.setStyleSheet(DARK_THEME)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
