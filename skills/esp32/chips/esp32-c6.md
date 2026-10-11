# ESP32-C6

- CPU: RISC-V HP core up to 160 MHz, plus an LP RISC-V core (~20 MHz) that
  can run while the HP core sleeps (ULP programming via `ulp` LP-core API).
  512 KB HP SRAM + 16 KB LP SRAM.
- Radio: Wi-Fi 6 (2.4 GHz), BLE 5, IEEE 802.15.4 (Thread / Zigbee).
- Native USB-Serial-JTAG on **GPIO12 (D−) / GPIO13 (D+)**.
- Toolchain prefix: `riscv32-esp-elf-`.
- Often used as the wireless co-processor for the ESP32-P4 (ESP-Hosted over SDIO).

## Pins to avoid or treat with care
- **GPIO24–30:** SPI flash. Taken on variants with in-package flash.
- **Strapping pins: GPIO4, 5, 8, 9, 15.**
  - GPIO9 low at reset → download mode (BOOT button).
  - GPIO8 must be high for download mode.
  - GPIO4/5 select SDIO sampling/driving edge; GPIO15 selects JTAG source.
- GPIO0–7 are in the LP domain (usable by the LP core and for deep-sleep wakeup).
- GPIO16/17: UART0 TX/RX (console).

## Peripheral notes
- Only ADC1 exists (GPIO0–6).
- Wi-Fi and 802.15.4 share the 2.4 GHz radio; coexistence must be enabled for
  Thread/Zigbee + Wi-Fi gateways.
