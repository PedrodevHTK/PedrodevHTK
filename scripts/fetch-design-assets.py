"""Fetch attributed design assets from pinned official repository revisions."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import urlopen, Request
import hashlib
import json

ROOT = Path(__file__).resolve().parent.parent
DEVICON = '6a37858047b0e8d9c9c0e68f4a071fc410652e89'
FONTS = '47d54ca1ebb14fd864695f1d39dc734f39017c33'
LUCIDE = 'c29c276f16590cf017126671535ad8c792be64d8'
SIMPLE = 'c71c69e3a27e4436936b831c72643e6513b9f49b'
files = []

def add(path, repo, revision, upstream):
    files.append((path, f'https://raw.githubusercontent.com/{repo}/{revision}/{upstream}'))

for name in ['react', 'nextjs', 'typescript', 'tailwindcss', 'nodejs', 'nestjs', 'python', 'postgresql', 'redis', 'docker', 'kubernetes', 'googlecloud', 'terraform', 'githubactions', 'linkedin']:
    add(f'assets/vendor/icons/{name}.svg', 'devicons/devicon', DEVICON, f'icons/{name}/{name}-original.svg')
for name in ['brain-circuit', 'database-search', 'layers', 'briefcase-business', 'graduation-cap', 'mail', 'file-user']:
    add(f'assets/vendor/icons/{name}.svg', 'lucide-icons/lucide', LUCIDE, f'icons/{name}.svg')
add('assets/vendor/icons/modelcontextprotocol.svg', 'simple-icons/simple-icons', SIMPLE, 'icons/modelcontextprotocol.svg')
add('assets/vendor/icons/dbt.svg', 'dbt-labs/docs.getdbt.com', 'f5c4986033cfae8c93a1367d6e98fefd479045b0', 'website/static/img/dbt-logo.svg')
for filename in ['IBMPlexMono-Regular.ttf', 'IBMPlexMono-Bold.ttf']:
    add(f'assets/fonts/{filename}', 'google/fonts', FONTS, f'ofl/ibmplexmono/{filename}')
add('assets/fonts/Manrope.ttf', 'google/fonts', FONTS, 'ofl/manrope/Manrope%5Bwght%5D.ttf')
for name, repo, rev, upstream in [
    ('Devicon-LICENSE.txt', 'devicons/devicon', DEVICON, 'LICENSE'),
    ('Lucide-LICENSE.txt', 'lucide-icons/lucide', LUCIDE, 'LICENSE'),
    ('SimpleIcons-LICENSE.txt', 'simple-icons/simple-icons', SIMPLE, 'LICENSE.md'),
    ('IBMPlexMono-OFL.txt', 'google/fonts', FONTS, 'ofl/ibmplexmono/OFL.txt'),
    ('Manrope-OFL.txt', 'google/fonts', FONTS, 'ofl/manrope/OFL.txt'),
]:
    add(f'assets/licenses/{name}', repo, rev, upstream)

def download(item):
    relative, url = item
    try:
        with urlopen(Request(url, headers={'User-Agent': 'Profile-Asset-Builder'}), timeout=45) as response:
            data = response.read()
    except Exception as error:
        raise RuntimeError(f'Could not fetch {url}: {error}') from error
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return dict(path=relative, source=url, sha256=hashlib.sha256(data).hexdigest())

with ThreadPoolExecutor(max_workers=6) as pool:
    manifest = list(pool.map(download, files))
(ROOT / 'assets/sources.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
print(f'Downloaded {len(manifest)} original icons, fonts and licenses.')
