# Changelog

Versions are numbered `0.x.y` while the project is unfinished: `x` goes
up with a new feature, `y` with a fix. Each version has a git tag
`vX.Y.Z`. The number changes only at a release; changes between
releases are listed in the Unreleased section.

## Unreleased

- Docs: the manual is now for users only, reordered (installing, setup,
  screens, controls, settings, troubleshooting) and with a troubleshooting
  section. Building from source and the inner workings moved to the new
  `docs/development.md`, adding a language to `CONTRIBUTING.md`.

## 0.12.0 – 2026-10-14

- New: the battery voltage (for example `4.20V`) is shown on the status
  screen, bottom row, one space before the version. It is not shown without
  a cell. A long development version (`v0.11.12+13`) may overlap `NTP OK`.
- New: the console command `screen clock|propagation|list|map|status` shows
  a screen on the display, for a board you can't reach to press its button.

## 0.11.3 – 2026-10-12

- Small tweak to the spot list display.

## 0.11.2 – 2026-10-12

- Fix: on the map a new, blinking spot could be hidden under an older one
  nearby (or the same station on another band). The spots were drawn from
  the last memory slot to the first, and a new spot usually takes the last
  one, so it was drawn first and the older ones covered it; now they are
  drawn by arrival time, the newest on top.

## 0.11.1 – 2026-10-11

- Docs: README and the manual say that microHAMCLOCK is meant mainly for
  stationary use, plugged into a USB charger all the time, with or without
  a battery.

## 0.11.0 – 2026-10-11

- Docs: README and the manual now acknowledge the GIRO network and its
  observatories as the ionosonde data asks (citation, link, license).
- Changed: without any spot in the last hour, automatic screen switching
  skips the empty spot list: it goes between the clock, the propagation
  screen and the map (the world with day and night, shown for 5 seconds
  only). The spot list is still reached with the button. As soon as a spot
  comes in, all four screens rotate again.
- Changed: with the screen saver on and no spots, the first button press
  wakes the display on the clock.
- Changed: in the "dark" night mode a button press lights the display again
  (until the screen saver time runs out), while new spots still don't.
  Before, the button did nothing at night in that mode.
- Added: Advanced option "without spots, switch the map too" (on by default);
  turn it off to keep just the clock and the propagation screen when there
  are no spots.
- Added: Advanced option "without spots, switch all screens too" (off by
  default) keeps all four screens in rotation even with no spots.
- Changed: the ionosonde data (KC2G) is downloaded every 15 minutes, not
  every 10, which halves its load on the server; the data stays well inside
  the 90-minute limit.
- Changed: a failed download (propagation or ionosonde) is retried after
  2 minutes and each further failure doubles the wait, up to an hour. Before,
  every board retried every 2 minutes, so an outage was hit by all of them.
- Changed: the propagation data (hamqsl.com) is downloaded once an hour, not
  every 30 minutes, as its operator asks.
- Changed: refresh times and MQTT reconnects have a random spread of ±10 %,
  and the first downloads after Wi-Fi comes up fall within a minute, so boards
  that start together (after a power cut, say) do not all ask at once.
- Changed: the data downloads identify the board and the project in the
  User-Agent header (`microHAMCLOCK/<version>`), so the servers can tell who
  is asking and get in touch.

## 0.10.1 – 2026-10-10

- Fix: the setup hotspot page listed no Wi-Fi networks. With the hotspot
  on, a scan takes about 8 s, but the Arduino core gave up after 6 s and
  the late result was thrown away. The board now waits for it, repeats
  an empty scan up to twice, and the page fills in the list by itself
  when the scan is done (also after **Search for networks again**),
  without a reload, so nothing typed is lost. It says when no network
  was found.

## 0.10.0 – 2026-10-10

- README and the manual link straight to the firmware of the latest
  release, and `tools/release.py` builds the release binaries and
  publishes the GitHub Release.
- Fix: the web installer page linked to the repository with the git
  user name in the address.
- Fix: installing a new version with the web installer or a flasher
  erased the settings, even without choosing to erase the device,
  because the firmware image also covered the settings area. The
  settings now live at the end of the flash memory, out of the image's
  reach. Boards set up before have to be set up once more after this
  update.
- Factory reset: a button at the bottom of Advanced on the setup page
  and the `factory` console command erase all settings, Wi-Fi included,
  and restart in setup mode.
- Power off: a long press on the status screen or the `off` console
  command turns the display, Wi-Fi and the LoRa radio off and puts the
  board into deep sleep; the RST button starts it again. For running on
  a battery, which the board never disconnects when it is flat.
- Battery voltage measurement, printed by `status`, and a Heltec board
  version setting (automatic by default, or V3 / V3.1 or V3.2) at the
  bottom of Advanced, because V3.2 switches the measurement on the other
  way round. An automatic power off on a flat battery is prepared in the
  code but switched off.
- German language on the display and the setup page.
- Map: new Germany and UK (border outline, like Czechia) and USA (the 48
  contiguous states, with day and night) views. They and the Czechia view
  are now switched on
  in Advanced on the setup page, each off by default, so the long press
  and AUTO only use the countries you want. Czechia has to be switched
  on again on boards that used it. AUTO allows one pixel around the
  border, so coastal stations count as inside the country.
