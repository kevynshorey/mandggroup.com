#!/usr/bin/env python3
"""Build the M&G monogram assets from the site's own self-hosted fonts.

Outputs:
  assets/img/favicon.svg          rounded navy tile, used by modern browsers
  assets/img/apple-touch-icon.png 180x180 full-bleed tile for iOS home screens
  assets/img/logo-512.png         512x512 full-bleed tile (structured-data logo)
  favicon.ico                     16/32/48 legacy icon at the site root

Dev-only requirements: fonttools + brotli (pip), rsvg-convert, ImageMagick (`magick`).
Usage: python3 tools/build_assets.py
"""
from pathlib import Path
import subprocess
import tempfile

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"
IMG = ROOT / "assets" / "img"

NAVY = "#0F2442"
CREAM = "#F3EEE3"
GOLD = "#D9B872"
TRACK = 12  # extra font units between glyphs


def ntos(value: float) -> str:
    text = f"{value:.1f}".rstrip("0").rstrip(".")
    return "0" if text in ("-0", "") else text


def monogram():
    roman = instantiateVariableFont(
        TTFont(FONTS / "cormorant-garamond-latin-var.woff2"), {"wght": 700}
    )
    italic = TTFont(FONTS / "cormorant-garamond-italic-latin.woff2")
    run = [("M", roman, CREAM), ("&", italic, GOLD), ("G", roman, CREAM)]
    x = 0.0
    paths, box = [], None
    for char, font, colour in run:
        glyphs = font.getGlyphSet()
        name = font.getBestCmap()[ord(char)]
        flip = (1, 0, 0, -1, x, 0)
        pen = SVGPathPen(glyphs, ntos=ntos)
        glyphs[name].draw(TransformPen(pen, flip))
        bounds_pen = BoundsPen(glyphs)
        glyphs[name].draw(TransformPen(bounds_pen, flip))
        b = bounds_pen.bounds
        box = b if box is None else (
            min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3])
        )
        paths.append((pen.getCommands(), colour))
        x += font["hmtx"][name][0] + TRACK
    return paths, box


def tile_svg(size: int, pad: float, radius: float) -> str:
    paths, (x0, y0, x1, y1) = monogram()
    scale = (size - 2 * pad) / (x1 - x0)
    tx = pad - x0 * scale
    ty = (size - (y1 - y0) * scale) / 2 - y0 * scale
    body = "".join(f'<path fill="{colour}" d="{d}"/>' for d, colour in paths)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">'
        f'<title>M&amp;G Group</title>'
        f'<rect width="{size}" height="{size}" rx="{radius}" fill="{NAVY}"/>'
        f'<g transform="translate({tx:.2f} {ty:.2f}) scale({scale:.5f})">{body}</g></svg>\n'
    )


def render_png(svg_text: str, out: Path, px: int) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False) as handle:
        handle.write(svg_text)
        src = handle.name
    subprocess.run(["rsvg-convert", "-w", str(px), "-h", str(px), "-o", str(out), src], check=True)
    Path(src).unlink()


def main() -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    favicon = tile_svg(64, pad=7, radius=12)
    (IMG / "favicon.svg").write_text(favicon)
    full_bleed_180 = tile_svg(180, pad=26, radius=0)
    render_png(full_bleed_180, IMG / "apple-touch-icon.png", 180)
    full_bleed_512 = tile_svg(512, pad=80, radius=0)
    render_png(full_bleed_512, IMG / "logo-512.png", 512)
    with tempfile.TemporaryDirectory() as tmp:
        sizes = []
        for px in (16, 32, 48):
            png = Path(tmp) / f"icon-{px}.png"
            render_png(favicon, png, px)
            sizes.append(str(png))
        subprocess.run(["magick", *sizes, str(ROOT / "favicon.ico")], check=True)
    for path in (IMG / "favicon.svg", IMG / "apple-touch-icon.png", IMG / "logo-512.png", ROOT / "favicon.ico"):
        print(f"{path.relative_to(ROOT)}  {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
