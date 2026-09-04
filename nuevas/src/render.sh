#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
[ -f piezas.py ] && python3 piezas.py >/dev/null
python3 ensamblar.py
cd ../..
timeout 240 google-chrome --headless=new --disable-gpu --no-sandbox --no-pdf-header-footer \
  --virtual-time-budget=20000 --print-to-pdf="$PWD/actividades-nuevas.pdf" \
  "file://$PWD/actividades-nuevas.html" 2>&1 | tail -1
pdfinfo actividades-nuevas.pdf | grep -E "^Pages|^Page size"
