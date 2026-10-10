# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Matěj "Wolf" Holyszewski, OK2MTB

"""
Saves a snapshot of the microHAMCLOCK display as a PNG.

Usage:
    python tools/snapshot.py COM4 screen.png [scale]

Sends the "snapshot" command to the board and builds the image from the reply (64 hex rows).
Needs pyserial (part of PlatformIO) and Pillow.
"""
import sys
import time

import serial
from PIL import Image


def main():
    port, out = sys.argv[1], sys.argv[2]
    scale = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    s = serial.Serial(None, 115200, timeout=2)
    s.port = port
    # No DTR/RTS, otherwise the ESP32 resets when the port opens.
    s.dtr = False
    s.rts = False
    s.open()
    with s:
        time.sleep(0.2)
        s.reset_input_buffer()
        s.write(b"snapshot\r\n")
        rows = []
        deadline = time.time() + 5
        started = False
        while len(rows) < 64 and time.time() < deadline:
            line = s.readline().decode("ascii", "replace").strip()
            if line == "SNAPSHOT":
                started = True
            elif started and len(line) == 32:
                rows.append(bytes.fromhex(line))
    if len(rows) < 64:
        sys.exit("the board did not send a complete snapshot")
    img = Image.new("RGB", (128 * scale, 64 * scale))
    px = img.load()
    for y, row in enumerate(rows):
        for x in range(128):
            if row[x >> 3] & (0x80 >> (x & 7)):
                for dy in range(scale):
                    for dx in range(scale):
                        px[x * scale + dx, y * scale + dy] = (140, 220, 255)
    img.save(out)
    print("saved", out)


if __name__ == "__main__":
    main()
