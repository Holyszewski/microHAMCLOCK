"""
Checks the text catalogs in src/lang/*.inc against the master src/lang/en.inc.

Usage:
    python tools/check_lang.py

Reports:
  - errors (exit code 1): IDs unknown to English, IDs listed twice,
    printf placeholders that differ from English (%s, %d …), non-ASCII
    characters in display texts (S_…),
  - warnings: missing translations (English is used), display texts
    longer than a line (21 characters).
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANG_DIR = os.path.join(HERE, "..", "src", "lang")
LINE = re.compile(r'^\s*TR\(\s*(\w+)\s*,\s*((?:"(?:[^"\\]|\\.)*"\s*)+)\)\s*$')
LITERAL = re.compile(r'"((?:[^"\\]|\\.)*)"')
SPEC = re.compile(r"%(?:%|[-+ 0#]*\d*(?:\.\d+)?(?:hh|h|ll|l|z)?[diouxXcsfeEgGp])")
OLED_CHARS = 21


def parse(path):
    entries, errors = [], []
    with open(path, encoding="utf-8") as f:
        for no, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith("//"):
                continue
            m = LINE.match(line)
            if not m:
                errors.append(f"{os.path.basename(path)}:{no}: cannot parse line: {line}")
                continue
            text = "".join(LITERAL.findall(m.group(2)))
            text = text.encode("utf-8").decode("unicode_escape").encode("latin-1").decode("utf-8")
            entries.append((no, m.group(1), text))
    return entries, errors


def specs(text):
    return [s for s in SPEC.findall(text) if s != "%%"]


def main():
    errors, warnings = [], []
    master, errs = parse(os.path.join(LANG_DIR, "en.inc"))
    errors += errs
    en = {}
    for no, sid, text in master:
        if sid in en:
            errors.append(f"en.inc:{no}: {sid} is listed twice")
        en[sid] = text

    for path in sorted(glob.glob(os.path.join(LANG_DIR, "*.inc"))):
        name = os.path.basename(path)
        entries, errs = parse(path) if name != "en.inc" else (master, [])
        errors += errs
        seen = set()
        for no, sid, text in entries:
            where = f"{name}:{no}: {sid}"
            if name != "en.inc":
                if sid not in en:
                    errors.append(f"{where} is unknown to English")
                    continue
                if sid in seen:
                    errors.append(f"{where} is listed twice")
                if specs(text) != specs(en[sid]):
                    errors.append(f"{where} has placeholders {specs(text)}, English has {specs(en[sid])}")
            seen.add(sid)
            if sid.startswith("S_"):
                if not text.isascii():
                    errors.append(f"{where} contains non-ASCII characters (the display can't show them)")
                # estimated length after substitution: placeholder ~ 2 characters
                if len(SPEC.sub("xx", text)) > OLED_CHARS:
                    warnings.append(f"{where} may be longer than a display line ({OLED_CHARS} characters)")
        if name != "en.inc":
            missing = [sid for sid in en if sid not in seen]
            for sid in missing:
                warnings.append(f"{name}: missing {sid} (English is used)")
        print(f"{name}: {len(entries)} texts")

    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("ERROR:", e)
    if not errors:
        print("OK" if not warnings else "OK, warnings only")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
