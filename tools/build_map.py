#!/usr/bin/env python3
"""Draw the base map (sea or land, water, beaches, parks, roads, trails) around the house as an SVG.

Run from the project root:  python3 tools/build_map.py
Input:  tools/data/map.json (frame, title, labels, trail names) and tools/data/osm.json (python3 tools/fetch_osm.py)
Output: assets/img/map.svg. Pins and labels are added in the browser from assets/js/config.js,
using the bounding box written to the SVG's data-bbox attribute.
"""
import json
import math
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SETTINGS = json.loads((ROOT / "tools" / "data" / "map.json").read_text())
SRC = ROOT / "tools" / "data" / "osm.json"
OUT = ROOT / "assets" / "img" / "map.svg"

WEST, SOUTH, EAST, NORTH = SETTINGS["bbox"]
WIDTH = 1000
KX = WIDTH / (EAST - WEST)
KY = KX / math.cos(math.radians((NORTH + SOUTH) / 2))
HEIGHT = round((NORTH - SOUTH) * KY)

ROAD_CLASSES = {
    "secondary": "road-major",
    "tertiary": "road-major",
    "residential": "road",
    "unclassified": "road",
    "living_street": "road",
    "pedestrian": "road",
}


def xy(pt: dict) -> str:
    return f"{(pt['lon'] - WEST) * KX:.1f},{(NORTH - pt['lat']) * KY:.1f}"


def path(geom: list, close: bool = False) -> str:
    return "M" + " L".join(xy(p) for p in geom) + (" Z" if close else "")


def coastline(ways: list) -> list:
    """Stitch coastline ways end-to-start into one chain (land lies to the left of travel)."""
    by_start = {w["nodes"][0]: w for w in ways}
    ends = {w["nodes"][-1] for w in ways}
    first = next(w for w in ways if w["nodes"][0] not in ends)
    chain, way = [], first
    while way:
        chain.extend(way["geometry"] if not chain else way["geometry"][1:])
        way = by_start.get(way["nodes"][-1])
    return chain


def land(ways: list) -> str:
    """The land as one path: the coastline chain closed on its land side, plus any closed islands.

    Land lies to the left of the chain, so from the chain's end the outline walks counter-clockwise
    round a box just outside the frame and every coastline point, back to the chain's start.
    """
    islands = [w for w in ways if w["nodes"][0] == w["nodes"][-1]]
    pts = [((p["lon"] - WEST) * KX, (NORTH - p["lat"]) * KY) for p in coastline([w for w in ways if w not in islands])]
    x0 = min([0] + [x for x, _ in pts]) - 50
    x1 = max([WIDTH] + [x for x, _ in pts]) + 50
    y0 = min([0] + [y for _, y in pts]) - 50
    y1 = max([HEIGHT] + [y for _, y in pts]) + 50
    w, h = x1 - x0, y1 - y0

    def onto_box(x: float, y: float) -> tuple:
        """The nearest point on the box, and how far it is counter-clockwise from the top-right corner."""
        side = min((y - y0, "top"), (x - x0, "left"), (y1 - y, "bottom"), (x1 - x, "right"))[1]
        if side == "top":
            return (x, y0), x1 - x
        if side == "left":
            return (x0, y), w + y - y0
        if side == "bottom":
            return (x, y1), w + h + x - x0
        return (x1, y), 2 * w + h + y1 - y

    (end, t_end), (start, t_start) = onto_box(*pts[-1]), onto_box(*pts[0])
    ahead = lambda t: (t - t_end) % (2 * (w + h))
    corners = [((x0, y0), w), ((x0, y1), w + h), ((x1, y1), 2 * w + h), ((x1, y0), 0)]
    walk = [c for c, t in sorted(corners, key=lambda c: ahead(c[1])) if 0 < ahead(t) < ahead(t_start)]
    outline = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts + [end] + walk + [start]) + " Z"
    return " ".join([outline] + [path(i["geometry"], close=True) for i in islands])


def label(spec: dict) -> str:
    anchor = f' text-anchor="{spec["anchor"]}"' if "anchor" in spec else ""
    return f'  <text class="{spec["class"]}" x="{spec["x"]}" y="{spec["y"]}"{anchor}>{escape(spec["text"])}</text>'


def main() -> None:
    elements = json.loads(SRC.read_text())["elements"]
    tags = lambda e: e.get("tags", {})
    coast_ways = [e for e in elements if tags(e).get("natural") == "coastline"]
    trails = set(SETTINGS.get("trails", []))

    layers = {"water": [], "river": [], "sand": [], "park": [], "pier": [], "road": [], "road-major": [], "trail": []}
    for e in elements:
        t, g = tags(e), e.get("geometry")
        if not g:
            continue
        if t.get("natural") == "water":
            layers["water"].append(path(g, close=True))
        elif t.get("waterway") == "river":
            layers["river"].append(path(g))
        elif t.get("natural") in ("beach", "sand"):
            layers["sand"].append(path(g, close=True))
        elif t.get("leisure") == "park":
            layers["park"].append(path(g, close=True))
        elif t.get("man_made"):
            layers["pier"].append(path(g))
        elif t.get("name") in trails:
            layers["trail"].append(path(g))
        elif t.get("highway") in ROAD_CLASSES:
            layers[ROAD_CLASSES[t["highway"]]].append(path(g))

    groups = "\n".join(
        f'  <path class="{name}" d="{" ".join(paths)}"/>' for name, paths in layers.items() if paths
    )
    # By the sea: sea fills the frame and the coastline closes the land over it. Inland: land fills the frame.
    if coast_ways:
        ground = f"""  <rect class="sea" width="{WIDTH}" height="{HEIGHT}"/>
  <rect class="sea-texture" width="{WIDTH}" height="{HEIGHT}" fill="url(#waves)"/>
  <path class="land" d="{land(coast_ways)}"/>"""
    else:
        ground = f'  <rect class="land" width="{WIDTH}" height="{HEIGHT}"/>'
    scale = 500 / (111_320 * math.cos(math.radians((NORTH + SOUTH) / 2))) * KX  # 500 m in map units
    notes = "\n".join(label(spec) for spec in SETTINGS.get("labels", [])) + f"""
  <g class="scale" transform="translate(30 {HEIGHT - 80})">
    <path d="M0 0 H{scale:.0f} M0 -8 V0 M{scale:.0f} -8 V0"/>
    <text x="{scale / 2:.0f}" y="-14">500 m</text>
  </g>
  <g class="north" transform="translate({WIDTH - 44} 52)">
    <path d="M0 -26 L12 14 L0 6 L-12 14 Z"/>
    <text y="40">N</text>
  </g>"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" class="map-svg{'' if coast_ways else ' inland'}" data-bbox="{WEST},{SOUTH},{EAST},{NORTH}" role="img" aria-labelledby="map-title">
  <title id="map-title">{escape(SETTINGS["title"])}</title>
  <defs>
    <pattern id="waves" width="48" height="22" patternUnits="userSpaceOnUse">
      <path d="M2 14 q10 -8 20 0 t20 0" class="wave"/>
    </pattern>
    <clipPath id="frame"><rect width="{WIDTH}" height="{HEIGHT}" rx="0"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
{ground}
{groups}
{notes}
  </g>
  <g class="pins"></g>
</svg>
"""
    OUT.write_text(svg)
    print(f"{OUT.relative_to(ROOT)}  {WIDTH}x{HEIGHT}  {len(svg) // 1024} KB")


if __name__ == "__main__":
    main()
