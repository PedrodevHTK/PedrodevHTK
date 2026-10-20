"""Build themed technology chips and README. Requires Pillow and rendered icons."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ROOT = Path(__file__).resolve().parent.parent
BADGES = ROOT / 'assets/badges'
BADGES.mkdir(exist_ok=True)
UI = ROOT / 'assets/ui'
UI.mkdir(exist_ok=True)

def label_font(size):
    result = ImageFont.truetype(str(ROOT / 'assets/fonts/Manrope.ttf'), size)
    result.set_variation_by_axes([600])
    return result

FONT = label_font(29)
TECH = {
    'react': ('React', 'https://react.dev/'),
    'nextjs': ('Next.js', 'https://nextjs.org/'),
    'typescript': ('TypeScript', 'https://www.typescriptlang.org/'),
    'tailwindcss': ('Tailwind CSS', 'https://tailwindcss.com/'),
    'nodejs': ('Node.js', 'https://nodejs.org/'),
    'nestjs': ('NestJS', 'https://nestjs.com/'),
    'python': ('Python', 'https://www.python.org/'),
    'postgresql': ('PostgreSQL', 'https://www.postgresql.org/'),
    'redis': ('Redis', 'https://redis.io/'),
    'brain-circuit': ('LLM', None),
    'database-search': ('RAG', None),
    'modelcontextprotocol': ('MCP', 'https://modelcontextprotocol.io/'),
    'dbt': ('dbt', 'https://www.getdbt.com/'),
    'docker': ('Docker', 'https://www.docker.com/'),
    'kubernetes': ('Kubernetes', 'https://kubernetes.io/'),
    'googlecloud': ('Google Cloud', 'https://cloud.google.com/'),
    'terraform': ('Terraform', 'https://developer.hashicorp.com/terraform'),
    'githubactions': ('GitHub Actions', 'https://github.com/features/actions'),
    'file-user': ('Currículo', 'https://www.pmoraes.dev.br/curriculo'),
    'linkedin': ('LinkedIn', 'https://www.linkedin.com/in/pedrodev2005/'),
    'mail': ('Contato', 'mailto:pedro.dev2005@gmail.com'),
}
THEMES = {
    'dark': dict(bg='#101B2C', border='#243750', text='#E2E8F0'),
    'light': dict(bg='#F4F7FB', border='#CDDAED', text='#17263D'),
}
widths = {}
for slug, (label, url) in TECH.items():
    width = math.ceil(FONT.getlength(label)) + 112
    widths[slug] = math.ceil(width / 2)
    original = Image.open(ROOT / f'.cache/icons/{slug}.png').convert('RGBA')
    for theme, c in THEMES.items():
        image = Image.new('RGBA', (width, 84))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((1, 1, width - 2, 78), radius=13, fill=c['bg'], outline=c['border'], width=2)
        icon = original.copy()
        if slug == 'nextjs':
            draw.ellipse((18, 12, 74, 68), fill='#F4F7FB')
        image.alpha_composite(icon, (18, 12))
        draw.text((89, 39), label, font=FONT, fill=c['text'], anchor='lm')
        image.save(BADGES / f'{slug}-{theme}.png', optimize=True)

for slug in ['layers', 'briefcase-business', 'graduation-cap']:
    source = (ROOT / f'assets/vendor/icons/{slug}.svg').read_text()
    (UI / f'{slug}.svg').write_text(source.replace('currentColor', '#3B82F6'), encoding='utf-8')

def chip(slug):
    label, url = TECH[slug]
    image = f'<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/badges/{slug}-dark.png"><img src="./assets/badges/{slug}-light.png" alt="{label}" width="{widths[slug]}" height="42"></picture>'
    return f'<a href="{url}">{image}</a>' if url else image

def row(title, slugs):
    return f'<p><strong>{title}</strong></p>\n<p>\n  ' + '\n  '.join(chip(slug) for slug in slugs) + '\n</p>\n'

readme = '''<a href="https://www.pmoraes.dev.br/curriculo">
  <picture>
    <source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="./assets/resume-dark.png">
    <source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: light)" srcset="./assets/resume-light.png">
    <source media="(prefers-color-scheme: dark)" srcset="./assets/resume-dark.gif">
    <source media="(prefers-color-scheme: light)" srcset="./assets/resume-light.gif">
    <img src="./assets/resume-dark.gif" alt="Pedro Henrique. Software Engineer, AI Engineer e desenvolvedor Full Stack." width="100%">
  </picture>
</a>

<p>\n  ''' + '\n  '.join(chip(slug) for slug in ['file-user', 'linkedin', 'mail']) + '''
</p>

**Software, dados e inteligência artificial.** Desenvolvimento de ponta a ponta, de interfaces e APIs à orquestração de agentes e integrações corporativas.

## <img src="./assets/ui/layers.svg" width="23" height="23" alt=""> Stack técnica

'''
readme += row('Frontend', ['typescript', 'react', 'nextjs', 'tailwindcss'])
readme += row('Backend', ['nodejs', 'nestjs', 'python', 'postgresql'])
readme += row('Inteligência artificial & dados', ['brain-circuit', 'database-search', 'modelcontextprotocol', 'redis', 'dbt'])
readme += row('Cloud & infraestrutura', ['docker', 'kubernetes', 'googlecloud', 'terraform', 'githubactions'])
readme += '''
## <img src="./assets/ui/briefcase-business.svg" width="23" height="23" alt=""> Experiência

### Software Engineer | AI Engineer

**Haytek** &nbsp;·&nbsp; set/2026 → atual &nbsp;·&nbsp; Híbrido

Plataforma de IA agêntica: **LLM, RAG, MCP e orquestração**, com APIs, autenticação, permissões e integrações corporativas.

<details>
<summary><strong>Desenvolvedor Full Stack · Haytek</strong> &nbsp;·&nbsp; ago/2025 → ago/2026</summary>

Estágio com rotação em Administração, Dados e Infraestrutura. Atuação com Protheus/ADVPL, SQL, Python, dbt, GCP, Terraform e Kubernetes.

</details>

## <img src="./assets/ui/graduation-cap.svg" width="23" height="23" alt=""> Formação

**Engenharia de Software**<br>
Estácio &nbsp;·&nbsp; Bacharelado &nbsp;·&nbsp; 2026 → 2028 &nbsp;·&nbsp; Em andamento

**Análise e Desenvolvimento de Sistemas**<br>
Estácio &nbsp;·&nbsp; Tecnólogo &nbsp;·&nbsp; 2023 → 2026 &nbsp;·&nbsp; Concluído
'''
(ROOT / 'README.md').write_text(readme, encoding='utf-8')
print('Created 42 themed icon chips and the profile README.')
