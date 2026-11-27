#!/usr/bin/env python3
"""Gera as listas mundiais de cidades e monumentos do jogo Passos pelo Mundo.

Fontes:
  - GeoNames (CC BY 4.0): cidades com mais de 15 000 habitantes + nomes em português.
  - Wikidata (CC0): monumentos e locais de interesse com muita notoriedade
    (medida pelo número de edições da Wikipédia onde existem) + Património Mundial da UNESCO.
Só usa a biblioteca padrão do Python. Escreve em ../data/.
"""
import csv, io, json, os, sys, time, urllib.parse, urllib.request, zipfile

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
UA = 'PassosPeloMundo-build/1.0 (https://github.com/D3m0iG/Ashenstride-privacy)'
os.makedirs(OUT, exist_ok=True)

def get(url, timeout=600, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
            return urllib.request.urlopen(req, timeout=timeout).read()
        except Exception as e:
            print('  falha', i + 1, url[:90], e, file=sys.stderr)
            time.sleep(5 * (i + 1))
    raise RuntimeError('não consegui obter ' + url)

# ------------------------------------------------------------------ cidades
def build_cities():
    print('GeoNames: cidades…')
    z = zipfile.ZipFile(io.BytesIO(get('https://download.geonames.org/export/dump/cities15000.zip')))
    rows = []
    with z.open('cities15000.txt') as f:
        for r in csv.reader(io.TextIOWrapper(f, encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
            if len(r) < 15: continue
            rows.append({'id': int(r[0]), 'name': r[1], 'lat': float(r[4]), 'lon': float(r[5]),
                         'fc': r[7], 'cc': r[8], 'pop': int(r[14] or 0)})
    ids = {r['id'] for r in rows}
    print('  cidades:', len(rows), '— a ler nomes em português…')
    pt = {}
    zb = zipfile.ZipFile(io.BytesIO(get('https://download.geonames.org/export/dump/alternateNamesV2.zip', timeout=1800)))
    with zb.open('alternateNamesV2.txt') as f:
        for line in io.TextIOWrapper(f, encoding='utf-8'):
            p = line.rstrip('\n').split('\t')
            if len(p) < 9 or p[2] not in ('pt', 'pt-PT', 'pt-BR'): continue
            gid = int(p[1]) if p[1].isdigit() else 0
            if gid not in ids: continue
            if p[6] == '1' or p[7] == '1': continue  # coloquial ou histórico
            score = (2 if p[2] == 'pt-PT' else 1 if p[2] == 'pt' else 0) * 2 + (1 if p[4] == '1' else 0)
            if gid not in pt or score > pt[gid][0]: pt[gid] = (score, p[3])
    out = []
    for r in sorted(rows, key=lambda x: -x['pop']):
        n_pt = pt.get(r['id'], (0, r['name']))[1]
        out.append([r['id'], n_pt, r['name'], r['cc'], round(r['lon'], 4), round(r['lat'], 4), r['pop'], 1 if r['fc'] == 'PPLC' else 0])
    json.dump(out, open(os.path.join(OUT, 'cidades.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('  escrito cidades.json:', len(out), 'cidades,', sum(1 for o in out if o[7]), 'capitais')
    return out

# ---------------------------------------------------------------- monumentos
CLASSES = {
    'Q570116': 'atração turística', 'Q2319498': 'marco', 'Q4989906': 'monumento', 'Q23413': 'castelo',
    'Q16560': 'palácio', 'Q2977': 'catedral', 'Q16970': 'igreja', 'Q44539': 'templo', 'Q32815': 'mesquita',
    'Q33506': 'museu', 'Q12280': 'ponte', 'Q12518': 'torre', 'Q839954': 'sítio arqueológico',
    'Q179700': 'estátua', 'Q1081138': 'sítio histórico', 'Q57821': 'fortaleza', 'Q39715': 'farol',
}

def sparql(q):
    url = 'https://query.wikidata.org/sparql?format=json&query=' + urllib.parse.quote(q)
    for i in range(4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/sparql-results+json'})
            return json.load(urllib.request.urlopen(req, timeout=120))['results']['bindings']
        except Exception as e:
            print('  falha SPARQL', i + 1, e, file=sys.stderr); time.sleep(15 * (i + 1))
    return None

def one(b, k): return b.get(k, {}).get('value')

def build_monuments():
    print('Wikidata: monumentos…')
    found = {}
    def run(label, where, minsl):
        q = ('SELECT ?item ?coord ?sl ?lpt ?len ?cc WHERE { %s ?item wdt:P625 ?coord ; wikibase:sitelinks ?sl . '
             'FILTER(?sl >= %d) OPTIONAL{?item rdfs:label ?lpt FILTER(lang(?lpt)="pt")} '
             'OPTIONAL{?item rdfs:label ?len FILTER(lang(?len)="en")} '
             'OPTIONAL{?item wdt:P17/wdt:P297 ?cc} }') % (where, minsl)
        res = sparql(q)
        if res is None: print('  SALTADO:', label); return 0
        n = 0
        for b in res:
            qid = one(b, 'item').rsplit('/', 1)[-1]
            c = one(b, 'coord') or ''
            if not c.startswith('Point('): continue
            lon, lat = [float(x) for x in c[6:-1].split()]
            en = one(b, 'len'); pt = one(b, 'lpt') or en
            if not (en or pt): continue
            if qid not in found:
                found[qid] = [qid, pt or en, en or pt, one(b, 'cc') or '', round(lon, 4), round(lat, 4), int(one(b, 'sl')), label]
                n += 1
        print('  %-20s +%d' % (label, n)); time.sleep(3); return n
    counts = {}
    counts['UNESCO'] = run('UNESCO', '?item wdt:P1435 wd:Q9259 .', 12)
    for qid, nome in CLASSES.items():
        counts[nome] = run(nome, '?item wdt:P31 wd:%s .' % qid, 30)
    out = sorted(found.values(), key=lambda x: -x[6])[:6000]
    json.dump(out, open(os.path.join(OUT, 'monumentos.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('  escrito monumentos.json:', len(out))
    json.dump(counts, open(os.path.join(OUT, 'monumentos_por_classe.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return out

if __name__ == '__main__':
    c = build_cities()
    m = build_monuments()
    stats = {'gerado': time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime()), 'cidades': len(c),
             'capitais': sum(1 for o in c if o[7]), 'monumentos': len(m),
             'monumentos_sem_pais': sum(1 for o in m if not o[3])}
    json.dump(stats, open(os.path.join(OUT, 'estatisticas.json'), 'w'), ensure_ascii=False, indent=1)
    open(os.path.join(OUT, 'ATRIBUICAO.txt'), 'w', encoding='utf-8').write(
        'Cidades: GeoNames (https://www.geonames.org), licença CC BY 4.0.\n'
        'Monumentos: Wikidata (https://www.wikidata.org), CC0.\n')
    print(stats)
