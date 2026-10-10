"""
Builds the web installer site into site/ (not in git).

Usage:
    python tools/build_site.py [--repo URL] [--serve [PORT]]

The site is web/index.html plus manifest.json for ESP Web Tools, the merged
firmware from firmware/ (made at a release, see CLAUDE.md) and the README
screen images. The version comes from the first "## X.Y.Z" heading in
CHANGELOG.md that is a real version. Publish the contents of site/ on GitHub
Pages; ESP Web Tools needs the firmware on the same site (CORS).

--serve starts a local web server (default port 8000). Browsers allow the
installer on http://localhost, so it can be tested before publishing.
"""
import argparse
import functools
import http.server
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
FIRMWARE = "heltec_v3_microhamclock-merged.bin"


def release_version():
    with open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8") as f:
        for line in f:
            m = re.match(r"## (\d+\.\d+\.\d+) ", line)
            if m:
                return m.group(1)
    sys.exit("build_site: no version heading in CHANGELOG.md")


def repo_url():
    try:
        url = subprocess.run(["git", "remote", "get-url", "origin"], cwd=ROOT, capture_output=True,
                             text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "#"
    if url.startswith("git@github.com:"):
        url = "https://github.com/" + url[len("git@github.com:"):]
    return url[:-4] if url.endswith(".git") else url


def main():
    ap = argparse.ArgumentParser(description="Build the web installer site into site/.")
    ap.add_argument("--repo", help="link to the GitHub repository (default: git remote origin)")
    ap.add_argument("--serve", nargs="?", const=8000, type=int, metavar="PORT",
                    help="serve site/ on http://localhost:PORT after building")
    args = ap.parse_args()

    firmware = os.path.join(ROOT, "firmware", FIRMWARE)
    if not os.path.exists(firmware):
        sys.exit("build_site: %s is missing, make a release build first (see CLAUDE.md)" % firmware)
    version = release_version()

    shutil.rmtree(SITE, ignore_errors=True)
    os.makedirs(os.path.join(SITE, "img"))
    with open(os.path.join(ROOT, "web", "index.html"), encoding="utf-8") as f:
        page = f.read()
    page = page.replace("{{VERSION}}", version).replace("{{REPO_URL}}", args.repo or repo_url())
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    manifest = {
        "name": "microHAMCLOCK",
        "version": version,
        "new_install_prompt_erase": True,
        "builds": [{"chipFamily": "ESP32-S3", "parts": [{"path": FIRMWARE, "offset": 0}]}],
    }
    with open(os.path.join(SITE, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    shutil.copy(firmware, SITE)
    shutil.copy(os.path.join(ROOT, "docs", "img", "demo.png"), os.path.join(SITE, "img"))
    print("build_site: microHAMCLOCK %s in %s" % (version, SITE))

    if args.serve:
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=SITE)
        print("build_site: serving on http://localhost:%d (Ctrl+C to stop)" % args.serve)
        http.server.ThreadingHTTPServer(("127.0.0.1", args.serve), handler).serve_forever()


if __name__ == "__main__":
    main()
