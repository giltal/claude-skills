# ESP32-S3

- CPU: dual-core Xtensa LX7, up to 240 MHz, with vector (SIMD) instructions
  used by ESP-DSP / ESP-NN. 512 KB SRAM.
- Radio: Wi-Fi 4 (2.4 GHz), BLE 5. No Bluetooth Classic.
- Native USB: USB-OTG (TinyUSB) and USB-Serial-JTAG share **GPIO19 (D−) / GPIO20 (D+)**.
- Toolchain prefix: `xtensa-esp32s3-elf-`.

## Pins to avoid or treat with care
- **GPIO26–32:** SPI flash / quad PSRAM. Do not use.
- **GPIO33–37:** also taken on modules with **octal** flash or PSRAM
  (e.g. N16R8, N8R8). Check the module part number before using them.
- **Strapping pins: GPIO0, 3, 45, 46.**
  - GPIO0 low at reset → download mode.
  - GPIO45 selects VDD_SPI voltage (high = 1.8 V). Keep low for 3.3 V flash.
  - GPIO46 must not be high together with GPIO0 low.
  - GPIO3 selects the JTAG signal source.
- **GPIO39–42:** default JTAG (MTCK, MTDO, MTDI, MTMS) when using an external probe.
- GPIO19/20 are free for GPIO only if native USB is not used.
- GPIO43/44: UART0 TX/RX (console).

## Peripheral notes
- Prefer ADC1 (GPIO1–10). ADC2 (GPIO11–20) is shared with Wi-Fi.
- LCD: i80 parallel and RGB panel interfaces (`esp_lcd`). The RGB panel
  needs PSRAM framebuffers; enable `CONFIG_SPIRAM_FETCH_INSTRUCTIONS` and
  `CONFIG_SPIRAM_RODATA`, or use bounce buffers, to avoid display drift during
  flash writes.
- Camera: DVP interface (esp32-camera component).
- Octal PSRAM: set `CONFIG_SPIRAM_MODE_OCT`. A mismatch with the module
  causes PSRAM init failure at boot.
- Console: if the board has no UART bridge, set the console to
  USB-Serial-JTAG (`CONFIG_ESP_CONSOLE_USB_SERIAL_JTAG`).
