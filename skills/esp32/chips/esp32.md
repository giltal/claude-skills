# ESP32 (classic)

- CPU: dual-core Xtensa LX6, up to 240 MHz. 520 KB SRAM.
- Radio: Wi-Fi 4 (2.4 GHz), Bluetooth Classic + BLE 4.2.
- No native USB; programming goes through an external USB-UART bridge.
- Toolchain prefix: `xtensa-esp32-elf-`.

## Pins to avoid or treat with care
- **GPIO6–11:** connected to SPI flash on almost every module. Never use.
- **GPIO16/17:** used by PSRAM on WROVER modules (and on chips with in-package PSRAM).
- **Strapping pins: GPIO0, 2, 5, 12, 15.**
  - GPIO0 low at reset → download mode.
  - GPIO2 must be low/floating to enter download mode.
  - **GPIO12 (MTDI) high at reset selects 1.8 V flash voltage** → boot failure
    with 3.3 V flash. A pull-up on GPIO12 is a classic board bug. If it must
    be used, burn the VDD_SDIO eFuse (irreversible; ask first).
  - GPIO15 low silences boot log output.
- **GPIO34–39:** input only, no internal pull-ups/pull-downs.
- GPIO1/3: UART0 TX/RX (console).

## Peripheral notes
- **ADC2 (GPIO0, 2, 4, 12–15, 25–27) cannot be used while Wi-Fi is on.** Use ADC1 (GPIO32–39).
- DAC on GPIO25/26 (8-bit). Touch sensors on 10 pins.
- PSRAM is not reachable by most DMA engines; allocate DMA buffers from internal RAM.
- Revision v3.0+ (ECO3) fixes several PSRAM/cache errata; check
  `CONFIG_ESP32_REV_MIN` if the silicon revision matters.
