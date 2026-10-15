# microHAMCLOCK development

How to build microHAMCLOCK from source and how it fits together. Using the
clock is described in the [manual](manual.md); how to contribute, including
translations, in [CONTRIBUTING.md](../CONTRIBUTING.md).

## Building and flashing

The project uses [PlatformIO](https://platformio.org/) with the stock
`espressif32` platform (Arduino core 2.x) and no external libraries. Run
these in the project folder (`python -m platformio …` works when `pio` is
not on the PATH):

```
pio run                               # build
pio run -t upload --upload-port COM4  # flash (the board's USB bridge is a CP210x)
pio device monitor                    # serial console, 115200 baud
```

`pio device list` shows the ports when more boards are attached.

There are no automated tests. A change is checked by building, flashing and
reading the serial log: `WiFi: connected`, `MQTT: subscribing to …`,
`Spot: …`, `Propagation: …`.

## Version numbers

Versions are numbered `0.x.y` while the project is unfinished; what changed
is in the [changelog](../CHANGELOG.md). Before each build,
`tools/version.py` takes the version from `git describe`. Firmware built
between releases shows `+` and the number of commits since the release
after the number on the display (for example `v0.5.1+3`), and the exact git
description in `status` and on the setup page, for example
`0.5.1-3-g1a2b3c4` = 3 commits after version 0.5.1. A `-dirty` suffix means
uncommitted changes.

## Serial console for testing

Besides the commands in the [manual](manual.md#serial-console), the console
has these for testing:

| command    | what it does                                                  |
|------------|---------------------------------------------------------------|
| `snapshot` | prints the display contents (formerly `snimek`, which still works) |
| `blink`    | switches to the propagation screen and fakes new data a second later, so the data flash can be watched |

`stav` still works as an alias of `status`.

`python tools/snapshot.py COM4 screen.png` sends `snapshot` and saves the
current screen as a PNG, so layouts can be checked without a photo. It
opens the port without resetting the board, and it can't run while
`pio device monitor` holds the port.

## Source layout

| path                 | what it is                                             |
|----------------------|--------------------------------------------------------|
| `src/main.cpp`       | the firmware: display, font, settings, network task, MQTT client, data downloads, setup modes, screens |
| `src/i18n.*`, `src/lang/*.inc` | translations of the display and the setup page |
| `src/tz.*`           | the time zone table (about 50 city regions plus fixed offsets) |
| `src/life.*`         | the Game of Life screen saver                          |
| `src/maps.h`         | the map bitmaps, generated, don't edit by hand         |
| `web/index.html`     | the web installer page                                 |
| `partitions.csv`     | the flash layout; the settings sit behind the app so that an update keeps them |
| `tools/`             | helper scripts, see below                              |

All tunable parameters (default screen switching, spot window, default
brightness, refresh intervals…) are in the `SETTINGS` section at the top of
`src/main.cpp`.

## Where the data comes from

- **PSKReporter** – the public MQTT feed `mqtt.pskreporter.info:1883`,
  subscription `pskr/filter/v2/+/+/YOURCALL/#` (a `/` in the callsign
  becomes `.`). The callsign is subscribed as entered, in its base form and
  with each suffix in `CALL_SUFFIXES` (`/P`, `/M`). Spots older than an hour
  expire; a station is kept once per band.
- **Ionosonde** – `https://prop.kc2g.com/api/stations.json`, every 15
  minutes. The board takes the nearest station within 1500 km of the
  locator with a measurement younger than 90 minutes, and keeps the current
  station while it is at most 300 km farther than the nearest.
- **Propagation** – `https://www.hamqsl.com/solarxml.php`, every hour.
- **Time** – NTP `ntp.ufe.cz`, `tik.cesnet.cz`, `pool.ntp.org`.

Refresh times have ±10 % jitter and the first download waits up to a minute
after Wi-Fi comes up, so boards don't all ask at once. A failed download is
retried after 2 minutes, doubling up to an hour. Requests carry a
`microHAMCLOCK/<version>` User-Agent with the project's address.

## Maps

`src/maps.h` is generated from [Natural Earth](https://www.naturalearthdata.com/)
data (public domain), downloaded from
[github.com/nvkelso/natural-earth-vector](https://github.com/nvkelso/natural-earth-vector):

```
python tools/make_map.py <ne_110m_land.geojson> <ne_10m_admin_0_countries.geojson>
```

`--preview <dir>` also writes PNG previews. The views are defined in
`VIEWS` in the script: WORLD and EUROPE are land masks from `ne_110m_land`,
CZECHIA, GERMANY, UK and USA the territory of one country from
`ne_10m_admin_0_countries`.

## Other tools

- `python tools/readme_screens.py` renders the screen images in `docs/img/`
  for the README with example data. It is a Python copy of the screen
  renderers, so update it when a screen layout changes.
- `python tools/check_lang.py` checks the translation catalogs, see
  [CONTRIBUTING.md](../CONTRIBUTING.md#translations).
- `python tools/build_site.py --serve` builds the web installer into `site/`
  and serves it on localhost, where browsers allow Web Serial, so it can be
  tried in Chrome. It needs the merged binary in `firmware/`, which
  `tools/release.py build` makes.
- `tools/release.py` builds and publishes a release (maintainer only).
