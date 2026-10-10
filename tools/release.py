# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Matěj "Wolf" Holyszewski, OK2MTB

"""
Release binaries and the GitHub Release (see Versioning in CLAUDE.md).

Usage:
    python tools/release.py build X.Y.Z
    python tools/release.py publish X.Y.Z

build makes the release build (MICROHAMCLOCK_RELEASE=X.Y.Z) and puts both
distribution binaries in firmware/ (not in git). Run it after renaming the
Unreleased section of CHANGELOG.md to "## X.Y.Z – date".

publish runs after the release commit and the tag vX.Y.Z are pushed. It
creates the GitHub Release for the tag (or updates an existing one), with the
CHANGELOG section as its notes and both binaries attached, and marks it as the
latest release. The asset names never change, so
    https://github.com/<owner>/<repo>/releases/latest/download/<asset>
always serves the newest release; README and the manual link there. Needs the
GitHub CLI (gh), logged in.
"""
import argparse
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, ".pio", "build", "heltec_v3")
MERGED = "heltec_v3_microhamclock-merged.bin"
APP = "heltec_v3_microhamclock.bin"
ASSETS = [MERGED, APP]
PIO_CORE = os.environ.get("PLATFORMIO_CORE_DIR", os.path.join(os.path.expanduser("~"), ".platformio"))
BOOT_APP0 = os.path.join(PIO_CORE, "packages", "framework-arduinoespressif32", "tools", "partitions",
                         "boot_app0.bin")


def fail(msg):
    sys.exit("release: " + msg)


def run(cmd, **kw):
    print("release: " + " ".join(cmd), flush=True)
    try:
        return subprocess.run(cmd, cwd=ROOT, check=True, **kw)
    except OSError as e:
        fail("cannot run %s: %s" % (cmd[0], e))
    except subprocess.CalledProcessError as e:
        fail("%s failed with exit code %d" % (cmd[0], e.returncode))


def changelog_section(version, first):
    """The text under "## X.Y.Z – date" up to the next heading; first: it must be the top one."""
    with open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8") as f:
        text = f.read()
    if first:
        m = re.search(r"^## (.*)$", text, re.M)
        if not m or not m.group(1).startswith(version + " "):
            fail("the first heading in CHANGELOG.md is not version " + version)
    else:
        m = re.search(r"^## " + re.escape(version) + " .*$", text, re.M)
        if not m:
            fail("CHANGELOG.md has no heading for version " + version)
    body = text[m.end():]
    nxt = re.search(r"^## ", body, re.M)
    return (body[:nxt.start()] if nxt else body).strip()


def check_binary(path, version):
    """A release build holds the plain version string; a development one has -N-g<hash> or +N."""
    if not os.path.exists(path):
        fail("%s is missing, run: python tools/release.py build %s" % (path, version))
    with open(path, "rb") as f:
        if (b"\0" + version.encode() + b"\0") not in f.read():
            fail("%s is not a release build of %s, run: python tools/release.py build %s"
                 % (path, version, version))


def check_nvs(path):
    """The merged image must end before NVS (see partitions.csv), or writing it would erase the settings."""
    with open(path, "rb") as f:
        image = f.read()
    for i in range(0x8000, 0x8000 + 0xc00, 32):        # partition table entries
        magic, ptype, subtype, offset, size = struct.unpack("<HBBII", image[i:i + 12])
        if magic != 0x50AA:
            break
        if ptype == 1 and subtype == 2:                 # data, nvs
            if offset < len(image):
                fail("%s reaches into NVS at 0x%x, installing it would erase the settings" % (path, offset))
            return
    fail("%s has no NVS partition in its partition table" % path)


def build(version):
    changelog_section(version, True)
    env = dict(os.environ, MICROHAMCLOCK_RELEASE=version)
    run([sys.executable, "-m", "platformio", "run"], env=env)
    os.makedirs(os.path.join(ROOT, "firmware"), exist_ok=True)
    run([sys.executable, "-m", "platformio", "pkg", "exec", "-p", "tool-esptoolpy", "--",
         "esptool.py", "--chip", "esp32s3", "merge_bin", "-o", os.path.join("firmware", MERGED),
         "--flash_mode", "dio", "--flash_freq", "80m", "--flash_size", "8MB",
         "0x0", os.path.join(BUILD, "bootloader.bin"),
         "0x8000", os.path.join(BUILD, "partitions.bin"),
         "0xe000", BOOT_APP0,
         "0x10000", os.path.join(BUILD, "firmware.bin")])
    shutil.copy(os.path.join(BUILD, "firmware.bin"), os.path.join(ROOT, "firmware", APP))
    for name in ASSETS:
        check_binary(os.path.join(ROOT, "firmware", name), version)
    check_nvs(os.path.join(ROOT, "firmware", MERGED))
    print("release: microHAMCLOCK %s binaries in firmware/" % version)


def publish(version):
    tag = "v" + version
    notes = changelog_section(version, False)
    assets = [os.path.join(ROOT, "firmware", name) for name in ASSETS]
    for path in assets:
        check_binary(path, version)
    check_nvs(assets[0])
    remote = run(["git", "ls-remote", "--tags", "origin", "refs/tags/" + tag],
                 capture_output=True, text=True).stdout.strip()
    if not remote:
        fail("tag %s is not on origin, push it first: git push origin main %s" % (tag, tag))

    notes += ("\n\n### Download\n\n"
              "- `%s`: write it at address `0x0` with any ESP32-S3 flasher, or use the web "
              "installer. An update keeps the settings unless you erase the flash.\n"
              "- `%s`: the application alone, for address `0x10000`.\n" % (MERGED, APP))
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
        f.write(notes)
        notes_file = f.name
    try:
        exists = subprocess.run(["gh", "release", "view", tag], cwd=ROOT,
                                capture_output=True).returncode == 0
        if exists:
            run(["gh", "release", "edit", tag, "--title", "microHAMCLOCK " + version,
                 "--notes-file", notes_file, "--latest"])
            run(["gh", "release", "upload", tag, "--clobber"] + assets)
        else:
            run(["gh", "release", "create", tag, "--verify-tag", "--title", "microHAMCLOCK " + version,
                 "--notes-file", notes_file, "--latest"] + assets)
    finally:
        os.unlink(notes_file)

    url = run(["gh", "repo", "view", "--json", "url", "-q", ".url"],
              capture_output=True, text=True).stdout.strip()
    print("release: published %s/releases/tag/%s" % (url, tag))
    for name in ASSETS:
        print("release: latest  %s/releases/latest/download/%s" % (url, name))


def main():
    ap = argparse.ArgumentParser(description="Build the release binaries or publish the GitHub Release.")
    ap.add_argument("action", choices=["build", "publish"])
    ap.add_argument("version", help="the release number X.Y.Z")
    args = ap.parse_args()
    if not re.fullmatch(r"\d+\.\d+\.\d+", args.version):
        fail("the version must be in the form X.Y.Z")
    if args.action == "build":
        build(args.version)
    else:
        publish(args.version)


if __name__ == "__main__":
    main()
