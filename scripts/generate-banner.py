"""Render the original animated profile banner. Requires Pillow >= 10.

Uses the attributed IBM Plex Mono fonts in assets/fonts.
Pass --font-dir to supply the same font family elsewhere. No network requests.
"""
from argparse import ArgumentParser
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

parser = ArgumentParser()
parser.add_argument('--font-dir', type=Path)
args = parser.parse_args()
font_dirs = [args.font_dir] if args.font_dir else [Path(__file__).resolve().parent.parent / 'assets/fonts']

def font(size, bold=False):
    names = ['IBMPlexMono-Bold.ttf'] if bold else ['IBMPlexMono-Regular.ttf']
    for directory in font_dirs:
        for name in names:
            file = directory / name
            if file.is_file():
                return ImageFont.truetype(str(file), size)
    raise SystemExit('Run scripts/fetch-design-assets.py to download IBM Plex Mono.')

W, H = 960, 256
assets = Path(__file__).resolve().parent.parent / 'assets'
assets.mkdir(exist_ok=True)
themes = {
    'dark': dict(bg='#0B1220', grid='#111E31', border='#21314D', text='#E2E8F0', muted='#9CAEC8', accent='#3B82F6', glow='#93C5FD'),
    'light': dict(bg='#F4F7FB', grid='#E9EFF8', border='#C7D6EC', text='#0B1220', muted='#5A6B85', accent='#2563EB', glow='#1D4ED8'),
}
roles = ['Software Engineer', 'AI Engineer', 'Full Stack Developer']
body_font, small_font = font(24), font(14)

def role_at(frame):
    phase, tick = divmod(frame, 32)
    role, next_role = roles[phase], roles[(phase + 1) % len(roles)]
    if tick < 18:
        return role
    if tick < 23:
        return role[:round(len(role) * (23 - tick) / 5)]
    return next_role[:round(len(next_role) * (tick - 22) / 9)]

def point_along(points, progress):
    lengths = [math.dist(a, b) for a, b in zip(points, points[1:])]
    remaining = progress * sum(lengths)
    for (a, b), length in zip(zip(points, points[1:]), lengths):
        if remaining <= length:
            t = remaining / length
            return a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])
        remaining -= length
    return points[-1]

def render(c, frame, static=False):
    im = Image.new('RGB', (W, H), c['bg'])
    d = ImageDraw.Draw(im)
    for x in range(0, W, 32):
        d.line((x, 0, x, H), fill=c['grid'])
    for y in range(0, H, 32):
        d.line((0, y, W, y), fill=c['grid'])
    for x, y, dx, dy in [(16, 16, 1, 1), (944, 16, -1, 1), (16, 240, 1, -1), (944, 240, -1, -1)]:
        d.line([(x, y + dy * 16), (x, y), (x + dx * 16, y)], fill=c['accent'], width=2)
    d.text((40, 27), 'PH', font=font(18, True), fill=c['text'])
    d.text((72, 27), '// dev', font=font(18), fill=c['accent'])
    d.text((920, 31), 'PROFILE / RESUME', font=font(12), fill=c['muted'], anchor='rt')
    d.line((40, 64, 920, 64), fill=c['border'])
    d.text((36, 79), 'Pedro Henrique', font=font(62, True), fill=c['text'])
    d.text((40, 156), '>', font=body_font, fill=c['muted'])
    role = roles[0] if static else role_at(frame)
    d.text((68, 156), role, font=body_font, fill=c['accent'])
    end = 68 + d.textlength(role, font=body_font)
    if static or (frame // 5) % 2 == 0:
        d.rectangle((end + 10, 159, end + 19, 181), fill=c['accent'])
    d.text((40, 213), 'SOFTWARE / INTELIGÊNCIA ARTIFICIAL', font=small_font, fill=c['muted'])
    # Circuit branches with packets traveling from input to output.
    paths = [
        [(698, 118), (738, 118), (766, 90), (854, 90)],
        [(698, 118), (794, 118), (822, 146), (888, 146)],
        [(738, 118), (738, 162), (772, 196), (854, 196)],
    ]
    for lane, points in enumerate(paths):
        d.line(points, fill=c['border'], width=2)
        if not static:
            progress = ((frame + lane * 25) % 96) / 95
            x, y = point_along(points, progress)
            d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=c['accent'])
            d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=c['glow'])
        x, y = points[-1]
        d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=c['bg'], outline=c['accent'], width=2)
    d.rectangle((692, 112, 704, 124), fill=c['accent'])
    return im

for theme, colors in themes.items():
    still = render(colors, 0, static=True)
    still.save(assets / f'resume-{theme}.png', optimize=True)
    palette = still.quantize(colors=64)
    frames = [render(colors, frame).quantize(palette=palette, dither=Image.Dither.NONE) for frame in range(96)]
    frames[0].save(
        assets / f'resume-{theme}.gif', save_all=True, append_images=frames[1:],
        duration=100, loop=0, optimize=True, disposal=1,
    )
    output = assets / f'resume-{theme}.gif'
    print(f'{output.name}: {output.stat().st_size:,} bytes / 96 frames / 9.6s')
