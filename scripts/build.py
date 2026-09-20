"""Build bilingual static cards from JSON front matter in Markdown files (stdlib only)."""
import json
import hashlib
import re
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT = {
    'fr': dict(alias='Alias', period='Période', locations='Lieux', length='Longueur', wingspan='Envergure', weight='Poids', diet='Régime', sources='Sources', edit='Éditer cette fiche', missing='À compléter', dinosaur='Dinosaure', pterosaur='Ptérosaure', marine_reptile='Reptile marin', hybrid='Hybride fictif', fictional='Fiction contemporaine', universe='Univers', jurassic='Jurassique', cretaceous='Crétacé', triassic='Trias', permian='Permien', synapsid='Synapside', crocodyliform='Crocodyliforme', herbivore='Herbivore', carnivore='Carnivore', omnivore='Omnivore', unknown='Incertain', count='fiches'),
    'en': dict(alias='Aliases', period='Period', locations='Locations', length='Length', wingspan='Wingspan', weight='Weight', diet='Diet', sources='Sources', edit='Edit this entry', missing='To be completed', dinosaur='Dinosaur', pterosaur='Pterosaur', marine_reptile='Marine reptile', hybrid='Fictional hybrid', fictional='Contemporary fiction', universe='Universe', jurassic='Jurassic', cretaceous='Cretaceous', triassic='Triassic', permian='Permian', synapsid='Synapsid', crocodyliform='Crocodyliform', herbivore='Herbivore', carnivore='Carnivore', omnivore='Omnivore', unknown='Uncertain', count='entries'),
}

# Display-only country metadata: source Markdown stays plain text.
COUNTRY_CODES = dict(zip(
    'Algeria|Antarctica|Argentina|Australia|Austria|Belgium|Brazil|Canada|China|Egypt|England|France|Germany|India|Italy|Japan|Kazakhstan|Lesotho|Madagascar|Malawi|Mongolia|Morocco|Netherlands|Niger|Portugal|Romania|Russia|South Africa|Spain|Switzerland|Tanzania|Tunisia|USA|United Kingdom|Uzbekistan|Wales|Zimbabwe'.split('|'),
    'DZ|AQ|AR|AU|AT|BE|BR|CA|CN|EG|GB-ENG|FR|DE|IN|IT|JP|KZ|LS|MG|MW|MN|MA|NL|NE|PT|RO|RU|ZA|ES|CH|TZ|TN|US|GB|UZ|GB-WLS|ZW'.split('|'),
))
ORIGINAL_IMAGES = json.loads((ROOT / 'docs/assets/original-silhouettes/manifest.json').read_text())

def country_flag(code):
    if code.startswith('GB-'):
        # Unicode subdivision flags for England and Wales.
        return chr(0x1F3F4) + ''.join(chr(0xE0000 + ord(c)) for c in code.replace('-', '').lower()) + chr(0xE007F)
    return ''.join(chr(0x1F1E6 + ord(c) - ord('A')) for c in code)

def locations_html(d, lang):
    labels = d[f'locations_{lang}'].split(', ')
    countries = d['locations_en'].split(', ')
    assert len(labels) == len(countries), d['name']
    rendered = []
    for country, label in zip(countries, labels):
        code = COUNTRY_CODES.get(country.split(' (', 1)[0])
        flag = f'<span class="country-flag" aria-hidden="true">{country_flag(code)}</span> ' if code else ''
        rendered.append(f'<span class="country">{flag}{esc(label)}</span>')
    return ', '.join(rendered)

def load_entries():
    entries = []
    for path in sorted((ROOT / 'content').glob('*/*.md')):
        data = json.loads(path.read_text().split('---', 2)[1])
        assert data['period'] in {'permian', 'triassic', 'jurassic', 'cretaceous', 'fictional'}
        assert (data['period'] == 'fictional') == (data['category'] == 'fictional')
        assert data['diet'] in {'herbivore', 'carnivore', 'omnivore', 'unknown'}
        assert data['category'] in {'real', 'fictional'}
        assert data['kind'] in {'dinosaur', 'pterosaur', 'marine_reptile', 'hybrid', 'synapsid', 'crocodyliform'}
        if data['category'] == 'fictional':
            assert data.get('universe_fr') and data.get('universe_en')
        assert data['measurement'] in {'length', 'wingspan'}
        assert data['sources'] and all(s['url'].startswith('https://') for s in data['sources'])
        data['file'] = path.relative_to(ROOT).as_posix()
        entries.append(data)
    assert len({d['name'] for d in entries}) == len(entries), 'Duplicate genus'
    return sorted(entries, key=lambda d: (d['category'] == 'fictional', d['name'].lower()))

