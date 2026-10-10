# microHAMCLOCK manual

The complete manual for microHAMCLOCK on the Heltec WiFi LoRa 32 V3. A short
overview is in the [README](../README.md).

A small ham radio clock on a 128×64 OLED display: UTC, propagation
conditions and live PSKReporter spots (who heard you), as a list and on
a world map. No external libraries, and all it needs is Wi-Fi.

Versions are numbered `0.x.y` while the project is unfinished. What changed
in each version is in the [CHANGELOG.md](../CHANGELOG.md). The current
version is shown at startup, on the status screen (triple click), in the
`status` command and on the setup page. Firmware built between releases
shows `+` and the number of commits since the release after the number on
the display (for example `v0.5.1+3`), and the exact git description in
`status`, for example `0.5.1-3-g1a2b3c4` = 3 commits after version 0.5.1.

## Language

The display and the setup page are available in **English** (the default),
**Czech** and **German**. You choose the language during setup: on the web page it is
the first field of the form (the page switches right away), in the console
it is the wizard's first question. The serial console is always in English.

The texts live in the catalogs `src/lang/<code>.inc` (`en.inc` is the
master; a missing translation falls back to English). To add a language:

1. copy `src/lang/en.inc` to `src/lang/<code>.inc` and translate the texts,
2. add `LANG_<CODE>` to `enum Lang` in `src/i18n.h`,
3. add a row to the `LANGS` table in `src/i18n.cpp`,
4. run `python tools/check_lang.py`. The check finds missing texts,
   `%s`/`%d` placeholders that differ from the English ones, and accented
   characters in display texts. The display font is ASCII only; the web
   page can use UTF-8.

## Flashing

The easiest way is the web installer: open it in Chrome, Edge or Opera on a
computer, connect the board with a USB-C cable and press **Install**. On an
update your settings are kept unless you choose to erase the device.

To flash by hand, download `heltec_v3_microhamclock-merged.bin` from the
[latest release](../../../releases/latest) and flash it with any ESP32-S3
flasher, for example the MeshCore web flasher. microHAMCLOCK is not in its list;
choose a custom file from your computer. The file is written from address
0x0, with the flash erased. From the command line:

```
esptool.py --chip esp32s3 write_flash 0x0 heltec_v3_microhamclock-merged.bin
```

If you build from source, the project uses PlatformIO (run in the project
folder):

```
pio run -t upload
```

## Setup

Wi-Fi, callsign and locator are not entered in the source code, so there
are no passwords in the binary. You can set them in three ways, and all are
available at the same time:

### In the web installer (computer)

Right below the Install button, the installer page has a **Set up** step.
Close the installer window first, then press **Connect to microHAMCLOCK** (the
browser may ask for the serial port again). The form is filled in with what
the board already has, except the password. Pick the display language, your
Wi-Fi from the list the board has scanned (**Scan again** looks again,
**Other network** lets you type the name; only 2.4 GHz networks work), the password, your callsign and locator, and check the time
zone, which is preselected from your computer. An empty password keeps the
stored one. After **Save** the board restarts and the page follows it:
connecting to Wi-Fi, getting the time, listening for your spots. If the
Wi-Fi doesn't connect within 45 seconds, the page says why and shows the form
again. **Disconnect** releases the serial port for other programs.

The other settings (screen rotation, screen saver, night, brightness, NVIS,
ionosonde) are on the hotspot setup page.

### Over the hotspot (phone, laptop)

As long as the board is not set up, it starts an open Wi-Fi network
**MICROHAMCLOCK-xxxx** at power-on (the name is on the display). Connect to it:
your phone will usually open the setup page by itself, otherwise open
`http://4.3.2.1`. In the form, choose the language, pick your Wi-Fi from
the list, enter the password, your callsign and locator, check the time
zone (preselected from your phone), adjust the screen saver and night if
you like, and press **Save and restart**. The hotspot then turns off.

Later you can get back into setup mode by **holding the PRG button for
10 s**. After 2 s a countdown appears on the display. This works at any
time, even while the board is still waiting in vain for a Wi-Fi network
entered earlier. Your saved values are not erased:

- the form is prefilled,
- an empty password keeps the saved one,
- **Leave without saving** or a short press of the button returns the
  board to normal operation with no changes.

If the board can't connect after saving, the display shows why
(`WRONG PASSWORD?` or `NETWORK NOT FOUND`) and it keeps trying every
minute. The fix is the same: hold the button for 10 s and enter the
correct details.

If nothing happens in setup mode for 10 minutes, a board that is already
set up returns to normal operation by itself. It also returns after a power
cycle.

