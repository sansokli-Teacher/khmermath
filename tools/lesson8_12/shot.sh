#!/bin/bash
# usage: shot.sh a b  -> sh/a-b.png
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --window-size=1960,1650 --virtual-time-budget=6000 --screenshot=/private/tmp/claude-501/-Users-koemsreang-PISA-Math-2026-new/d2060f27-1f17-483c-8451-2862a4a88c92/scratchpad/sh/$1-$2.png "http://localhost:8765/_g8_sheet.html#$1-$2" >/dev/null 2>&1
