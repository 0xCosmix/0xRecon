# 0xRecon GUI v2.0
> Advanced OSINT Framework — by [0xCosmix](https://github.com/0xCosmix)

```
  ██████╗ ██╗  ██╗██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
 ██╔═████╗╚██╗██╔╝██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
 ██║██╔██║ ╚███╔╝ ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
 ████╔╝██║ ██╔██╗ ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
 ╚██████╔╝██╔╝ ██╗██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
```

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-41CD52?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-557C94?style=for-the-badge)
[![License: GPL v3](https://shields.io)](https://gnu.org)
![Status](https://img.shields.io/badge/Status-Active-00ff88?style=for-the-badge)

---

## 🔍 What is 0xRecon?

**0xRecon** is an advanced OSINT (Open Source Intelligence) framework with a professional dark-themed GUI. Built for ethical security researchers, it aggregates passive reconnaissance data from multiple public sources into a single interface.

> ⚠️ **Legal use only** — Only use on systems you own or have explicit written permission to test. All modules perform **passive analysis** only.

---

## ✨ Features

| Module | Description |
|--------|-------------|
| 🌐 **DNS Lookup** | A, AAAA, MX, NS, TXT, CNAME records |
| 📍 **IP & Geolocation** | IP resolution, country, city, ISP, ASN |
| 📋 **WHOIS** | Registrar, dates, nameservers, emails |
| 🔒 **SSL Certificate** | Subject, issuer, validity, SANs |
| 📡 **HTTP Headers** | Status, security headers, missing protections |
| 🔌 **Port Scan** | 20 common ports with service detection |
| 🌿 **Subdomain Discovery** | Passive enumeration of common subdomains |
| 🛠️ **Tech Detection** | WordPress, React, Nginx, Cloudflare, PHP... |
| 💥 **Breach Check** | HaveIBeenPwned domain breach lookup |
| 🤖 **Robots & Sitemap** | robots.txt and sitemap.xml analysis |
| 🕸️ **Graph View** | Interactive visual map of all findings |
| 📄 **PDF Export** | Professional report generation |
| 📦 **JSON Export** | Raw data export for further analysis |

---

## 🖥️ Screenshots

> *Terminal tab with live scan output*

> *Graph view showing domain connections*

> *Results tree with all findings*

---

## 🚀 Installation

### 🐧 Linux (Kali / Ubuntu / Debian)

```bash
# Clone the repo
git clone https://github.com/0xCosmix/security-research.git
cd security-research/tools/0xrecon

# Run install script
chmod +x install_linux.sh
./install_linux.sh

# Launch
python3 0xrecon_gui.py
```

### 🪟 Windows

```batch
# Clone or download the repo
# Double-click install_windows.bat
# OR run in cmd:

install_windows.bat

# Then launch:
python 0xrecon_gui.py
```

### 📦 Manual install (both platforms)

```bash
pip install PyQt6 requests dnspython python-whois reportlab networkx
python3 0xrecon_gui.py
```

---

## 📖 Usage

1. Enter a **domain** or **IP** in the target field
2. Select the **modules** you want to run
3. Click **▶ SCAN**
4. View results in **Terminal**, **Results**, **Graph** or **JSON** tabs
5. Export as **PDF** or **JSON** for your report

---

## 🗂️ Project Structure

```
0xrecon/
├── 0xrecon_gui.py        ← Main GUI application
├── 0xrecon.py            ← Terminal version (v1)
├── install_linux.sh      ← Linux installer
├── install_windows.bat   ← Windows installer
├── requirements.txt      ← Python dependencies
└── README.md
```

---

## ⚖️ Legal Disclaimer

This tool is designed for **educational purposes** and **authorized security testing only**.

- ✅ Use on your own systems
- ✅ Use on systems you have written permission to test
- ✅ Use on CTF platforms (TryHackMe, HTB, etc.)
- ✅ Use for OSINT on public domain information
- ❌ Do NOT use on systems without authorization
- ❌ Do NOT use for illegal activities

The author is not responsible for any misuse of this tool.

---

## 👤 Author

**0xCosmix** — Aspiring Penetration Tester

[![GitHub](https://img.shields.io/badge/GitHub-0xCosmix-181717?style=flat-square&logo=github)](https://github.com/0xCosmix)
[![TryHackMe](https://img.shields.io/badge/TryHackMe-0xCosmix-red?style=flat-square&logo=tryhackme)](https://tryhackme.com/p/0xCosmix)

---

*"Only test what you own. Learn everything else."*