- Fix: spot times from PSKReporter and ionosonde measurement times were
  read through signed 32-bit numbers that overflow in January 2038. The
  system clock itself is still 32-bit on the current Arduino core.
- Fix: foF2 and MUF on the propagation screen could stay `--` for hours.
  The KC2G parser found records by their first key (`"source"`), but
  KC2G changes the key order of its records, so after such a change no
  ionosonde was read. Records are now found by their braces.
- License changed from MIT to GPL-3.0-or-later, copyright Matěj "Wolf"
  Holyszewski, OK2MTB. Source files carry an SPDX header.
- Contributor License Agreement (`CLA.md`), `CONTRIBUTING.md` and a
  pull request template.
- The Game of Life screen saver can turn the display off after a set
  number of days (Advanced on the web: off by default, 2 days when
  ticked, 1–30). Game of Life stays the saver, waking works as before.
  `status` shows it.

## 0.9.1 – 2026-10-10

- Fix: automatic screen rotation could be switched only by a double
  click. The setup page now has a checkbox for it, and the seconds per
  screen (15 by default, 5–120) are in Advanced. `status` shows it.

## 0.9.0 – 2026-10-10

- The project is now called **microHAMCLOCK**, a tribute to HamClock by
  WB0OEW. The boot screen shows MICRO and a big HAMCLOCK, the hotspot is
  `MICROHAMCLOCK-xxxx`, the binaries are `heltec_v3_microhamclock*.bin`.
  Settings are stored under the new name, so a board set up before has
  to be set up again.
- README: a recommended 3D-printed case (Bender Battery Case for the
  Heltec V3 by zerofox3D on Printables).

## 0.8.0 – 2026-10-10

- New console command `saver` turns the screen saver on right away:
  `saver` the one you set, `saver off`, `saver life` or `saver dim`
  a given one. Settings don't change; the button or a spot ends it.

## 0.7.0 – 2026-10-10

- Fix: right after start the display said "WRONG PASSWORD?" although the
  board then connected; the first attempt after a restart often fails.
  A Wi-Fi error is now shown only after 20 s without a connection.
- Fix: the status screen showed "SOLAR OK" instead of the time when the
  solar data arrived before the clock was set.
