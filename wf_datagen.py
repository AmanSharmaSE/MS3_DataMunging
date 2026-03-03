import os
import re
import gzip
import shutil
import hashlib
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

CITY_PAGE = "https://insideairbnb.com/mexico-city/"  # Mexico City portal page
RAW_DIR = "data_original"
GZ_OUT = os.path.join(RAW_DIR, "listings.csv.gz")
CSV_OUT = os.path.join(RAW_DIR, "MexicoCityDataSet.csv")
MD5_OUT = os.path.join(RAW_DIR, "MexicoCityDataSet.md5.txt")


def md5_file(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def find_latest_listings_gz_url() -> str:
    """
    Scrape the Mexico City InsideAirbnb page and find the latest 'listings.csv.gz' link.
    We pick the link with the newest YYYY-MM-DD in the URL.
    """
    r = requests.get(CITY_PAGE, timeout=60)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        full = urljoin(CITY_PAGE, href)

        # We only want detailed listings gz
        if full.endswith("/data/listings.csv.gz") and "data.insideairbnb.com" in full:
            # Extract date like 2025-09-28 from URL if present
            m = re.search(r"/(\d{4}-\d{2}-\d{2})/data/listings\.csv\.gz$", full)
            date_str = m.group(1) if m else "0000-00-00"
            links.append((date_str, full))

    if not links:
        raise RuntimeError("Could not find any listings.csv.gz links on the city page.")

    # Sort by date string (YYYY-MM-DD sorts lexicographically correctly)
    links.sort(key=lambda x: x[0], reverse=True)
    return links[0][1]


def download(url: str, out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)


def gunzip(gz_path: str, csv_path: str) -> None:
    with gzip.open(gz_path, "rb") as f_in:
        with open(csv_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


def run_datagen() -> dict:
    """
    Downloads the latest Mexico City listings.csv.gz, extracts it to CSV, and writes md5.
    Returns metadata about what was downloaded.
    """
    os.makedirs(RAW_DIR, exist_ok=True)

    url = find_latest_listings_gz_url()
    print(f"Found latest listings.gz URL:\n{url}")

    print(f"Downloading to {GZ_OUT} ...")
    download(url, GZ_OUT)

    print(f"📦 Extracting to {CSV_OUT} ...")
    gunzip(GZ_OUT, CSV_OUT)

    md5_csv = md5_file(CSV_OUT)
    with open(MD5_OUT, "w", encoding="utf-8") as f:
        f.write(f"{md5_csv}  {os.path.basename(CSV_OUT)}\n")
        f.write(f"source_url: {url}\n")

    return {
        "city_page": CITY_PAGE,
        "source_url": url,
        "gz_path": GZ_OUT,
        "csv_path": CSV_OUT,
        "csv_md5": md5_csv,
        "md5_file": MD5_OUT,
    }


if __name__ == "__main__":
    meta = run_datagen()
    print("Data generation complete:")
    for k, v in meta.items():
        print(f"{k}: {v}")