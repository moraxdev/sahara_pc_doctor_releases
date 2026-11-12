#!/usr/bin/env python3
"""Adds a Windows build to the update feed.
  publish.py windows <Sahara-PC-Doctor.exe> <build> <version> --key update-key.pem [--force] [--min N] [--notes TEXT]
--force blocks every older version until it updates; --min N blocks only builds below N.
"""
import argparse, json, os, shutil
BASE = "https://raw.githubusercontent.com/moraxdev/sahara_pc_doctor_releases/main/"
a = argparse.ArgumentParser()
a.add_argument("platform", choices=["windows"]); a.add_argument("file"); a.add_argument("number", type=int); a.add_argument("version")
a.add_argument("--key", required=True); a.add_argument("--force", action="store_true"); a.add_argument("--min", type=int, default=0); a.add_argument("--notes", default="")
o = a.parse_args()
from cryptography.hazmat.primitives.serialization import load_pem_private_key
key = load_pem_private_key(open(o.key, "rb").read(), None)
data = open(o.file, "rb").read()
name = f"windows/Sahara-PC-Doctor-{o.version}.exe"
os.makedirs("windows", exist_ok=True)
for old in os.listdir("windows"): os.remove(os.path.join("windows", old))
shutil.copyfile(o.file, name)
feed = json.load(open("update.json")) if os.path.exists("update.json") else {}
feed["windows"] = {"version": o.version, "url": BASE + name, "notes": o.notes, "force": o.force,
                   "build": o.number, "minBuild": o.min, "signature": key.sign(data).hex()}
json.dump(feed, open("update.json", "w"), indent=2, ensure_ascii=False)
print("published", name)
