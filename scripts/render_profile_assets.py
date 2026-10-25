from __future__ import annotations

import io
import math
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
NODE_PATHS = [
    [(500, 111), (500, 139), (125, 139), (125, 190)],
    [(500, 111), (500, 139), (375, 139), (375, 190)],
    [(500, 111), (500, 139), (625, 139), (625, 190)],
    [(500, 111), (500, 139), (875, 139), (875, 190)],
]
NODE_COLORS = [(56, 189, 248), (167, 139, 250), (52, 211, 153), (251, 191, 36)]


def point_on_polyline(points: list[tuple[int, int]], progress: float) -> tuple[float, float]:
    lengths = [
        math.hypot(b[0] - a[0], b[1] - a[1])
        for a, b in zip(points, points[1:])
    ]
    remaining = (progress % 1.0) * sum(lengths)
    for (a, b), distance in zip(zip(points, points[1:]), lengths):
        if remaining <= distance:
            fraction = remaining / distance if distance else 0.0
            return (
                a[0] + (b[0] - a[0]) * fraction,
                a[1] + (b[1] - a[1]) * fraction,
            )
        remaining -= distance
    return float(points[-1][0]), float(points[-1][1])


def render_network_gif() -> None:
    svg_path = ASSETS / "global-hq-network.svg"
    if not svg_path.is_file():
        raise FileNotFoundError(f"Required vector source not found: {svg_path}")
    png = cairosvg.svg2png(
        bytestring=svg_path.read_bytes(), output_width=1000, output_height=370
    )
    base = Image.open(io.BytesIO(png)).convert("RGBA")
    frames: list[Image.Image] = []

    for frame_index in range(8):
        frame = base.copy()
        glow = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        draw_glow = ImageDraw.Draw(glow)
        for node_index, path in enumerate(NODE_PATHS):
            x, y = point_on_polyline(
                path, (frame_index / 8 + node_index * 0.23) % 1
            )
            radius = 5 + (frame_index % 4) * 0.25
            color = NODE_COLORS[node_index]
            draw_glow.ellipse(
                (x - radius * 2.1, y - radius * 2.1,
                 x + radius * 2.1, y + radius * 2.1),
                fill=(*color, 42),
            )
            draw_glow.ellipse(
                (x - radius, y - radius, x + radius, y + radius),
                fill=(*color, 230),
            )
            draw_glow.ellipse(
                (x - 1.7, y - 1.7, x + 1.7, y + 1.7),
                fill=(255, 255, 255, 255),
            )
        frame = Image.alpha_composite(frame, glow.filter(ImageFilter.GaussianBlur(3)))
        draw = ImageDraw.Draw(frame)
        for node_index, (cx, cy) in enumerate(
            [(48, 217), (298, 217), (548, 217), (798, 217)]
        ):
            phase = (frame_index + node_index * 2) % 8
            radius = 6 + (phase / 7) * 8
            color = NODE_COLORS[node_index]
            draw.ellipse(
                (cx - radius, cy - radius, cx + radius, cy + radius),
                outline=(*color, int(150 * (1 - phase / 8))),
                width=2,
            )
            draw.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=(*color, 255))
        frames.append(frame.convert("RGB"))

    palette = (
        base.convert("RGB").resize((250, 93))
        .quantize(colors=48, method=Image.Quantize.MEDIANCUT)
    )
    indexed = [
        frame.quantize(palette=palette, dither=Image.Dither.NONE)
        for frame in frames
    ]
    output = ASSETS / "global-hq-network.gif"
    indexed[0].save(
        output, save_all=True, append_images=indexed[1:], duration=180,
        loop=0, optimize=True, disposal=1,
    )
    print(f"Generated {output.relative_to(ROOT)} ({output.stat().st_size} bytes)")


def render_badge_strip_gif() -> None:
    source_names = [
        "badge-konya.svg", "badge-sakarya.svg",
        "badge-istanbul.svg", "badge-tashkent.svg",
    ]
    images: list[Image.Image] = []
    for name in source_names:
        path = ASSETS / name
        if not path.is_file():
            raise FileNotFoundError(f"Required badge source not found: {path}")
        png = cairosvg.svg2png(url=str(path), output_width=220, output_height=38)
        images.append(Image.open(io.BytesIO(png)).convert("RGBA"))

    width, height = 4 * 220 + 3 * 10, 42
    frames: list[Image.Image] = []
    for frame_index in range(12):
        frame = Image.new("RGBA", (width, height), (11, 16, 32, 255))
        for node_index, badge in enumerate(images):
            x = node_index * 230
            frame.alpha_composite(badge, (x, 2))
            phase = (frame_index + node_index * 3) % 12
            radius = 4 + phase / 11 * 4
            layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(layer)
            color = NODE_COLORS[node_index]
            draw.ellipse(
                (x + 17 - radius, 21 - radius, x + 17 + radius, 21 + radius),
                outline=(*color, int(210 * (1 - phase / 12))),
                width=2,
            )
            frame = Image.alpha_composite(frame, layer)
        frames.append(frame.convert("RGB"))

    palette = (
        frames[0].resize((300, 14))
        .quantize(colors=64, method=Image.Quantize.MEDIANCUT)
    )
    indexed = [
        frame.quantize(palette=palette, dither=Image.Dither.NONE)
        for frame in frames
    ]
    output = ASSETS / "hq-node-badges.gif"
    indexed[0].save(
        output, save_all=True, append_images=indexed[1:], duration=150,
        loop=0, optimize=True, disposal=2,
    )
    print(f"Generated {output.relative_to(ROOT)} ({output.stat().st_size} bytes)")


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    render_network_gif()
    render_badge_strip_gif()


if __name__ == "__main__":
    main()