### Over USB (serial console)

Connect the board over USB and open the serial console (115200 baud):

```
pio device monitor
```

and type `setup`. The board asks you, step by step, for:

1. the display language (`en`, `cs`, `de`),
2. the Wi-Fi network (SSID) and password,
3. your callsign,
4. your locator (4 or 6 characters, for example JO70va),
5. the time zone: part of a city name is enough (`prague`, `new york`), or
   a fixed offset such as `UTC+3`; `list` prints them all,
6. the screen saver: after how many minutes (0 = never), what it does
   (`off`, `life`, `dim`) and whether a new spot wakes the display;
   optionally a LED flash when a spot wakes it,
7. night: the hours (for example `22-6`) and the behaviour (`button`,
   `spots`, `dark`).

Enter keeps the value in square brackets, `cancel` quits the wizard without
saving. After you confirm, everything is saved to flash and the board
restarts.

Once connected to Wi-Fi, the board gets the time from an NTP server (see
below). Local time follows the chosen zone, including daylight saving time.
The list has about 50 regions named after cities (`src/tz.cpp`). If yours
isn't there, choose a region with the same time, or a fixed offset from
UTC−12 to UTC+14 (without daylight saving time).

## Screen saver and night

To keep the OLED from burning in, a screen saver starts after the set time
of inactivity (10 min by default):

| option | what it does                                                     |
|--------|------------------------------------------------------------------|
| `off`  | the display turns off completely (default, no burn-in at all)    |
| `life` | runs the Game of Life, with no text, dimmed                      |
| `dim`  | the picture stays, dimmed and shifted by up to 2 px every minute |

- Activity means a button press and (when waking on spots is on) **every
  new spot**. When you transmit and someone hears you, the display lights
  up on the spot list and stays on as long as spots keep coming. Only spots
  younger than 15 minutes wake it, late reports don't.
- The first button press only wakes the display and doesn't switch
  anything. Holding it for 10 s to enter setup always works.
- The built-in LED flashes once for 0.5 s when a spot wakes the display.
  This option is on by default, you can turn it off on the web page or in
  the console, and it applies to all three screen savers. Once
  the display is awake, further spots don't flash the LED. Waking with the
  button doesn't flash it; the night restriction on waking by spots applies
  to the LED too.
- The spots come from PSKReporter, so they cover every mode that someone
  decodes automatically (FT8, FT4, JS8, PSK, RTTY, CW…). An SSB or FM
  contact won't wake the display.

At night (22–06 local time by default) the display is dimmed and, depending
on the setting: `button` = only the button wakes it, `spots` = spots wake
it too (default), `dark` = it stays off. The same hour for start and end
means no night.

The setup page has a checkbox for automatic screen rotation (on by
default; a double click on the button toggles it too). How many seconds
each screen stays up (15 by default, 5–120) is in the **Advanced**
section.

You can change the display brightness for day, night and both screen
savers on the web page, in the **Advanced** section (in percent). When you
move a slider, the display shows that brightness for a few seconds; it is
saved only with the Save button.

The Game of Life saver runs until something wakes the display. If you'd
rather not have it running for days while you're away, tick **turn the
display off after some days of Game of Life** in **Advanced** and set the
number of days (2 by default, 1–30; off by default). After that time the
display turns off, but Game of Life stays the screen saver: the button or
a spot wakes the display as usual, and the next time the saver starts,
the days count from zero again.

The **Advanced** section also has the propagation options:
- **NVIS margin** – how many percent below foF2 the recommended NVIS band
  must lie. The default is 0 % (the band right below foF2); the classic
  optimum working frequency (FOT) is 15 % lower.
