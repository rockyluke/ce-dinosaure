"""Draw original, schematic SVG silhouettes for entries without NHM artwork.

Coordinates describe body plans, not fossil reconstructions. Human comparisons
use a 1.75 m adult and the card's stated length or wingspan (midpoint of ranges).
No human or implied scale is added when the card has no measurement.
"""
import json
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'docs/assets/original-silhouettes'
# Original outlines: all animal forms occupy x=0..300, facing right.
TAIL_BODY = 'M0 55 Q45 68 100 35 Q130 18 175 32 L207 25 '
SHAPES = {
 'theropod': TAIL_BODY + 'L227 10 L266 10 L288 21 L300 25 L298 34 L262 39 L243 34 L218 52 L232 63 L247 68 L241 73 L221 68 L202 59 L183 66 L171 86 L183 92 L190 98 L157 98 L155 87 L164 66 L141 64 L132 83 L119 94 L132 97 L106 98 L103 91 L119 75 L120 58 Q64 82 0 55 Z',
 'raptor': 'M0 52 Q63 60 111 33 Q144 20 178 33 L222 14 L247 10 L282 19 L300 25 L296 32 L258 35 L237 31 L210 48 L234 57 L254 76 L228 64 L205 60 L187 57 L172 77 L186 88 L185 96 L163 96 L158 91 L161 77 L146 63 L128 76 L111 91 L124 95 L104 98 L96 91 L119 67 L116 53 Q59 71 0 52 Z',
 'hadrosaur': 'M0 45 Q62 65 104 36 Q144 18 183 31 L216 23 L240 14 L263 17 L280 30 L300 33 L298 42 L272 44 L251 37 L226 45 L209 58 L213 79 L224 94 L213 97 L202 90 L188 63 L169 66 L163 84 L177 95 L160 98 L149 88 L143 67 L123 59 Q64 77 0 45 Z',
 'sauropod': 'M0 67 Q49 72 85 47 Q113 26 151 44 Q175 48 182 32 L201 5 Q207 0 223 0 L242 5 L245 12 L226 16 L216 12 L207 43 Q203 57 186 65 L184 91 L192 97 L173 98 L168 72 L152 69 L144 91 L151 97 L134 98 L128 70 L111 66 L105 91 L111 97 L93 98 L87 70 Q40 82 0 67 Z M245 5 L300 5 L300 6 L245 6 Z',
 'ceratopsian': 'M0 55 Q40 59 76 41 Q118 22 170 38 L191 14 L202 30 L209 18 L218 35 L229 37 L250 14 L248 39 L269 42 L282 29 L280 49 L300 57 L289 68 L269 68 L252 61 L229 69 L216 72 L215 91 L225 96 L205 98 L197 73 L169 75 L162 93 L172 98 L151 98 L145 72 L104 66 L96 89 L106 95 L86 97 L79 65 Q40 66 0 55 Z',
 'small_ceratopsian': 'M0 48 Q52 62 98 38 Q139 21 177 40 L195 22 L211 29 L220 38 L254 40 L282 47 L300 57 L290 67 L265 67 L242 59 L218 64 L207 83 L216 94 L199 96 L187 69 L163 68 L152 88 L164 96 L143 98 L133 88 L134 64 L113 57 Q58 72 0 48 Z',
 'ankylosaur': 'M0 63 L52 57 L82 39 L95 44 L109 29 L120 37 L137 25 L149 34 L166 29 L181 39 L203 38 L219 51 L244 48 L264 53 L278 51 L300 64 L290 74 L259 76 L240 69 L223 72 L220 88 L229 96 L212 97 L199 76 L165 75 L160 91 L170 97 L150 98 L141 78 L112 76 L106 91 L114 98 L95 98 L87 73 L61 66 L0 63 Z',
 'stegosaur': 'M0 64 L43 60 L58 49 L73 55 L79 31 L95 44 L107 12 L126 34 L141 3 L156 32 L178 7 L186 39 L207 23 L211 52 L243 55 L273 64 L300 67 L299 74 L278 79 L248 71 L228 73 L224 92 L233 98 L213 98 L204 72 L170 71 L165 93 L177 98 L154 98 L148 76 L117 68 L109 91 L119 98 L98 98 L92 70 L44 68 L0 64 Z',
 'mosasaur': 'M0 57 L19 34 L36 46 Q78 58 107 42 Q155 19 211 43 L243 36 L286 44 L300 52 L294 61 L250 62 L228 57 L206 66 L197 88 L174 98 L181 70 L146 67 L126 83 L102 87 L113 65 Q67 62 38 59 L20 75 Z',
 'pliosaur': 'M0 54 Q39 46 78 49 Q100 31 148 40 L180 46 L212 32 L258 35 L300 50 L295 62 L255 69 L210 62 L179 64 L150 73 L144 95 L118 98 L128 71 L102 65 L79 87 L54 91 L67 64 L0 54 Z',
 'plesiosaur': 'M0 64 Q35 51 62 55 Q85 44 111 52 Q141 57 174 37 Q213 9 260 18 L279 14 L300 22 L298 29 L275 32 L262 28 Q225 22 186 52 Q153 76 123 73 L113 94 L87 98 L98 71 L71 70 L46 91 L23 94 L44 69 L0 64 Z',
 'ichthyosaur': 'M0 28 L25 50 Q59 45 95 40 L119 16 L136 35 Q174 31 220 45 L253 45 L300 54 L253 59 L228 62 L194 68 L177 91 L153 97 L162 72 L113 70 Q60 70 26 59 L0 83 L12 56 Z',
 'crocodile': 'M0 62 Q61 45 107 49 L113 43 L126 48 L136 41 L148 48 L162 43 L175 51 L221 51 L242 44 L260 45 L273 51 L300 54 L300 62 L273 67 L239 66 L217 68 L224 83 L243 88 L219 93 L202 77 L168 74 L124 73 L105 88 L82 90 L89 79 L106 68 Q62 69 0 62 Z',
 'dimetrodon': 'M0 68 Q48 67 76 53 Q91 36 98 21 L105 35 L116 9 L124 28 L137 0 L145 22 L158 5 L167 29 L181 18 L189 40 L202 44 L221 43 L234 33 L260 36 L281 47 L300 54 L294 65 L262 69 L239 61 L218 69 L233 87 L252 92 L232 98 L213 86 L198 73 L164 74 L131 71 L109 87 L117 98 L94 95 L89 84 L103 67 Q54 77 0 68 Z',
 # Front views: total width is wingspan, not body length.
 'pterosaur': 'M0 9 Q75 40 130 41 L143 33 L146 14 L152 1 L155 14 L158 33 L170 41 Q225 40 300 9 L258 55 L214 66 L178 58 L159 51 L161 71 L171 88 L161 93 L151 76 L141 93 L130 88 L143 71 L141 51 L123 58 L86 66 L42 55 Z',
}
# Replace the artificial sauropod extent with a natural long neck and head.
SHAPES['sauropod'] = SHAPES['sauropod'].split(' M245')[0].replace('L242 5 L245 12 L226 16 L216 12','L290 5 L300 11 L296 18 L275 18 L260 12 L216 12')
GROUPS = {
 'hadrosaur':'jinzhousaurus eolambia tanius equijubus nipponosaurus',
 'sauropod':'lapparentosaurus isisaurus', 'ceratopsian':'zuniceratops',
 'small_ceratopsian':'liaoceratops graciliceratops udanoceratops',
 'ankylosaur':'shamosaurus tsagantegia', 'stegosaur':'yingshanosaurus',
 'raptor':'pyroraptor troodon indoraptor', 'theropod':'dubreuillosaurus indominus-rex scorpios-rex',
 'mosasaur':'mosasaurus tylosaurus', 'pliosaur':'kronosaurus',
 'plesiosaur':'plesiosaurus elasmosaurus', 'ichthyosaur':'mixosaurus',
 'crocodile':'sarcosuchus', 'dimetrodon':'dimetrodon', 'pterosaur':'pterodactylus quetzalcoatlus',
}
# Original standing adult, y=0..175; 100 SVG units represent one metre.
HUMAN = '<circle cx="16" cy="10" r="10"/><path d="M8 23 Q16 19 24 23 L31 51 L34 79 L28 81 L23 54 L23 87 L27 130 L30 170 L38 175 L23 175 L18 133 L15 103 L12 133 L9 175 L0 175 L3 169 L4 127 L6 86 L6 52 L1 80 L-5 78 L0 48 Z"/>'

