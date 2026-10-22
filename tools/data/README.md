# Map data

`map.json` sets the base map:

- `bbox`: the frame as `[west, south, east, north]` in decimal degrees. The map is 1000 units wide; its height follows from the frame's shape.
- `title`: the map's accessible name.
- `trails`: OpenStreetMap way names drawn as a red dashed trail, e.g. `"Saint Blaize Hiking Trail"`.
- `labels`: text drawn on the map, e.g. `{ "text": "Indian Ocean", "x": 790, "y": 740, "class": "sea-label" }`. `x` and `y` are map units (0 to 1000 across). `class` is `sea-label` (big faded capitals) or `trail-label` (red, for a trail). Add `"anchor": "end"` or `"start"` to change the alignment, which is centred by default.

`osm.json` is OpenStreetMap data (© OpenStreetMap contributors, ODbL), downloaded from the Overpass API:

```bash
python3 tools/fetch_osm.py    # after changing bbox
python3 tools/build_map.py    # after changing anything in map.json
```
