# ESP32-C3

- CPU: single-core RISC-V (RV32IMC), up to 160 MHz. 400 KB SRAM.
- Radio: Wi-Fi 4 (2.4 GHz), BLE 5.
- No PSRAM support.
- Native USB-Serial-JTAG on **GPIO18 (D−) / GPIO19 (D+)**. Console/flash/JTAG
  only; not USB-OTG.
- Toolchain prefix: `riscv32-esp-elf-`.

## Pins to avoid or treat with care
- **GPIO12–17:** SPI flash. Taken on all variants with in-package flash (C3FH4 etc.).
- **Strapping pins: GPIO2, 8, 9.**
  - GPIO9 low at reset → download mode (it is usually the BOOT button).
  - GPIO8 must be high for download mode to work.
  - GPIO2 should be high at reset.
- GPIO20/21: UART0 RX/TX (console).

## Peripheral notes
- Use ADC1 (GPIO0–4). ADC2 (GPIO5) is not usable for reliable readings;
  treat it as unavailable.
- Single core: anything that busy-waits starves Wi-Fi and the idle task.
  Expect task watchdog resets.
- Only 22 GPIOs; plan the pin map early.
