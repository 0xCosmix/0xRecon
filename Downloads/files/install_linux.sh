#!/bin/bash
# 0xRecon — Linux Installer
# by 0xCosmix

GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
DIM='\033[2m'
NC='\033[0m'

echo -e "${GREEN}"
echo "  ██████╗ ██╗  ██╗██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗"
echo " ██╔═████╗╚██╗██╔╝██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║"
echo " ██║██╔██║ ╚███╔╝ ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║"
echo " ████╔╝██║ ██╔██╗ ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║"
echo " ╚██████╔╝██╔╝ ██╗██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║"
echo "  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝"
echo -e "${NC}"
echo -e "${CYAN}// OSINT Framework — Linux Installer${NC}"
echo -e "${DIM}// by 0xCosmix${NC}"
echo ""

# Check Python
echo -e "${CYAN}[*] Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[!] Python3 not found. Installing...${NC}"
    sudo apt-get update && sudo apt-get install -y python3 python3-pip
else
    echo -e "${GREEN}[✓] Python3 found: $(python3 --version)${NC}"
fi

# Check pip
echo -e "${CYAN}[*] Checking pip...${NC}"
if ! command -v pip3 &> /dev/null; then
    sudo apt-get install -y python3-pip
fi
echo -e "${GREEN}[✓] pip ready${NC}"

# Install dependencies
echo ""
echo -e "${CYAN}[*] Installing dependencies...${NC}"

PACKAGES=(
    "PyQt6"
    "requests"
    "dnspython"
    "python-whois"
    "reportlab"
    "networkx"
    "pillow"
)

for pkg in "${PACKAGES[@]}"; do
    echo -e "${DIM}  Installing $pkg...${NC}"
    pip3 install "$pkg" --break-system-packages -q 2>/dev/null || pip3 install "$pkg" -q
    echo -e "${GREEN}  [✓] $pkg${NC}"
done

# Make executable
echo ""
echo -e "${CYAN}[*] Setting permissions...${NC}"
chmod +x 0xrecon_gui.py
chmod +x 0xrecon.py 2>/dev/null
echo -e "${GREEN}[✓] Done${NC}"

# Create launcher
echo -e "${CYAN}[*] Creating desktop launcher...${NC}"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cat > /tmp/0xrecon.desktop << EOF
[Desktop Entry]
Name=0xRecon
Comment=OSINT Framework by 0xCosmix
Exec=python3 $SCRIPT_DIR/0xrecon_gui.py
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=Security;Network;
EOF

cp /tmp/0xrecon.desktop ~/Desktop/0xRecon.desktop 2>/dev/null
chmod +x ~/Desktop/0xRecon.desktop 2>/dev/null
echo -e "${GREEN}[✓] Desktop launcher created${NC}"

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}  Installation complete!${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}  Launch with:${NC}"
echo -e "  python3 0xrecon_gui.py"
echo ""
echo -e "${DIM}  Only use on authorized systems.${NC}"
echo ""
