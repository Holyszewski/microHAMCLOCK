# Contributing to microHAMCLOCK

Bug reports, ideas and pull requests are welcome, including new translations.

## Contributor License Agreement

Before a pull request can be merged, you need to agree to the
[Contributor License Agreement](CLA.md) once. You keep the copyright to your work. The CLA allows
the author to publish the project, with your contribution, under other terms besides the GPL, for
example a commercial license. Versions already published under the GPL stay under the GPL.

To agree, add this comment to your pull request:

> I have read the microHAMCLOCK CLA (version 1.0) and I agree to it.

## Pull requests

- Keep code, comments, documentation and commit messages in English.
- Build with `pio run` and, ideally, test on a Heltec WiFi LoRa 32 V3.
- After changing a text catalog in `src/lang/`, run `python tools/check_lang.py`.
- New source files start with the same two lines as the existing ones: the
  `SPDX-License-Identifier: GPL-3.0-or-later` line and the copyright line.
- Mention any code or data you took from elsewhere, with its source and license.

## Translations

The display and the setup page are translated; the serial console is English only. The texts live
in the catalogs `src/lang/<code>.inc`. `en.inc` is the master; a missing translation falls back to
English. To add a language:

1. copy `src/lang/en.inc` to `src/lang/<code>.inc` and translate the texts,
2. add `LANG_<CODE>` to `enum Lang` in `src/i18n.h`,
3. add a row to the `LANGS` table in `src/i18n.cpp`,
4. run `python tools/check_lang.py`. It finds missing texts, `%s`/`%d` placeholders that differ
   from the English ones, and accented characters in display texts.

Display texts (IDs starting with `S_`) must be ASCII, because the OLED font has no accents, and a
line has at most 21 characters. Web texts (`W_`) are UTF-8 and may contain HTML. Keep the
placeholders in the same order as in English.

Building and testing the firmware is described in [docs/development.md](docs/development.md).
