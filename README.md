<div align="center">

# microHAMCLOCK

**A pocket-sized ham radio clock that shows who is hearing you, right now.**

UTC · propagation · nearest ionosonde · live PSKReporter spots on a list and a world map,
on the tiny OLED of a Heltec WiFi LoRa 32 V3.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Board](https://img.shields.io/badge/board-Heltec%20WiFi%20LoRa%2032%20V3-orange)
![MCU](https://img.shields.io/badge/MCU-ESP32--S3-red)
![Built with PlatformIO](https://img.shields.io/badge/built%20with-PlatformIO-f5822a)

<img src="docs/img/demo.png" width="540" alt="microHAMCLOCK cycling through its screens: clock, propagation, list of stations that heard you, map">

</div>

Call CQ on FT8, glance at your desk, and see the stations that decoded you pop up on the display,
with band, SNR and distance, and as dots on a map with the day/night terminator. Between QSOs it is a
clean UTC clock with solar data and a band recommendation for NVIS. No app, no account, no cloud of your
own: the board talks straight to public ham radio data feeds over Wi-Fi.

## Features

- 🕐 **Clock**: big UTC with seconds, date, and local time with automatic daylight saving time
  (about 50 city regions plus fixed UTC offsets).
- ☀️ **Propagation**: solar flux, sunspot number, A and K index, X-ray class and HF band conditions
  for day and night (N0NBH).
- 📡 **Nearest ionosonde**: foF2 and MUF(3000) from the closest GIRO ionosonde with a fresh
  measurement, picked automatically from your locator, plus the **recommended NVIS band**.
- 👂 **Who hears me**: live PSKReporter spots of your callsign over MQTT, any mode that gets
  decoded automatically (FT8, FT4, JS8, PSK, RTTY, CW…). Your `/P` and `/M` variants are included.
- 🗺️ **Map**: world, Europe and Czechia views with the day/night terminator. AUTO zooms to fit
  your spots, and new spots pulse.
- 🌙 **Kind to the OLED**: screen saver (off, Game of Life, or dim and shift), night mode, and an
  optional wake-up when a new spot arrives, with an LED flash if you like.
- 📱 **Easy setup**: install and set up in one browser page over USB, or from your phone through
  the board's own Wi-Fi hotspot. No passwords in the firmware, and entering setup never erases
  what you saved.
- 🌍 **Localized**: English and Czech on the display and the setup page, and easy to translate.
- 🪶 **Lightweight**: plain C++ on the Arduino core, with no external libraries.

## Screens

<table>
  <tr>
    <td align="center"><img src="docs/img/clock.png" width="400" alt="Clock screen"><br><b>Clock</b><br>UTC, date, local time, callsign and locator</td>
    <td align="center"><img src="docs/img/propagation.png" width="400" alt="Propagation screen"><br><b>Propagation</b><br>SFI, SN, A, K, NVIS band, X-ray, foF2, MUF, band conditions</td>
  </tr>
  <tr>
    <td align="center"><img src="docs/img/heard-list.png" width="400" alt="List of stations that heard you"><br><b>Heard me: list</b><br>callsign, band, SNR, km; sorted by time or distance</td>
    <td align="center"><img src="docs/img/heard-map.png" width="400" alt="Map of stations that heard you"><br><b>Heard me: map</b><br>home square, spots, dotted land in daylight</td>
  </tr>
</table>

<sub>Screens rendered from the firmware's own font and map data, with example values.</sub>

## What you need

- A **[Heltec WiFi LoRa 32 V3](https://heltec.org/project/wifi-lora-32-v3/)** (ESP32-S3 with a
  0.96″ 128×64 OLED). The LoRa radio is not used.
- A USB-C cable and a 2.4 GHz Wi-Fi network.
- Your callsign and Maidenhead locator.
- Optional, recommended: a 3D-printed case. The
  [Bender Battery Case for the Heltec V3](https://www.printables.com/model/797822-bender-battery-case-for-the-heltec-v3-heltec-t114)
  by zerofox3D on Printables fits well: it clips together without screws, keeps both buttons
  (PRG and RST) reachable, has a bay for an 18650 battery and an optional on/off switch. The
  model is free for personal use only, so please don't sell prints of it.

## Quick start

1. **Flash** it in one click: open the **[web installer](INSTALLER_URL)** in Chrome, Edge or
   Opera on a computer, plug in the board, press **Install**. That's it, no tools to install.

   <details><summary>Prefer to flash by hand?</summary>

   Download `heltec_v3_microhamclock-merged.bin` from the [latest release](../../releases/latest) and
   write it at address `0x0`, for example with [esptool-js](https://espressif.github.io/esptool-js/)
   or from the command line:
   ```
   esptool.py --chip esp32s3 write_flash 0x0 heltec_v3_microhamclock-merged.bin
   ```
   If the board does not connect, hold **PRG**, tap **RST** and release **PRG**.
   </details>

2. **Set it up** right on the same page: press **Connect to microHAMCLOCK**, pick your Wi-Fi from the
   list, enter the password, your callsign and locator, and **Save**. The page then shows the board
   connecting to Wi-Fi, getting the time and listening for your spots.

   No computer at hand? The board also starts a Wi-Fi hotspot called **MICROHAMCLOCK-xxxx**. Join it
   with your phone and the setup page opens by itself (or go to `http://4.3.2.1`).
3. **Get on the air**: call CQ in FT8 and watch the list fill up as stations hear you.
   (WSJT-X reports to PSKReporter about every 5 minutes.)

Need to change something later? **Hold PRG for 10 seconds** to get back to the setup page.

## Controls

One button, **PRG**:

| Press | Action |
|---|---|
| Short | next screen |
| Double | auto-rotate screens on/off (15 s per screen by default) |
| Triple | status screen (Wi-Fi, IP, MQTT, data age, version) |
| Long (0.7 s) | list: sort by time or distance · map: AUTO → WORLD → EUROPE → CZECHIA |
| Hold 10 s | setup mode (hotspot) |

## Data sources and thanks

microHAMCLOCK only shows data that others kindly make public. Thank you to:

- **[PSKReporter](https://pskreporter.info/)** by Philip Gladstone, N1DQ, and its live
  **MQTT feed** by Tom Fanning, M0LTE: the reception reports.
- **[N0NBH](https://www.hamqsl.com/solar.html)**, Paul Herrman: solar and band condition data.
- **[KC2G](https://prop.kc2g.com/)** and the **[GIRO](https://giro.uml.edu/)** ionosonde network:
  foF2 and MUF measurements.
- **[Natural Earth](https://www.naturalearthdata.com/)**: public domain map data.
- **NTP**: [ntp.ufe.cz](https://www.ufe.cz/) (the Czech national time standard), `tik.cesnet.cz`
  and `pool.ntp.org`.

## Building from source

The project uses [PlatformIO](https://platformio.org/):

```
pio run                               # build
pio run -t upload --upload-port COM4  # flash
pio device monitor                    # serial console, 115200 baud
```

The serial console understands `setup` (a step-by-step setup wizard), `status`, `snapshot`
(a screen dump; `python tools/snapshot.py COM4 screen.png` turns it into a PNG), `blink` and
`saver [off|life|dim]` (the screen saver right away).
`python tools/build_site.py --serve` builds the web installer and serves it on localhost.

## Translations

Display and web texts live in `src/lang/<code>.inc`, with `en.inc` as the master. To add a language,
copy `en.inc`, translate it, register the language in `src/i18n.h` and `src/i18n.cpp`, and run
`python tools/check_lang.py`. Display texts must be ASCII, because the OLED font has no accents.
Pull requests with new languages are very welcome.

## Documentation

- [Full manual](docs/manual.md): setup over USB, screen saver and night mode, advanced settings,
  details on every data source.
- [Changelog](CHANGELOG.md)

## About the name

microHAMCLOCK is a tribute to [HamClock](https://www.hamclock.com/) by Elwood Downey, WB0OEW (SK),
the clock that has graced so many shacks, which the community keeps going as
[OpenHamClock](https://github.com/openhamclock). microHAMCLOCK is a separate, much smaller project
with its own code. It is not affiliated with HamClock, the Clear Sky Institute or microHAM s.r.o.

## Made with AI assistance

microHAMCLOCK was designed and tested by OK2MTB and written with the help of AI: the code and
documentation were developed in conversation with Claude (Anthropic) in Claude Code. Every feature
was decided by a human and verified on real hardware.

## License

[MIT](LICENSE). The firmware binaries also contain the Arduino-ESP32 core (LGPL-2.1) and ESP-IDF
components (mostly Apache-2.0), under their own licenses. The map data is public domain (Natural Earth).

<div align="center">

**73 de OK2MTB**

</div>
