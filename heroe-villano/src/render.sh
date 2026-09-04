#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
python3 piezas.py >/dev/null
python3 ensamblar.py
cd ../..
timeout 180 google-chrome --headless=new --disable-gpu --no-sandbox --no-pdf-header-footer \
  --virtual-time-budget=20000 --print-to-pdf="$PWD/actividad-heroe-y-villano.pdf" \
  "file://$PWD/actividad-heroe-y-villano.html" 2>&1 | tail -1
pdfinfo actividad-heroe-y-villano.pdf | grep -E "^Pages|^Page size"
