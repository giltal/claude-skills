# ESP32-P4

> Values marked (verify) should be checked against the current ESP32-P4
> datasheet and the board schematic. The P4 is new, and details vary
> between silicon revisions.

- CPU: dual-core RISC-V HP (up to 360 MHz on v1.x silicon; higher on newer
  revisions (verify)), plus an LP RISC-V core. 768 KB HP L2 memory;
  many variants have in-package PSRAM (16/32 MB).
- **No Wi-Fi or Bluetooth.** Wireless comes from a companion chip, usually an
  ESP32-C6 running ESP-Hosted (SDIO) — use `esp_wifi_remote` +
  `esp_hosted` components; the C6 needs its own matching slave firmware.
- Multimedia: MIPI-DSI (display), MIPI-CSI + ISP (camera), H.264 encoder,
  JPEG codec, PPA (pixel processing accelerator: scale/rotate/blend),
  2D-DMA.
- Connectivity: USB 2.0 High-Speed OTG, USB-Serial-JTAG, Ethernet MAC (RMII),
  SDIO 3.0 host.
- Toolchain prefix: `riscv32-esp-elf-`.

## Silicon revision and IDF version
- Check the revision (`esptool` prints it; also in the boot log).
  ESP-IDF needs `CONFIG_ESP32P4_REV_MIN` set to match. Images built for one
  revision family may not boot on another (verify for v3.x silicon).
- Use a recent ESP-IDF (5.4+; 5.5+ for newer silicon revisions (verify)).
  P4 drivers are moving quickly; check the IDF release notes for the version in use.

## Pins to avoid or treat with care
- Strapping pins: GPIO34–38 (verify against the datasheet for the revision in use).
- Pins used for in-package PSRAM and flash are not available.
- MIPI-DSI/CSI use dedicated pins, not the GPIO matrix.
- The P4 has several power domains; some GPIO banks have separate IO voltage
  rails (e.g. 1.8 V vs 3.3 V for the SDIO/SD pins). Check the board schematic
  before connecting 3.3 V peripherals.

## Peripheral notes
- Display pipeline: `esp_lcd` MIPI-DSI panel driver + LVGL (esp_lvgl_port).
  Put framebuffers in PSRAM and use PPA / 2D-DMA for blits instead of the CPU.
- Camera: `esp_video` / `esp_cam_sensor` components for MIPI-CSI sensors.
- Cache coherence: after DMA writes into PSRAM, invalidate with
  `esp_cache_msync()` before the CPU reads; write back before DMA reads.
  Align buffers to the cache line size (use `heap_caps_aligned_alloc` or
  `MALLOC_CAP_CACHE_ALIGNED`).
- Wi-Fi via the C6: the SDIO pin assignment and the C6 reset GPIO depend on
  the board; set them in menuconfig under the ESP-Hosted options.
