#!/usr/bin/env bash
# Identify the ESP32-family target.
# 1) From sdkconfig in the current project (no hardware needed).
# 2) Otherwise from a connected board via esptool.
# Usage: detect_chip.sh [serial-port]
set -u

if [ -f sdkconfig ]; then
  t=$(grep -E '^CONFIG_IDF_TARGET=' sdkconfig | cut -d'"' -f2)
  if [ -n "${t:-}" ]; then
    echo "sdkconfig target: $t"
    [ $# -eq 0 ] && exit 0
  fi
fi

port_args=()
[ $# -ge 1 ] && port_args=(--port "$1")

# esptool v5 is `esptool` with dashed commands; v4 is `esptool.py` with underscores.
if command -v esptool >/dev/null 2>&1; then
  out=$(esptool "${port_args[@]}" chip-id 2>&1) || out=$(esptool "${port_args[@]}" chip_id 2>&1)
elif command -v esptool.py >/dev/null 2>&1; then
  out=$(esptool.py "${port_args[@]}" chip_id 2>&1)
else
  echo "esptool not found. Run the ESP-IDF export script or: pip install esptool" >&2
  exit 2
fi

line=$(printf '%s\n' "$out" | grep -iE 'Chip (is|type)' | head -n1)
if [ -n "$line" ]; then
  echo "board: $line"
  printf '%s\n' "$out" | grep -iE 'Features|Crystal|revision' | head -n3
else
  echo "Could not identify chip. esptool output:" >&2
  printf '%s\n' "$out" | tail -n 10 >&2
  exit 1
fi
