"""Geocode addresses using OpenStreetMap Nominatim with caching.

This script reads service location records that lack latitude/longitude
values, queries the OSM Nominatim API to obtain coordinates, and
writes the results back to the processed CSV or directly updates the
database. Results are cached in a local SQLite database to avoid
duplicate requests and respect rate limits. In development, you
should pause between requests to avoid hammering the service.
"""

import sqlite3
import time
from pathlib import Path
from typing import Optional, Tuple

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


CACHE_DB = Path(__file__).resolve().parents[2] / "data" / "cache" / "geocode.sqlite"


class Geocoder:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="govmate-etl")
        self.rate_limited_geocode = RateLimiter(self.geolocator.geocode, min_delay_seconds=1)
        # ensure cache directory exists
        CACHE_DB.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(CACHE_DB)
        self._ensure_table()

    def _ensure_table(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                query TEXT PRIMARY KEY,
                lat REAL,
                lon REAL
            )
            """
        )

    def geocode(self, query: str) -> Optional[Tuple[float, float]]:
        cur = self.conn.cursor()
        row = cur.execute("SELECT lat, lon FROM cache WHERE query = ?", (query,)).fetchone()
        if row:
            return row
        # perform lookup
        try:
            location = self.rate_limited_geocode(query)
        except Exception:
            location = None
        if location:
            lat, lon = location.latitude, location.longitude
            cur.execute("INSERT INTO cache (query, lat, lon) VALUES (?, ?, ?)", (query, lat, lon))
            self.conn.commit()
            return lat, lon
        return None


def main():
    g = Geocoder()
    # Example usage
    addr = "56 Edward Street Brisbane City QLD"
    coords = g.geocode(addr)
    print(addr, coords)


if __name__ == "__main__":
    main()