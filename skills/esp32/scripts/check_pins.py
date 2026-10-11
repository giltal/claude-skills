#!/usr/bin/env python3
"""Flag risky GPIO choices for ESP32-family targets.

Usage:
  check_pins.py <target> <gpio> [<gpio> ...]
  check_pins.py esp32s3 0 19 20 35 --octal-psram

Exit code 1 if any ERROR is found, else 0.
"""
import argparse
import sys

# Pin data per target. Reasons are short; details live in chips/*.md.
T = {
    "esp32": {
        "valid": set(range(0, 40)) - {20, 24, 28, 29, 30, 31},
        "error": {**{p: "connected to SPI flash" for p in range(6, 12)}},
        "warn": {
            0: "strapping (download mode)",
            2: "strapping (must be low/floating for download)",
            5: "strapping (SDIO timing)",
            12: "strapping: high at reset selects 1.8 V flash -> boot failure",
            15: "strapping (boot log / SDIO timing)",
            16: "used by PSRAM on WROVER modules",
            17: "used by PSRAM on WROVER modules",
            1: "UART0 TX (console)",
            3: "UART0 RX (console)",
            **{p: "input only, no internal pull-up/down" for p in range(34, 40)},
        },
        "adc2_wifi": {0, 2, 4, 12, 13, 14, 15, 25, 26, 27},
    },
    "esp32s3": {
        "valid": set(range(0, 49)) - {22, 23, 24, 25},
        "error": {**{p: "SPI flash / quad PSRAM" for p in range(26, 33)}},
        "warn": {
            0: "strapping (download mode)",
            3: "strapping (JTAG source)",
            45: "strapping: high selects 1.8 V VDD_SPI",
            46: "strapping (boot mode / ROM log)",
            19: "native USB D-",
            20: "native USB D+",
            39: "default JTAG MTCK", 40: "default JTAG MTDO",
            41: "default JTAG MTDI", 42: "default JTAG MTMS",
            43: "UART0 TX (console)", 44: "UART0 RX (console)",
        },
        "octal": {p: "octal flash/PSRAM" for p in range(33, 38)},
        "adc2_wifi": set(range(11, 21)),
    },
    "esp32c3": {
        "valid": set(range(0, 22)),
        "error": {**{p: "SPI flash" for p in range(12, 18)}},
        "warn": {
            2: "strapping (should be high at reset)",
            8: "strapping (must be high for download mode)",
            9: "strapping (BOOT button, low = download)",
            18: "USB-Serial-JTAG D-",
            19: "USB-Serial-JTAG D+",
            20: "UART0 RX (console)", 21: "UART0 TX (console)",
            5: "ADC2: unreliable, treat as no ADC",
        },
    },
    "esp32c6": {
        "valid": set(range(0, 31)),
        "error": {**{p: "SPI flash" for p in range(24, 31)}},
        "warn": {
            4: "strapping (SDIO edge)", 5: "strapping (SDIO edge)",
            8: "strapping (must be high for download mode)",
            9: "strapping (BOOT button, low = download)",
            15: "strapping (JTAG source)",
            12: "USB-Serial-JTAG D-", 13: "USB-Serial-JTAG D+",
            16: "UART0 TX (console)", 17: "UART0 RX (console)",
        },
    },
    "esp32p4": {
        "valid": set(range(0, 55)),
        "error": {},
        "warn": {p: "strapping (verify against datasheet)" for p in range(34, 39)},
        "note": "P4 data is partial: also check the board schematic for flash/PSRAM "
                "pins, IO voltage domains and the C6 SDIO link.",
    },
}

ALIASES = {"esp32-s3": "esp32s3", "esp32-c3": "esp32c3",
           "esp32-c6": "esp32c6", "esp32-p4": "esp32p4"}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target")
    ap.add_argument("gpios", nargs="+", type=int)
    ap.add_argument("--octal-psram", action="store_true",
                    help="S3 module with octal flash or PSRAM (e.g. N16R8)")
    ap.add_argument("--wifi", action="store_true",
                    help="Wi-Fi is used (flags ADC2 pins)")
    a = ap.parse_args()

    tgt = ALIASES.get(a.target.lower(), a.target.lower())
    if tgt not in T:
        sys.exit(f"Unknown target '{a.target}'. Known: {', '.join(T)}")
    d = T[tgt]
    errors = 0
    seen = set()

    for g in a.gpios:
        if g in seen:
            print(f"GPIO{g}: ERROR assigned more than once")
            errors += 1
            continue
        seen.add(g)
        if g not in d["valid"]:
            print(f"GPIO{g}: ERROR does not exist on {tgt}")
            errors += 1
        elif g in d["error"]:
            print(f"GPIO{g}: ERROR {d['error'][g]}")
            errors += 1
        elif a.octal_psram and g in d.get("octal", {}):
            print(f"GPIO{g}: ERROR {d['octal'][g]}")
            errors += 1
        else:
            msgs = []
            if g in d["warn"]:
                msgs.append(d["warn"][g])
            if g in d.get("octal", {}) and not a.octal_psram:
                msgs.append("taken on octal flash/PSRAM modules; confirm module part number")
            if a.wifi and g in d.get("adc2_wifi", set()):
                msgs.append("ADC2 channel: unusable for ADC while Wi-Fi is on")
            print(f"GPIO{g}: " + ("WARN " + "; ".join(msgs) if msgs else "OK"))

    if "note" in d:
        print(f"NOTE: {d['note']}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