- Fix: on the Czech status screen the solar and ionosonde times overlapped
  ("SIRENI 23:49" and "IONO 23:40" didn't fit on one line). Both
  languages now use the labels SOLAR and IONO.
- New defaults: the LED flashes when a spot wakes the display, and spots
  wake the display at night too. Boards that already have these settings
  saved keep them.
- The web installer can now set up the board too: after installing, press
  Connect, pick your Wi-Fi from a scanned list, enter the password,
  callsign and locator, and save. The page then shows the board
  connecting to Wi-Fi, getting the time and listening for spots. It has a
  Disconnect button that releases the serial port.
- Fix: in the web installer's console (ESP Web Tools) the setup wizard's
  questions stayed hidden until answered, so it was easy to answer the
  previous question: the Wi-Fi password could end up as the callsign.
  Each question now ends its line and the answer goes below it.
- Repository translated to English: code comments, tool messages, manual
  and changelog. `src/mapa.h` renamed to `src/maps.h`, `tools/snimek.py`
  to `tools/snapshot.py`.
- Firmware binaries are no longer kept in the repository; they are
  attached to GitHub Releases.
- One-click web installer (`web/index.html`, ESP Web Tools): flash
  HamClock from Chrome or Edge without any tools. `tools/build_site.py`
  builds the site for GitHub Pages and can serve it locally.
- The README is a new English front page for GitHub with screen images
  (`tools/readme_screens.py`). The full manual is in `docs/manual.md`.
- Map mode constants renamed to English (`MM_WORLD`, `MM_EUROPE`,
  `MM_CZECHIA`); the stored setting is unchanged.
- MIT license (file `LICENSE`, still to be confirmed before publishing).
- Web: clearer wording of the LED option ("briefly flash the LED when
  a spot wakes the display"). The option is indented under waking on
  a spot and greys out without it; the stored value doesn't change.

## 0.6.0 – 2026-10-10

- The ionosonde is no longer hardwired to Průhonice: the nearest one to
  the locator with a fresh measurement within 1500 km is used, or the
  one whose GIRO code you enter under Advanced. The status screen shows
  the station code, `status` also its name and distance.
- The propagation screen shows the recommended NVIS band based on foF2
  (e.g. `NVIS80`). Under Advanced you can set a margin below foF2
  (default 0 %) and turn off the 60 m band.
- The propagation screen briefly inverts when new data arrives. The
  `blink` command in the serial console shows it without waiting for
  data.
- Fix: after a long press at night in "dark" mode, a swallowed press
  stayed pending, so in the morning the first press did nothing and
  a spot wake didn't switch to the list or flash the LED (bug since
  0.5.0).
- New Advanced section on the web: display brightness separately for
  day, night, the "dim and shift" screen saver and the Game of Life
  screen saver (1–100 %). Moving a slider shows the brightness on the
  display right away. Defaults are the same as before.
- The version number changes only at a release. A development build
  reports itself from git, e.g. `0.5.1-3-g1a2b3c4` (3 commits after
  0.5.1), shown on the display as `v0.5.1+3`.
- README: HamClock isn't listed in the MeshCore flasher; the file is
  picked from the computer.

## 0.5.1 – 2026-10-09

- A long press is now detected only while the button is held. Removed
  the old fallback branch that in rare cases fired it only on release.

## 0.5.0 – 2026-10-09

- A long press switches the map or list sorting after just 0.7 s of
  holding, only once. Releasing triggers no further action. Holding on
  opens setup after 10 s; the switch along the way is intentional.
- Optional half-second flash of the built-in LED when a new spot wakes
  the screen saver. Off by default, configurable on the web and in the
  USB console, stored in NVS. It doesn't flash when the display is
  already awake or when woken by the button, and respects night mode.

## 0.4.0 – 2026-10-09

- The time zone can be chosen. It's a list of about 50 regions by city
  with daylight saving time (`src/tz.cpp`), plus fixed offsets UTC−12
  to UTC+14.
  - On the web, the zone is preselected from the phone at first setup.
  - In the console, typing part of a city name is enough, e.g. `prague`.
  - A board configured in an older version keeps CET/CEST, a new one
    starts in UTC.
- Screen saver (by default after 10 min of inactivity). It can turn the
  display off (default), run Game of Life, or dim and shift the picture.
  - A new spot (younger than 15 min) counts as activity and wakes the
    display on the spot list.
  - The first button press only wakes the display; holding 10 s for
    setup always works.
- Configurable night (default 22–06): the display is dimmed and only the
  button wakes it, optionally spots too, or it stays off.
- The hotspot screen shows `WEB IP 4.3.2.1`; the empty spot list
  encourages transmitting in general (not just FT8).
- The spot list always starts at the first page when opened.

## 0.3.0 – 2026-10-09

- Display and setup page in English (default) or Czech. The language is
  chosen on the web (first form field, the page switches immediately)
  or in the console as the wizard's first question. It is stored as
  a code (`en`, `cs`).
- Texts are in the catalogs `src/lang/*.inc`; a missing translation
  falls back to English. `tools/check_lang.py` checks missing texts,
  parameters and diacritics on the display. New language = new catalog
  and one line.
- Date on the clock depends on the language (`FRI 09 OCT 2026` /
  `PA 09.10.2026`).
- The serial console is entirely in English. Commands `status` and
  `snapshot`; the original `stav` and `snimek` still work, `cancel`
  exits the wizard.
- The console wizard checks the Wi-Fi password length (8 to 63
  characters) like the web.
- Fixed: the Wi-Fi failure reason was overwritten with a generic
  "connecting" after a new connection attempt.

## 0.2.1 – 2026-10-09

- The hotspot has the address `http://4.3.2.1` instead of 192.168.4.1.
  Newer Android marked a network with a private address as "no
  internet" right away and didn't offer the sign-in page; now it shows
  "Sign in to network".
- The hotspot DHCP sends a DNS server, and our own DNS answers all names
  (including queries with EDNS).
- When Wi-Fi fails to connect, the display shows why: `WRONG PASSWORD?`
  or `NETWORK NOT FOUND`, and the board retries every minute (the core
  doesn't reconnect by itself after some errors).
- In config mode the console logs phone connections and the assigned
  address, without the core's error messages for every unknown page.

## 0.2.0 – 2026-10-09

- Config mode via hotspot: open Wi-Fi `HAMCLOCK-xxxx` with a form at
  `http://192.168.4.1` (network picked from a list, password, callsign,
  locator). The phone usually opens the page by itself.
- The hotspot starts by itself only on an unconfigured board, otherwise
  by holding the button for 10 s, even while waiting for Wi-Fi after
  boot. A countdown shows while holding. Stored values are not erased
  and leaving without saving changes nothing.
- A configured board returns from the hotspot to normal operation by
  itself after 10 minutes of inactivity or after a power cycle.
- A long press (list sorting, map view) is evaluated only on button
  release, so the 10 s hold doesn't switch it.
- The version number is shown after boot, on the status screen, in the
  `stav` command and on the setup page.

## 0.1.0 – 2026-10-09

First version.

- Screens CLOCK, PROPAGATION, PSK LIST and PSK MAP, rotating every 15 s.
- PSKReporter via MQTT: who heard me in the last hour, callsign in its
  base form and with `/P` and `/M`.
- Propagation from hamqsl.com (N0NBH), foF2 and MUF(3000) from the
  Průhonice ionosonde (PQ052) via KC2G.
- Maps of the world with the grey line, of Europe and of Czechia. AUTO
  mode picks the view from the spots.
- Time from NTP (`ntp.ufe.cz`), CET/CEST time zone, display dimmed at
  night.
- Setup via the serial console with the `setup` command, stored in NVS.
