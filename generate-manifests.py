#!/usr/bin/env python3
"""
generate-manifests.py

Scans every subfolder of images/ and (re)generates a manifest.json listing
all image files found there — regardless of filename. The site's JavaScript
reads these manifest.json files at runtime instead of having filenames
hardcoded in index.html, so adding or removing a photo is as simple as:

  1. Drop the image file into the right folder (images/hero,
     images/philosophy, images/collections, images/portfolio,
     images/instagram).
  2. Run:  python3 generate-manifests.py
  3. Commit + push. Done — no HTML edits needed.

If a manifest.json already exists for a folder, this script preserves any
hand-edited "alt", "sk", and "en" fields for files it already knows about,
and only adds fresh (generic) entries for new files. Removed files are
dropped automatically.

Every subfolder of images/ is discovered automatically — there is no
hardcoded folder list. Creating a brand new folder (e.g. images/press/)
and dropping photos into it is enough; running this script will generate
a manifest.json for it too. The site's JavaScript, however, only fetches
the specific folders it has sections for (hero, philosophy, collections,
portfolio, instagram) — see index.html if you add a new gallery section
and need it wired up.

Usage:
    python3 generate-manifests.py
"""

import json
import os

IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
VALID_EXT = (".jpg", ".jpeg", ".png", ".webp", ".avif")


def discover_folders():
    """Return every subfolder of images/ — no hardcoded names."""
    if not os.path.isdir(IMAGES_DIR):
        return []
    return sorted(
        f for f in os.listdir(IMAGES_DIR)
        if os.path.isdir(os.path.join(IMAGES_DIR, f))
    )


def load_existing(manifest_path):
    if not os.path.exists(manifest_path):
        return {}
    try:
        with open(manifest_path, encoding="utf-8") as f:
            data = json.load(f)
        return {item["file"]: item for item in data.get("images", [])}
    except (json.JSONDecodeError, KeyError):
        return {}


def humanize(filename):
    name = os.path.splitext(filename)[0]
    name = name.replace("-", " ").replace("_", " ").strip()
    return name[:1].upper() + name[1:] if name else "Leroy Diamonds jewelry"


def generate_for_folder(folder):
    folder_path = os.path.join(IMAGES_DIR, folder)
    if not os.path.isdir(folder_path):
        print(f"skip: {folder_path} does not exist")
        return

    manifest_path = os.path.join(folder_path, "manifest.json")
    existing = load_existing(manifest_path)

    files = sorted(
        f for f in os.listdir(folder_path)
        if f.lower().endswith(VALID_EXT)
    )

    images = []
    for f in files:
        if f in existing:
            images.append(existing[f])
        else:
            label = humanize(f)
            images.append({
                "file": f,
                "alt": f"Leroy Diamonds — {label}",
                "sk": label,
                "en": label,
            })

    with open(manifest_path, "w", encoding="utf-8") as out:
        json.dump({"images": images}, out, ensure_ascii=False, indent=2)
        out.write("\n")

    print(f"{folder}/manifest.json — {len(images)} image(s)")


if __name__ == "__main__":
    folders = discover_folders()
    if not folders:
        print(f"No subfolders found in {IMAGES_DIR} — nothing to do.")
    for folder in folders:
        generate_for_folder(folder)