def build():
 DEST.mkdir(parents=True,exist_ok=True); manifest={}
 for shape,slugs in GROUPS.items():
  for slug in slugs.split():
   matches=list((ROOT/'content').glob(f'*/{slug}.md'));assert len(matches)==1
   d=json.loads(matches[0].read_text().split('---',2)[1]);assert not d.get('image')
   outline=SHAPES[shape]
   # Distinguishing crests, feathers and dorsal spines remain schematic.
   if slug=='zuniceratops':outline=outline.replace('L269 42 L282 29 L280 49', 'L269 42 L280 49')
   extra=''
   if slug in {'indominus-rex','scorpios-rex'}:extra='<path d="M103 33 L107 22 L117 29 L123 17 L132 25 L140 14 L149 25 L157 16 L165 29 L174 22 L181 35 Z"/>'
   if slug=='pyroraptor':extra='<path d="M205 49 L223 47 L220 56 L241 62 L233 70 L254 76 L224 70 L204 60 Z"/>'
   if slug=='nipponosaurus':extra='<path d="M236 18 Q225 -1 248 0 L256 17 Z"/>'
   if slug=='quetzalcoatlus':extra='<path d="M146 16 L137 1 L157 8 L159 28 Z"/>'
   size=d['length_m'];length=sum(map(float,size.split('–')))/len(size.split('–')) if size else None
   human='';width=300;height=105
   if length:
    scale=300/(length*100);hh=175*scale;hw=43*scale
    height=max(105,hh);width=312+hw
    human=f'<g transform="translate({312+5*scale:.4f} {height-hh:.4f}) scale({scale:.5f})">{HUMAN}</g>'
   label=f"{d['name']} — original schematic silhouette"+(' with a 1.75 m human' if length else ', not to scale')
   art=f'<g transform="translate(0 {height-100:.4f})"><path d="{outline}"/>{extra}</g>'
   svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 -6 {width+12:.4f} {height+12:.4f}" role="img"><title>{escape(label)}</title><desc>Original artwork for ce-dinosaure.fr. Schematic body plan, not an anatomical reconstruction. '+('Comparison uses the stated '+d['measurement']+'; range midpoint when applicable.' if length else 'No documented measurement; no human comparison.')+f'</desc><g fill="#56734c">{art}{human}</g></svg>\n'
   (DEST/f'{slug}.svg').write_text(svg)
   manifest[slug]=dict(file=f'assets/original-silhouettes/{slug}.svg',mode='comparison' if length else 'silhouette',measurement=d['measurement'],reference_m=length,body_shape=shape)
 (DEST/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 print(f'Drew {len(manifest)} original silhouettes.')
if __name__=='__main__':build()
