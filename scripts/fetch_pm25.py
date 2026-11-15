#!/usr/bin/env python3
"""Download the full hourly history of one OpenAQ location from the public
OpenAQ S3 archive (no API key, no AWS credentials).

Source : https://openaq-data-archive.s3.amazonaws.com/
Layout : records/csv.gz/locationid={id}/year={yyyy}/month={mm}/location-{id}-{yyyymmdd}.csv.gz
Default: location 8876 = "Almaty" (provider AirNow, reference-grade PM2.5 monitor).

Usage  : python3 -I fetch_openaq_almaty.py [--location 8876] [--out data/openaq_8876]

Downloaded files are treated as untrusted data: they are only written to disk
here, never executed. Existing files with the same size are skipped, so the
script can be re-run to pick up new days.
"""
import argparse
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

BUCKET = "https://openaq-data-archive.s3.amazonaws.com/"
NS = "{http://s3.amazonaws.com/doc/2006-03-01/}"
UA = "almaty-smog-feasibility-check/0.1 (python urllib)"
KEY_RE = re.compile(r"^records/csv\.gz/locationid=(\d+)/year=(\d{4})/month=(\d{2})/location-\d+-(\d{8})\.csv\.gz$")


def http_get(url, retries=4, timeout=60):
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except Exception as exc:  # noqa: BLE001 - retry on any network error
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"GET failed after {retries} tries: {url}: {last}")


def list_keys(location_id):
    """Return [(key, size)] for every object of the location (paginated)."""
    prefix = f"records/csv.gz/locationid={location_id}/"
    token = None
    out = []
    while True:
        q = {"list-type": "2", "prefix": prefix, "max-keys": "1000"}
        if token:
            q["continuation-token"] = token
        root = ET.fromstring(http_get(BUCKET + "?" + urllib.parse.urlencode(q)))
        for c in root.findall(NS + "Contents"):
            out.append((c.findtext(NS + "Key"), int(c.findtext(NS + "Size"))))
        if root.findtext(NS + "IsTruncated") == "true":
            token = root.findtext(NS + "NextContinuationToken")
        else:
            return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--location", type=int, default=8876)
    ap.add_argument("--out", default=None)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = args.out or os.path.join(here, "data", f"openaq_{args.location}")
    os.makedirs(out_dir, exist_ok=True)

    keys = list_keys(args.location)
    todo = []
    for key, size in keys:
        m = KEY_RE.match(key)
        if not m or int(m.group(1)) != args.location:
            print("skipping unexpected key:", key, file=sys.stderr)
            continue
        # file name is rebuilt from validated digits only (no path taken from the listing)
        dest = os.path.join(out_dir, f"location-{args.location}-{m.group(4)}.csv.gz")
        if os.path.exists(dest) and os.path.getsize(dest) == size:
            continue
        todo.append((key, dest, size))

    print(f"location {args.location}: {len(keys)} objects listed, {len(todo)} to download -> {out_dir}")

    def fetch(item):
        key, dest, size = item
        data = http_get(BUCKET + urllib.parse.quote(key, safe="/=-."))
        if len(data) != size:
            raise RuntimeError(f"size mismatch for {key}: {len(data)} != {size}")
        tmp = dest + ".part"
        with open(tmp, "wb") as fh:
            fh.write(data)
        os.replace(tmp, dest)
        return dest

    done = 0
    failed = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for res in pool.map(lambda it: _safe(fetch, it), todo):
            if res is None:
                failed += 1
            else:
                done += 1
            if (done + failed) % 250 == 0:
                print(f"  {done + failed}/{len(todo)} ...", flush=True)
    names = sorted(f for f in os.listdir(out_dir) if f.endswith(".csv.gz"))
    print(f"downloaded {done}, failed {failed}, files on disk {len(names)}")
    if names:
        print("first file:", names[0], " last file:", names[-1])
    return 1 if failed else 0


def _safe(fn, item):
    try:
        return fn(item)
    except Exception as exc:  # noqa: BLE001
        print("FAILED:", item[0], exc, file=sys.stderr)
        return None


if __name__ == "__main__":
    sys.exit(main())
