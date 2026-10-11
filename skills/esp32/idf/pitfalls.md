# Common pitfalls

## ESP-IDF 5.x driver changes
The legacy drivers still compile with deprecation warnings, but you can't mix
a legacy and a new driver for the same peripheral (startup abort). Use the new
ones in new code:

| Peripheral | Legacy (avoid)                  | IDF 5.x                                   |
|------------|---------------------------------|-------------------------------------------|
| I2C        | `driver/i2c.h`                  | `driver/i2c_master.h` / `i2c_slave.h`     |
| ADC        | `driver/adc.h`, `esp_adc_cal.h` | `esp_adc/adc_oneshot.h`, `adc_continuous.h`, `adc_cali.h` |
| Timer      | `driver/timer.h`                | `driver/gptimer.h`                        |
| RMT        | `driver/rmt.h`                  | `driver/rmt_tx.h` / `rmt_rx.h`            |
| PCNT       | `driver/pcnt.h`                 | `driver/pulse_cnt.h`                      |
| I2S        | `driver/i2s.h`                  | `driver/i2s_std.h`, `i2s_pdm.h`, `i2s_tdm.h` |
| Temp sensor| `driver/temp_sensor.h`          | `driver/temperature_sensor.h`             |

Arduino-ESP32 3.x is built on IDF 5.x, so the same changes affect Arduino
sketches that call IDF APIs directly. Core 2.x code (e.g. `ledcSetup`/`ledcAttachPin`)
must be ported to the 3.x API (`ledcAttach`).

## Watchdogs
- **Task WDT:** a task (often the idle task) didn't run for ~5 s. Cause: busy
  loops without `vTaskDelay`, or a high-priority task hogging a core. Fix the loop;
  don't just disable the watchdog.
- **Interrupt WDT:** an ISR ran too long or interrupts stayed disabled. Move work out of the ISR.

## Memory
- DMA buffers: `MALLOC_CAP_DMA`. Classic ESP32 PSRAM is not DMA-capable;
  S3/P4 GDMA can reach PSRAM, but cache sync and alignment still apply.
- Large buffers go to PSRAM with `MALLOC_CAP_SPIRAM`, or enable
  `CONFIG_SPIRAM_USE_MALLOC` and threshold settings.
- Check stack high-water marks with `uxTaskGetStackHighWaterMark()` when tuning stacks.

## ISRs and flash
- During flash writes (NVS, OTA, SPIFFS/LittleFS) the cache is disabled.
  ISRs that may fire then need `ESP_INTR_FLAG_IRAM`, `IRAM_ATTR` code, and
  `DRAM_ATTR` constants.
- No `printf`/`ESP_LOGx` inside ISRs; use `ESP_DRAM_LOGx` sparingly, or defer to a task.

## Startup
- Wi-Fi needs NVS: call `nvs_flash_init()` (erase and retry on
  `ESP_ERR_NVS_NO_FREE_PAGES` / `ESP_ERR_NVS_NEW_VERSION_FOUND`) before `esp_wifi_init()`.
- Brownout resets on Wi-Fi start usually mean a weak 3.3 V supply or missing
  bulk capacitance. Fix the hardware; don't disable the brownout detector.
- FreeRTOS tick defaults to 100 Hz: `vTaskDelay(1)` is 10 ms. Use
  `pdMS_TO_TICKS()`, and don't assume 1 ms resolution.
