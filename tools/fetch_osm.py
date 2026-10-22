#!/usr/bin/env python3
"""Download the OpenStreetMap data for the base map into tools/data/osm.json.

Run from the project root:  python3 tools/fetch_osm.py   then   python3 tools/build_map.py
Reads the frame from tools/data/map.json. Data © OpenStreetMap contributors (ODbL), via the Overpass API.
"""
import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEST, SOUTH, EAST, NORTH = json.loads((ROOT / "tools" / "data" / "map.json").read_text())["bbox"]
OUT = ROOT / "tools" / "data" / "osm.json"
API = "https://overpass-api.de/api/interpreter"


def box(pad: float) -> str:
    return f"({SOUTH - pad},{WEST - pad},{NORTH + pad},{EAST + pad})"


# The coastline reaches well past the frame so the land shape closes outside it.
coast, near = box(0.008), box(0.003)
QUERY = f"""[out:json][timeout:90];(
way["natural"="coastline"]{coast};
way["highway"~"^(primary|secondary|tertiary|residential|unclassified|living_street|pedestrian|footway|path)$"]{near};
way["man_made"~"^(pier|breakwater|groyne)$"]{near};
way["leisure"~"^(golf_course|park)$"]{near};
way["natural"~"^(beach|sand|water)$"]{near};
way["waterway"="river"]{near};
);out geom;"""

request = urllib.request.Request(
    API, data=urllib.parse.urlencode({"data": QUERY}).encode(), headers={"User-Agent": "holiday-home-map/1.0"}
)
with urllib.request.urlopen(request, timeout=120) as response:
    data = json.load(response)
OUT.write_text(json.dumps(data))
print(f"{OUT.relative_to(ROOT)}  {len(data['elements'])} ways")
