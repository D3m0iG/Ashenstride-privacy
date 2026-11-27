#!/usr/bin/env python3
"""Calcula, de forma incremental, as etapas a pé entre cidades vizinhas.

Entrada : ../data/cidades.json (GeoNames) e um Valhalla (local, ou o servidor de demonstração)
Saída   : ../data/etapas/grafo.json            v2: nós [geonameid, lon, lat] e ligações [id, id, metros]
          ../data/etapas/c_<lon>_<lat>.json    desenho das etapas, por quadrícula de 1 grau
          ../data/etapas/falhadas.json         pares que não deram caminho a pé (barco, desvio, erro)
          ../data/etapas/estatisticas.json
As etapas derivam do OpenStreetMap, por isso ficam sob a licença ODbL.
Variáveis:
  TODOS="PT ES ..."  todos os países do grafo (a triangulação é feita sobre todos)
  PAISES="PT ES"     países deste grupo: só calcula pares com os dois extremos nestes países
  MODO=local|demo    local = Valhalla em localhost; demo = servidor de demonstração (pares que faltam, entre grupos)
  MAX_KM (150), TOL_M (15)
"""
import json, math, os, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from scipy.spatial import Delaunay

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')
OUT = os.path.join(DATA, 'etapas')
MODO = os.environ.get('MODO', 'local')
URL = os.environ.get('VALHALLA', 'https://valhalla1.openstreetmap.de' if MODO == 'demo' else 'http://localhost:8002') + '/route'
PAISES = os.environ.get('PAISES', 'PT').split()
TODOS = os.environ.get('TODOS', os.environ.get('PAISES', 'PT')).split()
MAX_M = float(os.environ.get('MAX_KM', '150')) * 1000
TOL_M = float(os.environ.get('TOL_M', '15'))
os.makedirs(OUT, exist_ok=True)

def hav(a, b):
    R = 6371008.8
    p1, p2 = math.radians(a[1]), math.radians(b[1])
    h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(b[0] - a[0]) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))

def decode(s, prec=6):
    f = 10.0 ** prec; i = 0; lat = 0; lng = 0; out = []
    while i < len(s):
        for k in (0, 1):
            shift = 0; res = 0
            while True:
                b = ord(s[i]) - 63; i += 1
                res |= (b & 0x1f) << shift; shift += 5
                if b < 0x20: break
            d = ~(res >> 1) if res & 1 else res >> 1
            if k == 0: lat += d
            else: lng += d
        out.append((lng / f, lat / f))
    return out

def encode(coords, prec=5):
    f = 10 ** prec; out = []; pl = 0; pg = 0
    def enc(v):
        v = ~(v << 1) if v < 0 else v << 1
        while v >= 0x20:
            out.append(chr((0x20 | (v & 0x1f)) + 63)); v >>= 5
        out.append(chr(v + 63))
    for lng, lat in coords:
        a = int(round(lat * f)); g = int(round(lng * f))
        enc(a - pl); enc(g - pg); pl = a; pg = g
    return ''.join(out)

def simplify(coords, tol_m):
    """Douglas-Peucker em metros (projeção local simples)."""
    n = len(coords)
    if n < 3: return coords
    k = math.cos(math.radians(coords[0][1])) * 111320.0
    xs = [c[0] * k for c in coords]; ys = [c[1] * 110540.0 for c in coords]
    keep = [False] * n; keep[0] = keep[-1] = True
    stack = [(0, n - 1)]
    while stack:
        a, b = stack.pop()
        if b <= a + 1: continue
        ax, ay, bx, by = xs[a], ys[a], xs[b], ys[b]
        dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy
        best = -1.0; bi = -1
        for i in range(a + 1, b):
            if L2 == 0: d = (xs[i] - ax) ** 2 + (ys[i] - ay) ** 2
            else:
                t = ((xs[i] - ax) * dx + (ys[i] - ay) * dy) / L2
                t = 0 if t < 0 else 1 if t > 1 else t
                d = (xs[i] - ax - t * dx) ** 2 + (ys[i] - ay - t * dy) ** 2
            if d > best: best = d; bi = i
        if best > tol_m * tol_m:
            keep[bi] = True; stack.append((a, bi)); stack.append((bi, b))
    return [c for c, k_ in zip(coords, keep) if k_]

def route(a, b):
    q = {'locations': [{'lon': a[0], 'lat': a[1]}, {'lon': b[0], 'lat': b[1]}], 'costing': 'pedestrian',
         'costing_options': {'pedestrian': {'use_ferry': 0}}, 'units': 'kilometers', 'directions_type': 'maneuvers'}
    for tentativa in range(3):
        req = urllib.request.Request(URL, data=json.dumps(q).encode(), headers={'Content-Type': 'application/json', 'User-Agent': 'PassosPeloMundo-build/1.0'})
        try:
            if MODO == 'demo' and 'openstreetmap.de' in URL: time.sleep(0.6)
            j = json.load(urllib.request.urlopen(req, timeout=120))
            break
        except urllib.error.HTTPError as e:
            if e.code == 400: return None, 'erro'
            time.sleep(5 * (tentativa + 1))
        except Exception:
            time.sleep(5 * (tentativa + 1))
    else:
        return None, 'erro'
    legs = j.get('trip', {}).get('legs') or []
    if not legs: return None, 'erro'
    for m in legs[0].get('maneuvers', []):
        if m.get('type') in (28, 29) or m.get('travel_mode') == 'transit' or m.get('ferry'):
            return None, 'barco'
    return (decode(legs[0]['shape']), j['trip']['summary']['length'] * 1000.0), 'ok'

def chunk_name(lon, lat): return 'c_%d_%d' % (math.floor(lon), math.floor(lat))

