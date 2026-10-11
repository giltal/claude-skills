# Build, flash, partitions, OTA, crash decoding (ESP-IDF)

## Core workflow
```bash
. $IDF_PATH/export.sh            # once per shell (or the IDF installer's shortcut)
idf.py set-target esp32s3        # changing target wipes sdkconfig and the build dir
idf.py menuconfig                # interactive config; result goes to sdkconfig
idf.py build
idf.py -p /dev/ttyUSB0 flash monitor     # Ctrl+] exits monitor
idf.py -p /dev/ttyUSB0 erase-flash       # ask first: wipes NVS too
```
- Keep project defaults in `sdkconfig.defaults` (and
  `sdkconfig.defaults.<target>`), and commit those. Don't hand-edit `sdkconfig`
  for durable settings.
- Add dependencies with the component manager:
  `idf.py add-dependency "espressif/esp_lvgl_port^2"` → `main/idf_component.yml`.

## Partition table
- Custom table: `CONFIG_PARTITION_TABLE_CUSTOM=y`,
  `CONFIG_PARTITION_TABLE_CUSTOM_FILENAME="partitions.csv"`.
- Flash size in menuconfig (`CONFIG_ESPTOOLPY_FLASHSIZE_*`) must match the
  module, or partitions beyond the configured size are rejected.
- App partition too small → the build fails with an overflow; check with
  `idf.py size` and `idf.py size-components`.

## OTA
- Needs `otadata` plus `ota_0` and `ota_1` app partitions of equal size.
- Use `esp_https_ota()` for simple cases. Enable rollback
  (`CONFIG_BOOTLOADER_APP_ROLLBACK_ENABLE`) and call
  `esp_ota_mark_app_valid_cancel_rollback()` after the new image proves healthy.

## Decoding crashes
- `idf.py monitor` decodes backtraces automatically when it runs against the
  same build directory as the flashed firmware.
- Manual decode with the target's addr2line (the prefix is in the chip file):
  ```bash
  xtensa-esp32s3-elf-addr2line -pfiaC -e build/<project>.elf 0x42001234 0x42005678
  riscv32-esp-elf-addr2line   -pfiaC -e build/<project>.elf 0x42001234
  ```
- On RISC-V targets the panic handler prints a stack dump; enable
  `CONFIG_ESP_SYSTEM_USE_EH_FRAME` for full backtraces.
- Core dump to flash: `CONFIG_ESP_COREDUMP_ENABLE_TO_FLASH`, then
  `idf.py coredump-info` / `coredump-debug`.
- Common panic reasons:
  - `LoadProhibited`/`StoreProhibited` (Xtensa) or `Load/Store access fault`
    (RISC-V): null or dangling pointer.
  - `Cache disabled but cached memory region accessed`: an ISR or callback is
    not in IRAM, or it touches flash data during a flash write.
  - `Stack canary watchpoint triggered`: task stack too small.
