# Google 3D Tiles AOI test

Serve the parent `apps/geolibre/experimental` directory over HTTP and open
`/google-3d-test/`. Paste a restricted Google Maps Platform key to test a small
Kharghar scene independently of the Helios AOI and ranking code. The key is
held only in memory for the current browser session and is cleared from the
input immediately after the renderer is created.

This test uses deck.gl's `Tile3DLayer` synchronized over MapLibre. Google lists
deck.gl as a supported Photorealistic 3D Tiles renderer. The earlier
`maplibre-gl-3d-tiles` control was removed because it stayed indefinitely at
`1 loading, 0 loaded` with Google's global root tileset.

The root URL carries the key as documented by Google, while descendant requests
also receive `X-GOOG-API-KEY`. A one-request probe reports Google's actual HTTP
status before the renderer starts, and rendered-tile attribution is displayed.
If Google's documented `root.json` responds with 404, the test also tries the
`/v1/3dtiles/root` endpoint referenced by Google's release notes.
