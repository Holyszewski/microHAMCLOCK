// SPDX-License-Identifier: GPL-3.0-or-later
// Copyright (c) 2026 Matěj "Wolf" Holyszewski, OK2MTB

// Game of Life as a screen saver (based on the sibling project "Game of Life").
// No text: just a random soup on a 64×32 torus (2×2 px cells). When the world
// dies out, freezes, starts repeating in a short cycle or runs too long, a new one starts.
#pragma once

#include <stdint.h>

void lifeReset(uint32_t seed);
void lifeStep();
// Draws the world into an SSD1306 128×64 buffer (8 pages of 128 bytes, bit = row).
void lifeRender(uint8_t *fb);
