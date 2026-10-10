// SPDX-License-Identifier: GPL-3.0-or-later
// Copyright (c) 2026 Matěj "Wolf" Holyszewski, OK2MTB

#include "tz.h"

#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

namespace {

// Sorted by offset. The rules reflect the state in 2026 (Mexico and Iran
// dropped DST, Egypt brought it back, Kazakhstan unified its time at +05).
const TzZone ZONES[] = {
  {"Pacific/Honolulu", "HST10", -600, "Honolulu", ""},
  {"America/Anchorage", "AKST9AKDT,M3.2.0,M11.1.0", -540, "Anchorage", "America/Juneau America/Nome America/Sitka"},
  {"America/Los_Angeles", "PST8PDT,M3.2.0,M11.1.0", -480, "Los Angeles, Seattle, Vancouver",
   "America/Vancouver America/Tijuana"},
  {"America/Phoenix", "MST7", -420, "Phoenix (no DST)", "America/Hermosillo"},
  {"America/Denver", "MST7MDT,M3.2.0,M11.1.0", -420, "Denver, Calgary", "America/Edmonton America/Boise"},
  {"America/Chicago", "CST6CDT,M3.2.0,M11.1.0", -360, "Chicago, Dallas, Winnipeg",
   "America/Winnipeg America/Indiana/Knox America/Menominee America/Matamoros"},
  {"America/Mexico_City", "CST6", -360, "Mexico City, Costa Rica, Guatemala",
   "America/Costa_Rica America/Guatemala America/El_Salvador America/Tegucigalpa America/Managua America/Regina "
   "America/Monterrey America/Merida"},
  {"America/New_York", "EST5EDT,M3.2.0,M11.1.0", -300, "New York, Toronto, Miami",
   "America/Toronto America/Detroit America/Indiana/Indianapolis America/Kentucky/Louisville America/Nassau "
   "America/Montreal"},
  {"America/Bogota", "<-05>5", -300, "Bogota, Lima, Panama", "America/Lima America/Panama America/Guayaquil "
   "America/Cancun America/Jamaica"},
  {"America/Halifax", "AST4ADT,M3.2.0,M11.1.0", -240, "Halifax, Bermuda", "Atlantic/Bermuda America/Moncton"},
  {"America/Caracas", "<-04>4", -240, "Caracas, La Paz, Puerto Rico",
   "America/La_Paz America/Puerto_Rico America/Santo_Domingo America/Manaus America/Barbados"},
  {"America/Santiago", "<-04>4<-03>,M9.1.6/24,M4.1.6/24", -240, "Santiago", ""},
  {"America/St_Johns", "NST3:30NDT,M3.2.0,M11.1.0", -210, "St. John's", ""},
  {"America/Sao_Paulo", "<-03>3", -180, "Sao Paulo, Buenos Aires, Montevideo",
   "America/Argentina/Buenos_Aires America/Buenos_Aires America/Montevideo America/Asuncion America/Recife"},
  {"Atlantic/Azores", "<-01>1<+00>,M3.5.0/0,M10.5.0/1", -60, "Azores", ""},
  {"Etc/UTC", "UTC0", 0, "UTC", "UTC Etc/GMT GMT Etc/Universal"},
  {"Atlantic/Reykjavik", "GMT0", 0, "Reykjavik, Dakar, Accra (no DST)", "Africa/Dakar Africa/Accra Africa/Abidjan"},
  {"Europe/London", "GMT0BST,M3.5.0/1,M10.5.0", 0, "London, Dublin", "Europe/Dublin Europe/Belfast Europe/Guernsey "
   "Europe/Jersey Europe/Isle_of_Man"},
  {"Europe/Lisbon", "WET0WEST,M3.5.0/1,M10.5.0", 0, "Lisbon, Canary Islands",
   "Atlantic/Canary Atlantic/Madeira Atlantic/Faroe"},
  {"Africa/Lagos", "WAT-1", 60, "Lagos, Kinshasa (no DST)", "Africa/Kinshasa Africa/Luanda Africa/Douala"},
  {"Europe/Prague", "CET-1CEST,M3.5.0,M10.5.0/3", 60, "Prague, Berlin, Paris, Rome, Madrid, Warsaw",
   "Europe/Bratislava Europe/Berlin Europe/Vienna Europe/Paris Europe/Rome Europe/Madrid Europe/Warsaw "
   "Europe/Budapest Europe/Amsterdam Europe/Brussels Europe/Luxembourg Europe/Zurich Europe/Stockholm Europe/Oslo "
   "Europe/Copenhagen Europe/Ljubljana Europe/Zagreb Europe/Belgrade Europe/Sarajevo Europe/Skopje "
   "Europe/Podgorica Europe/Tirane Europe/Malta Europe/Monaco Europe/Andorra Europe/Vaduz Europe/San_Marino "
   "Europe/Vatican Europe/Gibraltar Europe/Busingen Africa/Ceuta Arctic/Longyearbyen"},
  {"Africa/Johannesburg", "SAST-2", 120, "Johannesburg, Harare (no DST)", "Africa/Harare Africa/Maputo Africa/Lusaka"},
  {"Africa/Cairo", "EET-2EEST,M4.5.5/0,M10.5.4/24", 120, "Cairo", ""},
  {"Europe/Athens", "EET-2EEST,M3.5.0/3,M10.5.0/4", 120, "Athens, Helsinki, Kyiv, Bucharest, Sofia",
   "Europe/Helsinki Europe/Kiev Europe/Kyiv Europe/Bucharest Europe/Sofia Europe/Riga Europe/Tallinn "
   "Europe/Vilnius Asia/Nicosia Europe/Nicosia Europe/Mariehamn"},
  {"Asia/Jerusalem", "IST-2IDT,M3.4.4/26,M10.5.0", 120, "Jerusalem", "Asia/Tel_Aviv"},
  {"Europe/Istanbul", "<+03>-3", 180, "Istanbul, Riyadh, Minsk, Amman",
   "Asia/Istanbul Asia/Riyadh Asia/Baghdad Asia/Kuwait Asia/Qatar Asia/Bahrain Asia/Aden Asia/Amman "
   "Asia/Damascus Europe/Minsk"},
  {"Europe/Moscow", "MSK-3", 180, "Moscow, St. Petersburg", "Europe/Simferopol Europe/Kirov Europe/Volgograd"},
  {"Africa/Nairobi", "EAT-3", 180, "Nairobi, Addis Ababa", "Africa/Addis_Ababa Africa/Dar_es_Salaam "
   "Africa/Kampala Africa/Mogadishu"},
  {"Asia/Tehran", "<+0330>-3:30", 210, "Tehran", ""},
  {"Asia/Dubai", "<+04>-4", 240, "Dubai, Baku, Tbilisi, Yerevan", "Asia/Muscat Asia/Baku Asia/Tbilisi "
   "Asia/Yerevan Europe/Samara Indian/Mauritius"},
  {"Asia/Kabul", "<+0430>-4:30", 270, "Kabul", ""},
  {"Asia/Karachi", "PKT-5", 300, "Karachi", ""},
  {"Asia/Tashkent", "<+05>-5", 300, "Tashkent, Almaty, Yekaterinburg",
   "Asia/Almaty Asia/Yekaterinburg Indian/Maldives Asia/Dushanbe Asia/Ashgabat Asia/Samarkand"},
  {"Asia/Kolkata", "IST-5:30", 330, "India, Sri Lanka", "Asia/Calcutta Asia/Colombo"},
  {"Asia/Kathmandu", "<+0545>-5:45", 345, "Kathmandu", "Asia/Katmandu"},
  {"Asia/Dhaka", "<+06>-6", 360, "Dhaka, Bishkek, Omsk", "Asia/Bishkek Asia/Omsk Asia/Thimphu"},
  {"Asia/Yangon", "<+0630>-6:30", 390, "Yangon", "Asia/Rangoon"},
  {"Asia/Bangkok", "<+07>-7", 420, "Bangkok, Hanoi, Jakarta, Novosibirsk",
   "Asia/Ho_Chi_Minh Asia/Saigon Asia/Jakarta Asia/Phnom_Penh Asia/Vientiane Asia/Novosibirsk Asia/Krasnoyarsk"},
  {"Asia/Shanghai", "CST-8", 480, "Beijing, Shanghai, Taipei", "Asia/Chongqing Asia/Taipei Asia/Macau"},
  {"Asia/Singapore", "<+08>-8", 480, "Singapore, Hong Kong, Manila, Perth",
   "Asia/Kuala_Lumpur Asia/Manila Australia/Perth Asia/Hong_Kong Asia/Irkutsk Asia/Makassar Asia/Brunei"},
  {"Asia/Tokyo", "JST-9", 540, "Tokyo, Seoul", "Asia/Seoul Asia/Pyongyang Asia/Yakutsk Asia/Jayapura Pacific/Palau"},
  {"Australia/Darwin", "ACST-9:30", 570, "Darwin (no DST)", ""},
  {"Australia/Adelaide", "ACST-9:30ACDT,M10.1.0,M4.1.0/3", 570, "Adelaide", "Australia/Broken_Hill"},
  {"Australia/Brisbane", "AEST-10", 600, "Brisbane, Guam, Vladivostok (no DST)",
   "Australia/Lindeman Pacific/Guam Pacific/Port_Moresby Asia/Vladivostok"},
  {"Australia/Sydney", "AEST-10AEDT,M10.1.0,M4.1.0/3", 600, "Sydney, Melbourne, Hobart",
   "Australia/Melbourne Australia/Canberra Australia/Hobart Australia/ACT Australia/NSW Australia/Victoria "
   "Australia/Tasmania"},
  {"Pacific/Noumea", "<+11>-11", 660, "Noumea, Solomon Islands, Magadan",
   "Pacific/Guadalcanal Asia/Magadan Asia/Sakhalin Pacific/Bougainville"},
  {"Pacific/Auckland", "NZST-12NZDT,M9.5.0,M4.1.0/3", 720, "Auckland, Wellington", "Antarctica/McMurdo"},
  {"Pacific/Fiji", "<+12>-12", 720, "Fiji, Kamchatka", "Asia/Kamchatka Pacific/Majuro Pacific/Tarawa"},
  {"Pacific/Tongatapu", "<+13>-13", 780, "Tonga, Samoa", "Pacific/Apia"},
};
const size_t ZONE_COUNT = sizeof ZONES / sizeof ZONES[0];

bool hasWord(const char *list, const char *word) {   // is word in the space-separated list?
  size_t n = strlen(word);
  for (const char *p = list; *p;) {
    while (*p == ' ') p++;
    size_t len = strcspn(p, " ");
    if (len == n && !strncasecmp(p, word, n)) return true;
    p += len;
  }
  return false;
}

bool containsNoCase(const char *hay, const char *needle) {
  size_t n = strlen(needle);
  for (; *hay; hay++)
    if (!strncasecmp(hay, needle, n)) return true;
  return false;
}

// "UTC", "UTC+3", "utc-5" → offset in hours; false if it isn't a fixed offset.
bool parseFixed(const char *id, int &hours) {
  if (strncasecmp(id, "UTC", 3)) return false;
  const char *p = id + 3;
  if (!*p) { hours = 0; return true; }
  if (*p != '+' && *p != '-') return false;
  char *end;
  long h = strtol(p, &end, 10);
  if (*end || end == p + 1 || h < TZ_FIXED_MIN || h > TZ_FIXED_MAX) return false;
  hours = (int)h;
  return true;
}

}  // namespace

