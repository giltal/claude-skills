# ESP32 family skill for Claude Code

A [Claude Code](https://claude.com/claude-code) skill for firmware work on
Espressif ESP32-family MCUs (ESP32, ESP32-S3, ESP32-C3, ESP32-C6, ESP32-P4)
with ESP-IDF or Arduino-ESP32.

It has Claude identify the target chip before touching pins or peripherals,
use the right ESP-IDF 5.x driver APIs, and check GPIO choices against the
chip's flash, PSRAM, strapping and USB pins.

## Contents

| Path | What it is |
|------|------------|
| `SKILL.md` | Entry point: workflow and rules |
| `chips/*.md` | Per-chip notes: reserved and strapping pins, peripheral gotchas |
| `idf/build-flash.md` | Build, flash, partitions, OTA, crash decoding |
| `idf/pitfalls.md` | IDF 5.x driver changes, watchdogs, memory, ISRs |
| `scripts/check_pins.py` | Flags risky GPIO assignments per target |
| `scripts/detect_chip.sh` | Reads the target from `sdkconfig` or a connected board |

## Install

Personal (all projects):

```bash
git clone https://github.com/giltal/claude-skills
cp -r claude-skills/skills/esp32 ~/.claude/skills/
```

On Windows: clone the repo, then copy `skills\esp32` to `%USERPROFILE%\.claude\skills\esp32`

Per project (shared with everyone who clones the repo): copy the folder to
`<project>/.claude/skills/esp32/`.

## Machine-specific settings

Create `local.md` next to `SKILL.md` with your ESP-IDF install path, OS and
shell, and how to activate the IDF environment. The skill reads it first if
it exists. It is git-ignored, so it stays out of the shared repo.

## Pin checker

```bash
python3 scripts/check_pins.py esp32s3 0 19 35 --octal-psram --wifi
```

It prints ERROR for pins that must not be used and WARN for pins that need
care. The exit code is 1 if there is any ERROR.

## Status

The ESP32-P4 notes are partial. Values marked *(verify)* should be checked
against the current datasheet. Corrections and additional chips are welcome.
