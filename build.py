"""Build the Beacon Pool website into public/index.html.

The app is one self-contained page: src/app.html holds the markup, styles and
script; the truck-art drawings and the Lahore road + park data are inlined at
build time so the site loads with no other requests besides Google Fonts.

    python3 build.py
"""
import json
import pathlib
import urllib.parse

ROOT = pathlib.Path(__file__).parent
SRC, ART, OUT = ROOT / "src", ROOT / "src" / "art", ROOT / "public"
SITE = "https://beaconpool.vercel.app"
DESCRIPTION = ("Beacon Pool: carpools for Beaconhouse Garden Town, Lahore. Find classmates near you, "
               "share the school run, and grow a bagh of real trees with every ride.")

# The website has no shared database yet, so it runs as the demo version.
WEB_COPY = {
    "Preview mode: your spot stays on this device.":
        "Demo version: your spot stays on this device. The school version adds Beaconhouse sign-in.",
    "Open Beacon Pool while signed in to message real classmates.":
        "Chatting with real classmates turns on in the school version, with Beaconhouse sign-in.",
    "Open Beacon Pool while signed in to send real requests.":
        "Real ride requests turn on in the school version, with Beaconhouse sign-in.",
}

HEAD = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, interactive-widget=resizes-content">
<meta name="theme-color" content="#061D7B">
<meta name="color-scheme" content="light">
<meta name="description" content="{DESCRIPTION}">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Beacon Pool">
<meta name="format-detection" content="telephone=no">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Beacon Pool">
<meta property="og:title" content="Beacon Pool">
<meta property="og:description" content="{DESCRIPTION}">
<meta property="og:url" content="{SITE}/">
<meta property="og:image" content="{SITE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Beacon Pool">
<meta name="twitter:description" content="{DESCRIPTION}">
<meta name="twitter:image" content="{SITE}/og.png">
"""


def main():
    app = (SRC / "app.html").read_text()
    art = {key: (ART / name).read_text() for key, name in {
        "flowerPink": "flower-pink.svg", "flowerTeal": "flower-teal.svg", "flowerGold": "flower-gold.svg",
        "vine": "vine.svg", "leafTile": "leaf-tile.svg", "rickshaw": "rickshaw.svg"}.items()}
    roads = (SRC / "data" / "lahore-roads.json").read_text()
    app = (app.replace("/*ART*/", json.dumps(art).replace("</", "<\\/"))
              .replace("/*GRAPH*/", roads.replace("</", "<\\/")))
    # Urdu font: ask Google Fonts for just the letters the app uses (a few KB instead of a large file)
    urdu = sorted({ch for ch in app if "\u0600" <= ch <= "\u06ff" or ch in " !"})
    app = app.replace("/*URDU_FONT*/", "https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu&display=swap&text="
                      + urllib.parse.quote("".join(urdu)))
    for old, new in WEB_COPY.items():
        assert old in app, old
        app = app.replace(old, new)
    cut = app.index("</style>") + len("</style>")
    page = HEAD + app[:cut] + "\n</head>\n<body>\n" + app[cut:].lstrip() + "</body>\n</html>\n"
    assert page.count("<script>") == 1 and page.count("</script>") == 3, "script tags look wrong"
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(page)
    (OUT / "site.webmanifest").write_text(json.dumps({
        "name": "Beacon Pool", "short_name": "Beacon Pool", "description": DESCRIPTION,
        "start_url": "/", "display": "standalone", "orientation": "any",
        "background_color": "#061D7B", "theme_color": "#061D7B",
        "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]}, indent=2))
    print(f"public/index.html: {len(page) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
