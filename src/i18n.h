// SPDX-License-Identifier: GPL-3.0-or-later
// Copyright (c) 2026 Matěj "Wolf" Holyszewski, OK2MTB

// Localization of the texts on the display and on the setup web page.
// The serial console is English only and is not translated.
//
// Texts live in the catalogs src/lang/<code>.inc as TR(ID, "text").
// The English catalog is the master: it defines the list of IDs and serves
// as the fallback when a translation lacks a text. To add a language:
//   1. copy src/lang/en.inc to src/lang/<code>.inc and translate it,
//   2. add LANG_<CODE> to enum Lang below,
//   3. add a row to the LANGS table in i18n.cpp,
//   4. run python tools/check_lang.py.
#pragma once

#include <stddef.h>
#include <stdint.h>
#include <time.h>

enum StrId : uint16_t {
#define TR(id, text) id,
#include "lang/en.inc"
#undef TR
  STR_COUNT
};

// The order must match the LANGS table in i18n.cpp. NVS stores the language code,
// not the number, so the order can change.
enum Lang : uint8_t { LANG_EN, LANG_CS, LANG_COUNT };

struct LangInfo {
  const char *code;        // ISO 639-1, e.g. "en"
  const char *nameAscii;   // name for the console and display (ASCII)
  const char *nameNative;  // name for the web page (UTF-8)
};

const LangInfo &langInfo(Lang l);
bool langFromCode(const char *code, Lang &out);   // case-insensitive
void setLanguage(Lang l);
Lang language();

// Text in the current language.
const char *tr(StrId id);
// Text in the given language (the web page previews the language the user is picking).
const char *tr(StrId id, Lang l);

// Date by the S_DATE_FORMAT pattern: %a weekday, %d day, %m month,
// %b month abbreviation, %Y year, %% percent sign.
size_t formatDate(const struct tm &t, char *out, size_t n);
