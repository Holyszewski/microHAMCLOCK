# microHAMCLOCK manual

The complete user manual for microHAMCLOCK on the Heltec WiFi LoRa 32 V3. A
short overview is in the [README](../README.md); building the firmware
yourself is described in [development.md](development.md).

microHAMCLOCK is a small ham radio clock on a 128×64 OLED display: UTC,
propagation conditions and live PSKReporter spots (who heard you), as a list
and on a world map. All it needs is Wi-Fi.

It is meant mainly for stationary use: on your desk, plugged into a USB
charger or power supply all the time, with or without a battery. Wi-Fi
stays on, so a battery alone doesn't last long.

## What you need

- A **Heltec WiFi LoRa 32 V3** (ESP32-S3 with a 0.96″ 128×64 OLED; V3,
  V3.1 and V3.2 all work). The LoRa radio is not used.
- A USB-C cable that carries data (some only charge) and a computer with
  Chrome, Edge or Opera for installing.
- A USB charger or power supply. A battery is not needed.
- A **2.4 GHz** Wi-Fi network (the board can't use 5 GHz), your callsign and
  your Maidenhead locator.

## Installing the firmware

The easiest way is the **web installer**: open it in Chrome, Edge or Opera on a
computer, connect the board with a USB-C cable and press **Install**.

To flash by hand, download
[`heltec_v3_microhamclock-merged.bin`](../../../releases/latest/download/heltec_v3_microhamclock-merged.bin)
(this link always gives the latest release; older versions are on the
[releases page](../../../releases)) and flash it with any ESP32-S3
flasher, for example the MeshCore web flasher (microHAMCLOCK is not in its
list; choose a custom file from your computer). The file is written from
address 0x0. From the command line:

```
esptool.py --chip esp32s3 write_flash 0x0 heltec_v3_microhamclock-merged.bin
```

If the board doesn't connect to the flasher, hold **PRG**, briefly press
**RST** and release **PRG**. The board is then ready to be flashed.

**Updating** works the same way and keeps your settings, unless you choose
to erase the device (the installer asks; don't erase when updating).
Erasing, or a factory reset (see [Advanced settings](#advanced-settings)),
returns the board to the state without settings.

Boards that ran a version before 0.10.0 have to be set up once more after
updating: the settings moved to another place in the flash memory, so that
installing a new version doesn't overwrite them any more.

The version is shown at startup, on the status screen (triple click) and on
the setup page. What changed in each version is in the
[changelog](../CHANGELOG.md).

## Setting up

Wi-Fi, callsign and locator are not part of the firmware, so there are no
passwords in it. You enter them in one of three ways, whichever suits you.

The display and the setup page are available in **English** (the default),
**Czech** and **German**; you choose the language first, and the page
switches to it right away. The serial console is always in English.

### In the web installer (computer)

Right below the Install button, the installer page has a **Set up** step.
Close the installer window first, then press **Connect to microHAMCLOCK** (the
browser may ask for the serial port again). The form is filled in with what
the board already has, except the password. Pick the display language, your
Wi-Fi from the list the board has scanned (**Scan again** looks again,
**Other network** lets you type the name), the password, your callsign and
locator, and check the time zone, which is preselected from your computer.
An empty password keeps the stored one. After **Save** the board restarts
and the page follows it: connecting to Wi-Fi, getting the time, listening
for your spots. If the Wi-Fi doesn't connect within 45 seconds, the page
says why and shows the form again. **Disconnect** releases the serial port
for other programs.

The other settings (screen switching, screen saver, night, brightness and
the rest) are on the hotspot setup page.

### Over the hotspot (phone, laptop)

As long as the board is not set up, it starts an open Wi-Fi network
**MICROHAMCLOCK-xxxx** at power-on (the exact name is on the display).
Connect to it: your phone will usually open the setup page by itself,
otherwise open `http://4.3.2.1`. In the form:

1. choose the language at the very top,
2. pick your Wi-Fi from the list (it fills in by itself about 10 seconds
   after the hotspot starts, no need to reload the page; **Search for
   networks again** looks again) and enter its password,
3. enter your callsign and locator (4 or 6 characters, for example JO70va),
4. check the time zone, which is preselected from your phone,
5. adjust screen switching, the screen saver and night if you like (see
   below), and the **Advanced** section if you need it,
6. press **Save and restart**. The hotspot turns off, the board connects to
   your Wi-Fi, sets its clock and starts listening for your spots.

Later you can get back into setup mode by **holding the PRG button for
10 s**. After 2 s a countdown appears on the display. This works at any
time, even while the board is still trying in vain to reach a Wi-Fi network
entered earlier. Your saved values are not erased:

- the form is prefilled,
- an empty password keeps the saved one,
- **Leave without saving** or a short press of the button returns the
  board to normal operation with no changes.

If nothing happens in setup mode for 10 minutes, a board that is already
set up returns to normal operation by itself. It also returns after a power
cycle.

### Over USB (serial console)

Connect the board over USB, open any serial terminal at 115200 baud and
type `setup`. The board asks you, step by step, for:

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
saving. After you confirm, everything is saved and the board restarts.

### Time zone

Once connected to Wi-Fi, the board gets the exact time from the internet.
Local time follows the chosen zone, including daylight saving time. The
list has about 50 regions named after cities. If yours isn't there, choose
a city with the same time, or a fixed offset from UTC−12 to UTC+14 (without
daylight saving time).

### Your callsign

Spots are collected for your callsign in its base form and with `/P` and
`/M`, so it doesn't matter whether you enter `OK2MTB` or `OK2MTB/P`.

## Screens

| screen          | what it shows                                             |
|-----------------|-----------------------------------------------------------|
| Clock           | UTC in big digits, UTC date, local time, callsign and locator |
| Propagation     | SFI, SN, A, K, the recommended NVIS band, X-ray, foF2 and MUF(3000) from the nearest ionosonde, day and night conditions for 80–10 m (good ones are framed) |
| Heard me: list  | stations that heard you in the last hour: callsign, band, SNR, km |
| Heard me: map   | the same on a map; dotted land = day, outline only = night (the grey line) |
| Status          | Wi-Fi network, IP address and signal, the connection to PSKReporter (MQTT), spot count, when the propagation data arrived and when the ionosonde measured (UTC) with the station code, uptime, time sync, battery voltage and firmware version |

**Propagation.** The solar data and band conditions come from N0NBH, foF2
and MUF(3000) from the nearest ionosonde with a fresh measurement (see
[Where the data comes from](#where-the-data-comes-from)). A measurement
older than 90 minutes shows as `--`. NVIS is the recommended band for
short-distance (near vertical) contacts: the highest band (160–20 m) whose
lower edge lies below foF2, reduced by the NVIS margin from **Advanced**.
When new data arrives, the screen briefly flashes inverted.

**Heard me: list.** The list starts empty after power-on, because the
spots come in live; it fills up as stations hear you (WSJT-X sends its
reports about every 5 minutes). Each station is listed once per band.
A long list pages by itself every 5 seconds. A long press switches the
order between the newest first and the farthest first.

**Heard me: map.** Your home is an empty square with a dot, each spot a
filled square, and new spots blink for the first minute; the newest spot is
drawn on top. The number in the bottom left corner is the count of spots
visible on the map. The map has the views WORLD and EUROPE, and the country
views CZECHIA, GERMANY, UK and USA, each of which you switch on in
**Advanced** (all off by default). A country map shows just the territory
of that country. The Czechia, Germany and UK maps are just the outline of
the borders, without day and night; the USA map (the 48 contiguous states,
without Alaska and Hawaii) has day and night like the others. In AUTO mode
the map shows a switched-on country when your home and all spots are in
it, Europe when they are all in Europe, and otherwise the whole world.

## Controls (PRG button)

| press     | action                                                       |
|-----------|--------------------------------------------------------------|
| short     | next screen                                                  |
| double    | automatic screen switching on/off                            |
| triple    | status screen; a short press leaves it                       |
| long (0.7 s, fires while still held) | list: sort by time / distance; map: AUTO → WORLD → EUROPE → CZECHIA → GERMANY → UK → USA (only the switched-on countries); status screen: power off |
| hold 10 s | setup mode (hotspot), see [Setting up](#over-the-hotspot-phone-laptop) |

Screen switching, sorting and the map view are remembered across restarts.
The long press action fires only once; releasing the button doesn't switch
anything again. If you keep holding, setup opens after 10 s, even though
the map or the list sorting has switched along the way. On the status
screen the long press powers the board off, so leave the status screen
before holding the button for setup.

## Automatic screen switching

Automatic switching is on by default and can be turned off on the setup
page or with a double click. Each screen stays up for 15 seconds; you can
set 5–120 seconds in **Advanced**.

Without any spot in the last hour, switching goes between the clock, the
propagation screen and the map: the empty spot list is not shown
automatically, but you can still reach it with the button. In the AUTO
view, which is the world without spots, the map shows where it is day and
night, and it stays up for only 5 seconds, because there is little on it.
As soon as a spot comes in, switching goes through all four screens again.

Two **Advanced** options change this without spots: "without spots, switch
the map too" (on by default) can be turned off, which leaves just the
clock and the propagation screen, and "without spots, switch all screens
too" keeps all four in rotation (off by default). The map option is greyed
out while the "all screens" option is on, because it has no effect then.

## Screen saver and night

To keep the OLED from burning in, a screen saver starts after the set time
of inactivity (10 min by default; 0 = never):

| option                    | what it does                                         |
|---------------------------|------------------------------------------------------|
| turn the display off      | the display turns off completely (default, no burn-in at all) |
| Game of Life              | runs the Game of Life, with no text, dimmed           |
| dim and shift the picture | the picture stays, dimmed and shifted by up to 2 px every minute |

- Activity means a button press and (when "a new spot wakes the display" is
  on, as it is by default) **every new spot**. When you transmit and
  someone hears you, the display lights up on the spot list and stays on as
  long as spots keep coming. Only spots younger than 15 minutes wake it,
  late reports don't.
- The first button press only wakes the display and doesn't switch
  anything, with one exception: when switching runs without spots (see
  above), the press wakes the display on the clock, and switching goes on
  from there. Holding it for 10 s to enter setup always works.
- The built-in LED flashes once for 0.5 s when a spot wakes the display.
  This option is on by default, and it applies to all three screen savers.
  Once the display is awake, further spots don't flash the LED. Waking with
  the button doesn't flash it; the night restriction on waking by spots
  applies to the LED too.
- The spots come from PSKReporter, so they cover every mode that someone
  decodes automatically (FT8, FT4, JS8, PSK, RTTY, CW…). An SSB or FM
  contact won't wake the display.

At night (22–06 local time by default) the display is dimmed and, depending
on the setting:

| at night                          | what happens                            |
|-----------------------------------|-----------------------------------------|
| only the button wakes the display | spots don't wake it                     |
| spots wake the display too        | as during the day, only dimmed (default) |
| the display stays off             | spots don't light it; the button does, until the screen saver time runs out without a press (or until the morning if the screen saver is set to never) |

The same hour for start and end means no night.

## Advanced settings

The setup page has a collapsed **Advanced** section. It opens by itself
when something in it differs from the default.

- **Automatic screen switching: seconds per screen** and the two options
  for switching without spots, see
  [Automatic screen switching](#automatic-screen-switching).
- **Display brightness** for day, night and both screen savers, in percent.
  When you move a slider, the display shows that brightness for a few
  seconds; it is saved only with the Save button. High brightness wears an
  OLED out faster.
- **Turn the display off after some days of Game of Life** (off by default)
  and the number of days (2 by default, 1–30). The Game of Life saver
  otherwise runs until something wakes the display. After that time the
  display turns off, but Game of Life stays the screen saver: the button or
  a spot wakes the display as usual, and the next time the saver starts,
  the days count from zero again.
- **NVIS margin** – how many percent below foF2 the recommended NVIS band
  must lie. The default is 0 % (the band right below foF2); the classic
  optimum working frequency (FOT) is 15 % lower.
- **60 m band** – whether to recommend it for NVIS (yes by default; it
  isn't allowed everywhere).
- **Ionosonde** – an empty field = the nearest ionosonde with a fresh
  measurement within 1500 km of your locator. Or a GIRO station code, for
  example `PQ052` (Průhonice); the codes are on the map at
  [prop.kc2g.com](https://prop.kc2g.com/).
- **Country maps** – add the maps of Czechia, Germany, the United Kingdom
  and the USA to the map views (all off by default), see
  [Screens](#screens).
- **Heltec board version** – detected automatically by default; you can
  also pick V3 / V3.1 or V3.2 by hand (the version is printed on the
  board). It only matters for measuring the battery voltage, because V3.2
  switches the measurement on the other way round.
- **Factory reset**, the red button at the very bottom, erases all
  settings, the Wi-Fi network and password included, and restarts the
  board in setup mode, like a new one. The page asks first. Handy before
  you give the board to someone else.

## Battery and power off

microHAMCLOCK is meant to stay plugged into a charger. The Heltec charges a
Li-ion cell on its battery connector, but never disconnects it when it runs
flat, so a board left running on the battery drains it too deep.

The status screen shows the battery voltage (bottom row, before the
version). It means little on USB or without a cell: without a cell the
board measures the output of its charger instead, usually around 4 V.

**Power off.** A long press on the status screen (triple click, then hold)
powers the board off: the display says so for a moment, then the display,
Wi-Fi and the LoRa radio turn off and the board goes to deep sleep. Only
the **RST** button starts it again (PRG doesn't). Even powered off the
board draws a little, so disconnect the cell for long storage.

## Troubleshooting

- **`WRONG PASSWORD?` or `NETWORK NOT FOUND` on the display.** The board
  can't connect to your Wi-Fi and keeps trying every minute. Hold PRG for
  10 s and enter the correct details. The network must be on 2.4 GHz.
- **The spot list is empty.** That's normal after power-on. Spots appear
  once someone decodes you and their program reports it to PSKReporter.
- **The phone doesn't open the setup page by itself.** Open
  `http://4.3.2.1` by hand; turning off mobile data may help.
- **The flasher doesn't find the board.** Use a cable that carries data. If
  no serial port shows up, install the CP210x driver from Silicon Labs.
  Holding PRG while pressing RST puts the board into flashing mode.
- **The propagation screen says `WAITING FOR DATA`, or foF2 and MUF show
  `--`.** The board hasn't got the data yet, or the server is unreachable;
  it tries again by itself. The status screen shows when the data last
  arrived. foF2 and MUF also show `--` when no ionosonde within 1500 km has
  a fresh measurement, which is common in most of Asia at the moment.

## Serial console

Connect the board over USB and open any serial terminal at 115200 baud.
These commands are handy for users; the console is always in English.

| command    | what it does                                                  |
|------------|---------------------------------------------------------------|
| `setup`    | the step-by-step setup wizard, see [Over USB](#over-usb-serial-console) |
| `status`   | prints the settings, board version, battery voltage, Wi-Fi, time, MQTT, spot count and propagation data |
| `screen`   | shows a screen on the display: `screen clock`, `screen propagation`, `screen list`, `screen map` or `screen status`. Handy when you can't reach the button |
| `saver`    | turns the screen saver on right away: `saver` the one you set, `saver off`, `saver life` or `saver dim` a given one. The settings don't change; the button, or a spot when spots may wake the display, ends it as usual |
| `off`      | powers the board off, like the long press on the status screen |
| `factory`  | factory reset: erases all settings, Wi-Fi included, and restarts in setup mode. It asks first; type `yes` to confirm |

More commands for testing are listed in [development.md](development.md).

## Where the data comes from

microHAMCLOCK only shows data that others kindly make public.

- **PSKReporter** (Philip Gladstone, N1DQ) and its live MQTT feed (Tom
  Fanning, M0LTE) – the reports of who heard you. The feed is live only:
  nothing is kept while the board is off.
- **Ionosonde** – foF2 and MUF(3000) from the nearest GIRO ionosonde that
  has a fresh measurement and is within 1500 km of your locator (in
  Czechia usually Průhonice, PQ052, run by the Institute of Atmospheric
  Physics of the Czech Academy of Sciences). The board picks it
  automatically and stays with it while it isn't much farther than the
  nearest one, so the values don't jump between stations. The data comes
  from [KC2G](https://prop.kc2g.com/) (Andrew Rodland) and is refreshed
  about every 15 minutes. The code of the station in use is on the status
  screen; you can choose a different station in **Advanced**. Fresh data
  is available in Europe, the Americas, South Africa and Australia; in Asia
  there is almost none at the moment.
  The measurements are made by the observatories of the GIRO network (Lowell
  GIRO Data Center, University of Massachusetts Lowell; contacts in its
  [Acknowledgements List](https://giro.uml.edu/didbase/acknowledgements.html))
  and republished by KC2G. GIRO data is released under CC BY-NC-SA 4.0
  ([Rules of the Road](https://giro.uml.edu/didbase/RulesOfTheRoad.html)).
  Source: Reinisch, B. W., and I. A. Galkin, *Global Ionospheric Radio
  Observatory (GIRO)*, Earth, Planets and Space, 63, 377–381 (2011),
  [doi:10.5047/eps.2011.03.001](https://doi.org/10.5047/eps.2011.03.001),
  <http://spase.info/SMWG/Observatory/GIRO>.
- **Propagation** – solar data and band conditions from N0NBH (Paul
  Herrman, [hamqsl.com](https://www.hamqsl.com/solar.html)), refreshed
  about every hour, as N0NBH asks.
- **Time** – `ntp.ufe.cz` (the Institute of Photonics and Electronics of
  the Czech Academy of Sciences, which maintains the Czech national time
  standard), with `tik.cesnet.cz` and `pool.ntp.org` as backups. The board
  synchronizes after connecting to Wi-Fi and then about every hour.
- **Map** – [Natural Earth](https://www.naturalearthdata.com/) (public
  domain).

If a download fails, the board retries after 2 minutes, and each further
failure doubles the wait, up to an hour, so a server outage isn't made
worse by many boards asking at once. The board identifies itself to the
servers as `microHAMCLOCK/<version>` with the project's address.
