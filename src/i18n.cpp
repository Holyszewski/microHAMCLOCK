// SPDX-License-Identifier: GPL-3.0-or-later
// Copyright (c) 2026 Matěj "Wolf" Holyszewski, OK2MTB

#include "i18n.h"

#include <ctype.h>
#include <stdio.h>
#include <string.h>

namespace {

struct Entry {
  StrId id;
  const char *text;
};

// English exactly in ID order, other languages as ID–text pairs.
const char *const EN_TEXT[STR_COUNT] = {
#define TR(id, text) text,
#include "lang/en.inc"
#undef TR
};

const Entry CS_ENTRIES[] = {
#define TR(id, text) {id, text},
#include "lang/cs.inc"
#undef TR
};

struct LangDef {
  LangInfo info;
  const Entry *entries;             // nullptr = English only
  size_t count;
};

#define ENTRIES(arr) arr, sizeof arr / sizeof arr[0]

const LangDef LANGS[] = {
  {{"en", "English", "English"}, nullptr, 0},
  {{"cs", "Cestina", "Čeština"}, ENTRIES(CS_ENTRIES)},
};
static_assert(sizeof LANGS / sizeof LANGS[0] == LANG_COUNT, "LANGS and enum Lang must have the same number of languages");

// Ready-made tables for all languages (built once). Switching languages is then
// just an index change, so it is safe even at runtime.
const char *table[LANG_COUNT][STR_COUNT];
bool built;
volatile Lang current = LANG_EN;

void build() {
  for (int l = 0; l < LANG_COUNT; l++) {
    memcpy(table[l], EN_TEXT, sizeof EN_TEXT);
    for (size_t i = 0; i < LANGS[l].count; i++) table[l][LANGS[l].entries[i].id] = LANGS[l].entries[i].text;
  }
  built = true;
}

}  // namespace

const LangInfo &langInfo(Lang l) { return LANGS[l < LANG_COUNT ? l : LANG_EN].info; }

bool langFromCode(const char *code, Lang &out) {
  if (!code) return false;
  for (int l = 0; l < LANG_COUNT; l++)
    if (!strcasecmp(code, LANGS[l].info.code)) {
      out = Lang(l);
      return true;
    }
  return false;
}

void setLanguage(Lang l) {
  if (!built) build();
  current = l < LANG_COUNT ? l : LANG_EN;
}

Lang language() { return current; }

const char *tr(StrId id, Lang l) {
  if (!built) build();
  if (id >= STR_COUNT) return "";
  return table[l < LANG_COUNT ? l : LANG_EN][id];
}

const char *tr(StrId id) { return tr(id, current); }

size_t formatDate(const struct tm &t, char *out, size_t n) {
  if (!n) return 0;
  size_t len = 0;
  auto put = [&](const char *s) {
    while (*s && len + 1 < n) out[len++] = *s++;
  };
  char num[8];
  for (const char *p = tr(S_DATE_FORMAT); *p; p++) {
    if (*p != '%' || !p[1]) {
      char c[2] = {*p, 0};
      put(c);
      continue;
    }
    switch (*++p) {
      case 'a': put(tr(StrId(S_DOW_SUN + t.tm_wday % 7))); break;
      case 'b': put(tr(StrId(S_MONTH_JAN + t.tm_mon % 12))); break;
      case 'd': snprintf(num, sizeof num, "%02d", t.tm_mday); put(num); break;
      case 'm': snprintf(num, sizeof num, "%02d", t.tm_mon + 1); put(num); break;
      case 'Y': snprintf(num, sizeof num, "%04d", t.tm_year + 1900); put(num); break;
      default:  { char c[2] = {*p, 0}; put(c); }
    }
  }
  out[len] = 0;
  return len;
}
