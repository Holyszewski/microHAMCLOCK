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
