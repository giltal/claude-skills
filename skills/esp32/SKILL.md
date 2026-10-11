---
name: esp32
description: Use when writing, building, flashing, or debugging firmware for Espressif ESP32-family MCUs (ESP32, ESP32-S3, ESP32-C3, ESP32-C6, ESP32-P4) with ESP-IDF or Arduino-ESP32 — pin assignment, peripherals and drivers, sdkconfig/menuconfig, partition tables, OTA, PSRAM, and crash/backtrace analysis.
---

# ESP32 family firmware

## 0. Local environment
If `local.md` exists in this skill folder, read it first. It has the ESP-IDF
install location, the OS/shell, and how to activate the IDF environment on
this machine.

## 1. Establish the target before anything else
- Read `CONFIG_IDF_TARGET` from `sdkconfig`, or run `scripts/detect_chip.sh [port]`.
- Never assume the classic ESP32. Pins, peripherals, ADC channels and core
  architecture (Xtensa vs RISC-V) differ per chip.
- Read the matching chip file before choosing pins or peripherals:
  - ESP32 → `chips/esp32.md`
  - ESP32-S3 → `chips/esp32-s3.md`
  - ESP32-C3 → `chips/esp32-c3.md`
  - ESP32-C6 → `chips/esp32-c6.md`
  - ESP32-P4 → `chips/esp32-p4.md`
- Check the framework and version: `idf.py --version`, or the Arduino-ESP32
  core version. ESP-IDF 5.x replaced many drivers; see `idf/pitfalls.md`.
- If the project has a `CLAUDE.md` with a board pin map, it overrides generic
  advice here.

## 2. Rules
- Validate every GPIO assignment:
  `python3 scripts/check_pins.py <target> <gpio> [<gpio> ...]`
  Treat ERROR results as blockers; explain WARN results to the user.
- Use the driver API that matches the installed IDF version. Do not mix legacy
  and new drivers for the same peripheral (IDF 5.x aborts at startup).
- Prefer ADC1 channels. ADC2 conflicts with Wi-Fi on chips that have it.
- Mark ISR code and anything it calls `IRAM_ATTR`; keep ISRs minimal and defer
  work to a task via a queue/notification.
- Buffers handed to DMA must come from DMA-capable memory
  (`heap_caps_malloc(n, MALLOC_CAP_DMA)`), not stack or arbitrary PSRAM.
- Build with `idf.py build` after changes. Flash or erase flash only when the
  user asks; `erase-flash` destroys NVS data (Wi-Fi credentials, calibration).

## 3. When something fails
- Crash / Guru Meditation: decode the backtrace against the project ELF
  (`idf/build-flash.md` → "Decoding crashes") before proposing fixes.
- Boot loop or "invalid header": check strapping pins and flash mode/size in
  `sdkconfig` first, then the partition table.
- Watchdog resets: see `idf/pitfalls.md` → "Watchdogs".

## References
- Build, flash, partitions, OTA, size, crash decoding: `idf/build-flash.md`
- Common failure modes and IDF 5.x API changes: `idf/pitfalls.md`