def card(d, lang):
    t = TEXT[lang]
    def row(key, value):
        return f'<div><dt>{t[key]}</dt><dd>{esc(value)}</dd></div>'
    def measure(value, unit):
        if not value:
            return t['missing']
        number = value.replace('.', ',') if lang == 'fr' else value
        return f'{number} {unit}'
    rows = row('alias', d[f'aliases_{lang}'].replace(' | ', ' · ') or '—')
    if d['period'] == 'fictional':
        rows += row('period', t['fictional'])
        rows += row('universe', d[f'universe_{lang}'])
    else:
        rows += f'<div><dt>{t["period"]}</dt><dd><a class="period-link" href="periods.html#{d["period"]}">{t[d["period"]]}</a></dd></div>'
    rows += f'<div><dt>{t["locations"]}</dt><dd>{locations_html(d, lang)}</dd></div>'
    rows += row(d['measurement'], measure(d['length_m'], 'm'))
    rows += row('weight', measure(d['weight_kg'], 'kg')) + row('diet', t[d['diet']])
    links = ' '.join(f'<a href="{esc(s["url"])}" target="_blank" rel="noreferrer">{esc(s["label"])} ↗</a>' for s in d['sources'])
    rows += f'<div class="source-row"><dt>{t["sources"]}</dt><dd class="sources">{links}</dd></div>'
    aliases = ' '.join([d['name'], d['aliases_fr'], d['aliases_en']])
    attrs = ' '.join(f'data-{k}="{esc(v, quote=True)}"' for k, v in {'search': aliases, 'period': d['period'], 'diet': d['diet'], 'category': d['category']}.items())
    note = f'<p class="card-note">{esc(d.get("note_" + lang, ""))}</p>' if d.get('note_' + lang) else ''
    image = d.get('image')
    original = ORIGINAL_IMAGES.get(Path(d['file']).stem) if not image else None
    visual = ''
    if original:
        asset = ROOT / 'docs' / original['file']
        assert asset.is_file()
        if original['mode'] == 'comparison':
            detail = 'silhouette originale et humain de 1,75 m ; comparaison schématique' if lang == 'fr' else 'original silhouette and 1.75 m human; schematic comparison'
        else:
            detail = 'silhouette originale, sans échelle' if lang == 'fr' else 'original silhouette, not to scale'
        alt = d['name'] + ' : ' + detail
        visual = f'<span class="size-comparison original-silhouette" title="{esc(alt)}"><img src="../{esc(original["file"])}" alt="{esc(alt)}" width="88" height="68" loading="lazy" decoding="async"></span>'
    if image:
        assert image['mode'] in {'comparison', 'silhouette'}
        assert image['source'].startswith('https://')
        asset = ROOT / 'docs' / image['file']
        assert asset.is_file() and asset.suffix == '.svg'
        if image['mode'] == 'comparison':
            alt = (f"{d['name']} : silhouette générique et humain, comparaison schématique" if lang == 'fr' else f"{d['name']}: generic silhouette and human, schematic comparison")
        else:
            alt = (f"{d['name']} : silhouette générique de sauropode, sans échelle" if lang == 'fr' else f"{d['name']}: generic sauropod silhouette, not to scale")
        visual = f'<a class="size-comparison" href="{esc(image["source"])}" target="_blank" rel="noreferrer" title="{esc(alt)} — Natural History Museum"><img src="../{esc(image["file"])}" alt="{esc(alt)}" width="88" height="68" loading="lazy" decoding="async"></a>'
    return f'''<article class="dinosaur-card{' fictional' if d['category'] == 'fictional' else ''}" {attrs}>
  <div class="card-heading"><p class="kind-label">{t[d['kind']]}</p><div class="card-title-row{' without-image' if not visual else ''}"><div class="card-title-copy"><h2 class="{'long-name' if len(d['name']) > 15 else ''}">{esc(d['name'])}</h2></div>{visual}</div></div>
  <dl>{rows}</dl>{note}
  <a class="edit-link" href="https://github.com/rockyluke/ce-dinosaure/edit/main/{d['file']}" target="_blank" rel="noreferrer">{t['edit']} <span aria-hidden="true">↗</span></a>
</article>'''

def build():
    entries = load_entries()
    for lang, t in TEXT.items():
        path = ROOT / 'docs' / lang / 'index.html'
        page = path.read_text()
        grid = '<div class="dinosaur-grid" id="dinosaur-grid">\n' + '\n'.join(card(d, lang) for d in entries) + '\n</div>'
        count = f'<div class="summary" role="status" aria-live="polite"><strong id="entry-count">{len(entries)}</strong><span id="entry-count-label">{t["count"]}</span></div>'
        for name, content in [('CATALOG', grid), ('COUNT', count)]:
            pattern = f'<!-- {name}:START -->.*?<!-- {name}:END -->'
            page, n = re.subn(pattern, lambda _: f'<!-- {name}:START -->\n{content}\n<!-- {name}:END -->', page, flags=re.S)
            assert n == 1, f'Missing or duplicate {name} marker'
        path.write_text(page)
    # Refresh cached styles whenever the stylesheet changes, on every page.
    version = hashlib.sha256((ROOT / 'docs/styles.css').read_bytes()).hexdigest()[:12]
    for path in (ROOT / 'docs').glob('*/*.html'):
        page = re.sub(r'\.\./styles\.css(?:\?v=[a-zA-Z0-9-]+)?', f'../styles.css?v={version}', path.read_text())
        path.write_text(page)
    print(f'Built {len(entries)} entries in French and English.')

if __name__ == '__main__':
    build()