def main():
    allc = [c for c in json.load(open(os.path.join(DATA, 'cidades.json'), encoding='utf-8')) if c[3] in TODOS]
    allc.sort(key=lambda c: c[0])
    nodes = [(c[0], c[4], c[5], c[3]) for c in allc]
    byg = {n[0]: i for i, n in enumerate(nodes)}
    print('nós:', len(nodes), 'grupo:', PAISES, 'modo:', MODO)
    gpath = os.path.join(OUT, 'grafo.json')
    old = {}
    if os.path.exists(gpath):
        try: old = json.load(open(gpath))
        except Exception: old = {}
    edges = {}
    if old.get('v') == 2:
        for a, b, m in old['edges']: edges[(a, b)] = m
    else:  # formato antigo (v1): recomeçar do zero
        for f in os.listdir(OUT):
            if f.startswith('c_') and f.endswith('.json'): os.remove(os.path.join(OUT, f))
    fpath = os.path.join(OUT, 'falhadas.json')
    failed = json.load(open(fpath)) if (os.path.exists(fpath) and old.get('v') == 2) else {}
    pts = np.array([[n[1] * math.cos(math.radians(n[2])), n[2]] for n in nodes])
    tri = Delaunay(pts)
    pairs = set()
    for s in tri.simplices:
        for i in range(3):
            a, b = int(s[i]), int(s[(i + 1) % 3])
            if a > b: a, b = b, a
            pairs.add((a, b))
    pairs = sorted(p for p in pairs if hav(nodes[p[0]][1:3], nodes[p[1]][1:3]) <= MAX_M)
    print('ligações candidatas (todas):', len(pairs))
    covered = set()
    for (ga, gb) in edges:
        covered.add(nodes[byg[ga]][3]); covered.add(nodes[byg[gb]][3])
    todo = []
    for p in pairs:
        ga, gb = nodes[p[0]][0], nodes[p[1]][0]; key = '%d-%d' % (ga, gb)
        if (ga, gb) in edges: continue
        if MODO == 'local':
            if nodes[p[0]][3] not in PAISES or nodes[p[1]][3] not in PAISES: continue
            if key in failed and failed[key] in ('barco', 'desvio'): continue
        else:
            if nodes[p[0]][3] not in covered or nodes[p[1]][3] not in covered: continue
            if key in failed and failed[key] in ('barco', 'desvio'): continue
        todo.append(p)
    if MODO == 'demo' and len(todo) > int(os.environ.get('MAX_DEMO', '5000')): sys.exit('demasiados pares para o servidor de demonstração: %d' % len(todo))
    print('a calcular agora:', len(todo))
    t0 = time.time()
    def work(p):
        a, b = nodes[p[0]][1:3], nodes[p[1]][1:3]
        r, st = route(a, b)
        if r is None: return p, None, st
        coords, m = r
        if m > 3 * hav(a, b) + 5000: return p, None, 'desvio'
        return p, (simplify(coords, TOL_M), m), 'ok'
    with ThreadPoolExecutor(2 if MODO == 'demo' else 4) as ex: results = list(ex.map(work, todo))
    print('cálculo: %.0f s' % (time.time() - t0))
    counts = {}; chunks = {}; npts = 0
    for p, r, st in results:
        ga, gb = nodes[p[0]][0], nodes[p[1]][0]; key = '%d-%d' % (ga, gb)
        counts[st] = counts.get(st, 0) + 1
        if r is None: failed[key] = st; continue
        failed.pop(key, None)
        simp, m = r; npts += len(simp)
        edges[(ga, gb)] = int(round(m))
        chunks.setdefault(chunk_name(nodes[p[0]][1], nodes[p[0]][2]), {})[key] = encode(simp)
    for name, add in chunks.items():
        fp = os.path.join(OUT, name + '.json')
        cur = json.load(open(fp)) if os.path.exists(fp) else {}
        cur.update(add)
        open(fp, 'w').write(json.dumps(cur, separators=(',', ':')))
    elist = [[a, b, m] for (a, b), m in sorted(edges.items())]
    # só guarda nós que existem no grafo de países pedido (todos os de TODOS)
    g = {'v': 2, 'nodes': [[n[0], n[1], n[2]] for n in nodes], 'edges': elist}
    json.dump(g, open(gpath, 'w'), separators=(',', ':'))
    json.dump(failed, open(fpath, 'w'), separators=(',', ':'))
    # estatísticas do grafo completo
    parent = list(range(len(nodes)))
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for a, b, _ in elist:
        if a in byg and b in byg: parent[find(byg[a])] = find(byg[b])
    comp = {}
    for i in range(len(nodes)): comp.setdefault(find(i), []).append(i)
    big = sorted(comp.values(), key=len, reverse=True)
    names = {c[0]: c[1] for c in allc}
    total_bytes = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT) if f.startswith('c_'))
    stats = {'gerado': time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime()), 'ultimo_grupo': PAISES, 'modo': MODO,
             'paises_no_grafo': TODOS, 'nos': len(nodes), 'etapas': len(elist),
             'km_total': round(sum(e[2] for e in elist) / 1000), 'bytes_desenho': total_bytes,
             'esta_corrida': counts, 'falhadas_total': len(failed), 'componentes': [len(c) for c in big[:15]],
             'grupos_isolados': [[names[nodes[i][0]] for i in c][:4] for c in big[1:30] if len(c) > 1],
             'segundos': round(time.time() - t0)}
    json.dump(stats, open(os.path.join(OUT, 'estatisticas.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps(stats, ensure_ascii=False, indent=1))
    if not elist: sys.exit('nenhuma etapa')

if __name__ == '__main__':
    main()