size_t tzZoneCount() { return ZONE_COUNT; }
const TzZone &tzZone(size_t i) { return ZONES[i < ZONE_COUNT ? i : 0]; }

const char *tzPosix(const char *id, char *canonical, size_t n) {
  if (!id || !*id) return nullptr;
  int hours;
  if (parseFixed(id, hours)) {
    // POSIX has the opposite sign: UTC+3 = "<+03>-3".
    static char buf[16];
    if (hours) snprintf(buf, sizeof buf, "<%+03d>%d", hours, -hours);
    else       strcpy(buf, "UTC0");
    if (canonical) {
      if (hours) snprintf(canonical, n, "UTC%+d", hours);
      else       snprintf(canonical, n, "UTC");
    }
    return buf;
  }
  for (const TzZone &z : ZONES)
    if (!strcasecmp(id, z.id) || hasWord(z.aliases, id)) {
      if (canonical) snprintf(canonical, n, "%s", z.id);
      return z.posix;
    }
  return nullptr;
}

int tzSearch(const char *query, char *id, size_t n, void (*listMatch)(const char *, const char *)) {
  if (tzPosix(query, id, n)) return 1;               // exact ID, alias or UTC±x
  // Spaces in the query match underscores in IANA names ("new york" → New_York).
  char q[48];
  size_t k = 0;
  for (const char *p = query; *p && k + 1 < sizeof q; p++) q[k++] = *p == ' ' ? '_' : *p;
  q[k] = 0;
  int found = 0;
  for (const TzZone &z : ZONES) {
    if (!containsNoCase(z.id, q) && !containsNoCase(z.aliases, q) && !containsNoCase(z.cities, query)) continue;
    if (!found && id) snprintf(id, n, "%s", z.id);
    found++;
    if (listMatch) listMatch(z.id, z.cities);
  }
  return found;
}

void tzLabel(const TzZone &z, char *out, size_t n) {
  int m = z.offsetMin < 0 ? -z.offsetMin : z.offsetMin;
  snprintf(out, n, "UTC%c%02d:%02d %s", z.offsetMin < 0 ? '-' : '+', m / 60, m % 60, z.cities);
}
