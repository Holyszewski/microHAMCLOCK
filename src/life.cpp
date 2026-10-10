// SPDX-License-Identifier: GPL-3.0-or-later
// Copyright (c) 2026 Matěj "Wolf" Holyszewski, OK2MTB

#include "life.h"

#include <string.h>

namespace {

const int W = 64, H = 32;             // 2×2 px cell
const int HISTORY = 64;               // detects periods up to 64 generations
const uint32_t MAX_GENERATIONS = 2000;

uint8_t gridA[H][W], gridB[H][W];
uint8_t (*cur)[W] = gridA, (*nxt)[W] = gridB;
uint64_t history[HISTORY];
int histLen, histPos;
uint32_t generation, rng = 1;

uint32_t rnd() {                      // xorshift32
  rng ^= rng << 13;
  rng ^= rng >> 17;
  rng ^= rng << 5;
  return rng;
}

uint64_t hashWorld() {                // FNV-1a over the cells
  uint64_t h = 1469598103934665603ULL;
  for (int y = 0; y < H; y++)
    for (int x = 0; x < W; x++) h = (h ^ cur[y][x]) * 1099511628211ULL;
  return h;
}

// Stores a fingerprint of the state; true if the state was seen before (frozen or repeating).
bool repeated() {
  uint64_t h = hashWorld();
  bool seen = false;
  for (int d = 1; d <= histLen && !seen; d++) seen = history[(histPos - d + HISTORY) % HISTORY] == h;
  history[histPos] = h;
  histPos = (histPos + 1) % HISTORY;
  if (histLen < HISTORY) histLen++;
  return seen;
}

void seedSoup() {
  int pct = 25 + rnd() % 21;          // 25–45 % alive
  for (int y = 0; y < H; y++)
    for (int x = 0; x < W; x++) cur[y][x] = (int)(rnd() % 100) < pct;
  generation = 0;
  histLen = histPos = 0;
}

}  // namespace

void lifeReset(uint32_t seed) {
  rng = seed | 1;                     // xorshift must not start from zero
  seedSoup();
}

void lifeStep() {
  uint32_t pop = 0;
  for (int y = 0; y < H; y++) {
    const uint8_t *up = cur[(y + H - 1) % H], *mid = cur[y], *dn = cur[(y + 1) % H];
    for (int x = 0; x < W; x++) {
      int l = (x + W - 1) % W, r = (x + 1) % W;
      int n = up[l] + up[x] + up[r] + mid[l] + mid[r] + dn[l] + dn[x] + dn[r];
      uint8_t alive = n == 3 || (n == 2 && mid[x]);
      nxt[y][x] = alive;
      pop += alive;
    }
  }
  uint8_t (*t)[W] = cur;
  cur = nxt;
  nxt = t;
  generation++;
  if (!pop || repeated() || generation >= MAX_GENERATIONS) seedSoup();
}

void lifeRender(uint8_t *fb) {
  memset(fb, 0, 128 * 64 / 8);
  for (int y = 0; y < H; y++)
    for (int x = 0; x < W; x++) {
      if (!cur[y][x]) continue;
      for (int dy = 0; dy < 2; dy++) {
        int py = y * 2 + dy;
        uint8_t mask = 1 << (py & 7);
        fb[(py >> 3) * 128 + x * 2] |= mask;
        fb[(py >> 3) * 128 + x * 2 + 1] |= mask;
      }
    }
}