- **60 m band** – whether to recommend it for NVIS (yes by default; it
  isn't allowed everywhere).
- **Ionosonde** – an empty field = the nearest ionosonde with a fresh
  measurement within 1500 km of your locator. Or a GIRO station code, for
  example `PQ052` (Průhonice); the codes are on the map at
  [prop.kc2g.com](https://prop.kc2g.com/).

**Country maps** in **Advanced** add the maps of single countries to the
map views: Czechia, Germany, the United Kingdom and the USA (the 48
contiguous states). All are off by default. See the map screen below.

Other console commands:

| command    | what it does                                                  |
|------------|---------------------------------------------------------------|
| `status`   | prints the settings (time zone, screen rotation, screen saver, Game of Life limit, night, brightness, NVIS, country maps, ionosonde choice), Wi-Fi, time, MQTT, spot count and propagation data (formerly `stav`, which still works) |
| `snapshot` | prints the display contents; `python tools/snapshot.py COM4 screen.png` turns them into a PNG (formerly `snimek`, which still works) |
| `blink`    | switches to the propagation screen and demonstrates the flash, as if new data had arrived |
| `saver`    | turns the screen saver on right away: `saver` the one you set, `saver off`, `saver life` or `saver dim` a given one. The settings don't change; the button, or a spot when spots may wake the display, ends it as usual. Handy for trying the savers and the LED flash on a spot without waiting |

## Screens

| screen          | what it shows                                             |
|-----------------|-----------------------------------------------------------|
| Clock           | UTC in big digits, UTC date, local time, callsign and locator |
| Propagation     | SFI, SN, A, K, the recommended NVIS band, X-ray, foF2 and MUF(3000) from the nearest ionosonde, day and night conditions for 80–10 m (good ones are framed); briefly inverts when new data arrives |
| Heard me: list  | stations that heard you in the last hour: callsign, band, SNR, km |
| Heard me: map   | the same on a map; dotted land = day, outline only = night (the grey line) |

On the map your home is an empty square with a dot, each spot a filled
square, and new spots blink for the first minute. The number in the bottom
left corner is the count of spots visible on the map.

The map has the views WORLD and EUROPE, and the country views CZECHIA,
GERMANY, UK and USA, each of which you switch on in **Advanced** (all off
by default). A country map shows just the territory of that country. The
Czechia, Germany and UK maps are just the outline of the borders, without
day and night; the USA
map (the 48 contiguous states, without Alaska and Hawaii) has day and night
like the others. In AUTO mode the map shows a switched-on country when your
home and all spots are in it, Europe when they are all in Europe, and
otherwise the whole world.

## Controls (PRG button)

| press     | action                                                       |
|-----------|--------------------------------------------------------------|
| short     | next screen                                                  |
| double    | automatic screen rotation on/off (15 s per screen, set on the web) |
| triple    | status screen (Wi-Fi, IP, MQTT, data age, version)           |
| long (0.7 s, fires while still held) | list: sort by time / distance; map: AUTO → WORLD → EUROPE → CZECHIA → GERMANY → UK → USA (only the switched-on countries) |
| hold 10 s | setup mode (hotspot), see Setup                              |

Rotation, sorting and the map view are saved to flash memory. The long
press action fires only once; releasing the button doesn't switch anything
again. If you keep holding, setup opens after 10 s, even though the map or
the list sorting has switched along the way. At night the display is
dimmed, see Screen saver and night.

## Where the data comes from

- **PSKReporter** – the public MQTT feed `mqtt.pskreporter.info:1883`,
  subscription `pskr/filter/v2/+/+/YOURCALL/#`. Your callsign is subscribed
  in its base form and with the `/P` and `/M` suffixes (the list is in the
  `CALL_SUFFIXES` constant), so it doesn't matter whether you enter
  `OK2MTB` or `OK2MTB/P`. The feed is live only, so the list is empty after
  power-on and fills up as stations hear you (WSJT-X sends its reports
  about every 5 minutes).
- **Ionosonde** – foF2 and MUF(3000) from the nearest GIRO ionosonde that
  has a fresh measurement and is within 1500 km of your locator (in
  Czechia usually Průhonice, PQ052, run by the Institute of Atmospheric
  Physics of the Czech Academy of Sciences). The data comes from
  `https://prop.kc2g.com/api/stations.json` and is refreshed every 10
  minutes. A measurement older than 90 minutes shows as `--`. The code of
  the station in use is on the status screen; you can enter a different
  station in Advanced. Fresh data is available in Europe, the Americas,
  South Africa and Australia; in Asia there is almost none at the moment.
- **NVIS** – the recommended band is the highest band (160–20 m) whose
  lower edge lies below foF2 reduced by the margin from Advanced.
- **Propagation** – XML from N0NBH, `https://www.hamqsl.com/solarxml.php`,
  refreshed every 30 minutes.
- **Time** – NTP `ntp.ufe.cz` (the Institute of Photonics and Electronics
  of the Czech Academy of Sciences, which maintains the Czech national time
  standard). `tik.cesnet.cz` and `pool.ntp.org` serve as backups. The board
  synchronizes after connecting to Wi-Fi and then about every hour.
- **Map** – Natural Earth (public domain): land from `ne_110m_land`, the
  borders of Czechia, Germany, the UK and the USA from `ne_10m_admin_0_countries`. The `tools/make_map.py`
  script turns them into 128×64 bitmaps in `src/maps.h`.

All parameters (default rotation, spot window, default brightness…) are in the
`SETTINGS` section at the top of `src/main.cpp`.
