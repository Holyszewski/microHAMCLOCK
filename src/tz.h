// Time zones for the local time on the display.
//
// A short hand-written list of regions (by city) with DST rules in POSIX TZ
// format, plus fixed offsets UTC−12 … UTC+14. NVS stores the region ID
// (IANA name of the main city, e.g. "Europe/Prague") or "UTC+3".
// The full IANA database would take ~15 KB, so only the most common regions;
// anyone who can't find theirs picks a fixed offset (no DST).
#pragma once

#include <stddef.h>
#include <stdint.h>

struct TzZone {
  const char *id;        // IANA name, stored in NVS
  const char *posix;     // rule for setenv("TZ")
  int16_t offsetMin;     // standard (winter) offset from UTC in minutes
  const char *cities;    // label for the picker, in English
  const char *aliases;   // more IANA names separated by spaces (for detection from the browser)
};

size_t tzZoneCount();
const TzZone &tzZone(size_t i);

// Fixed offsets: "UTC", "UTC+3", "UTC-5" … (whole hours, −12 … +14).
const int TZ_FIXED_MIN = -12, TZ_FIXED_MAX = 14;

// Finds a region or fixed offset by ID or alias (case-insensitive).
// Returns the POSIX rule, or nullptr for an unknown ID. canonical gets the ID to store.
const char *tzPosix(const char *id, char *canonical = nullptr, size_t n = 0);

// Search for the console: exact match, alias, or an unambiguous part of the name or city
// ("prague", "new york"). Returns the number of matches; with a single match it fills id.
int tzSearch(const char *query, char *id, size_t n, void (*listMatch)(const char *id, const char *cities) = nullptr);

// Label for the web page and console, e.g. "UTC+01:00 Prague, Berlin, Paris".
void tzLabel(const TzZone &z, char *out, size_t n);
