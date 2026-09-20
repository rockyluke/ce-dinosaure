"""Build bilingual static cards from JSON front matter in Markdown files (stdlib only)."""
import json
import re
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT = {
    'fr': dict(alias='Alias', period='Période', locations='Lieux', length='Longueur', wingspan='Envergure', weight='Poids', diet='Régime', sources='Sources', edit='Éditer cette fiche', missing='À compléter', dinosaur='Dinosaure', jurassic='Jurassique', cretaceous='Crétacé', triassic='Trias', herbivore='Herbivore', carnivore='Carnivore', omnivore='Omnivore', unknown='Incertain', genus='Genre', count='fiches'),
    'en': dict(alias='Aliases', period='Period', locations='Locations', length='Length', wingspan='Wingspan', weight='Weight', diet='Diet', sources='Sources', edit='Edit this entry', missing='To be completed', dinosaur='Dinosaur', jurassic='Jurassic', cretaceous='Cretaceous', triassic='Triassic', herbivore='Herbivore', carnivore='Carnivore', omnivore='Omnivore', unknown='Uncertain', genus='Genus', count='entries'),
}

def load_entries():
    entries = []
    for path in sorted((ROOT / 'content').glob('*/*.md')):
        data = json.loads(path.read_text().split('---', 2)[1])
        assert data['period'] in {'triassic', 'jurassic', 'cretaceous'}
        assert data['diet'] in {'herbivore', 'carnivore', 'omnivore', 'unknown'}
        assert data['category'] in {'real', 'fictional'}
        assert data['kind'] == 'dinosaur'
        assert data['measurement'] in {'length', 'wingspan'}
        assert data['sources'] and all(s['url'].startswith('https://') for s in data['sources'])
        data['file'] = path.relative_to(ROOT).as_posix()
        entries.append(data)
    assert len({d['name'] for d in entries}) == len(entries), 'Duplicate genus'
    return entries

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
    rows += f'<div><dt>{t["period"]}</dt><dd><a class="period-link" href="periods.html#{d["period"]}">{t[d["period"]]}</a></dd></div>'
    rows += row('locations', d[f'locations_{lang}'])
    rows += row(d['measurement'], measure(d['length_m'], 'm'))
    rows += row('weight', measure(d['weight_kg'], 'kg')) + row('diet', t[d['diet']])
    links = ' '.join(f'<a href="{esc(s["url"])}" target="_blank" rel="noreferrer">{esc(s["label"])} ↗</a>' for s in d['sources'])
    rows += f'<div class="source-row"><dt>{t["sources"]}</dt><dd class="sources">{links}</dd></div>'
    aliases = ' '.join([d['name'], d['aliases_fr'], d['aliases_en']])
    attrs = ' '.join(f'data-{k}="{esc(v, quote=True)}"' for k, v in {'search': aliases, 'period': d['period'], 'diet': d['diet'], 'category': d['category']}.items())
    note = f'<p class="card-note">{esc(d.get("note_" + lang, ""))}</p>' if d.get('note_' + lang) else ''
    image = d.get('image')
    visual = ''
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
    return f'''<article class="dinosaur-card" {attrs}>
  <div class="card-heading"><p class="kind-label">{t[d['kind']]}</p><div class="card-title-row"><div class="card-title-copy"><h2 class="{'long-name' if len(d['name']) > 15 else ''}">{esc(d['name'])}</h2><p class="scientific">{t['genus']} : {esc(d['name'])}</p></div>{visual}</div></div>
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
    print(f'Built {len(entries)} entries in French and English.')

if __name__ == '__main__':
    build()
