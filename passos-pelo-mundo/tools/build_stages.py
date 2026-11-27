#!/usr/bin/env python3
"""Calcula as etapas a pé entre cidades vizinhas com um Valhalla local.

Entrada : ../data/cidades.json (GeoNames) e um Valhalla em http://localhost:8002
Saída   : ../data/etapas/grafo.json            nós e ligações (com metros)
          ../data/etapas/c_<lon>_<lat>.json    desenho das etapas, por quadrícula de 1 grau
          ../data/etapas/estatisticas.json
As etapas derivam do OpenStreetMap, por isso ficam sob a licença ODbL.
Variáveis: PAISES="PT ES" (códigos ISO), MAX_KM (150), TOL_M (15).
"""
import json, math, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from scipy.spatial import Delaunay

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')
OUT = os.path.join(DATA, 'etapas')
URL = os.environ.get('VALHALLA', 'http://localhost:8002') + '/route'
PAISES = os.environ.get('PAISES', 'PT').split()
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
    req = urllib.request.Request(URL, data=json.dumps(q).encode(), headers={'Content-Type': 'application/json'})
    try:
        j = json.load(urllib.request.urlopen(req, timeout=120))
    except Exception as e:
        return None, 'erro'
    legs = j.get('trip', {}).get('legs') or []
    if not legs: return None, 'erro'
    for m in legs[0].get('maneuvers', []):
        if m.get('type') in (28, 29) or m.get('travel_mode') == 'transit' or m.get('ferry'):
            return None, 'barco'
    return (decode(legs[0]['shape']), j['trip']['summary']['length'] * 1000.0), 'ok'

def main():
    cities = [c for c in json.load(open(os.path.join(DATA, 'cidades.json'), encoding='utf-8')) if c[3] in PAISES]
    nodes = [(c[0], c[4], c[5]) for c in cities]
    print('nós:', len(nodes), PAISES)
    pts = np.array([[n[1] * math.cos(math.radians(n[2])), n[2]] for n in nodes])
    tri = Delaunay(pts)
    pairs = set()
    for s in tri.simplices:
        for i in range(3):
            a, b = int(s[i]), int(s[(i + 1) % 3])
            if a > b: a, b = b, a
            pairs.add((a, b))
    pairs = sorted(p for p in pairs if hav(nodes[p[0]][1:], nodes[p[1]][1:]) <= MAX_M)
    print('ligações candidatas:', len(pairs))
    t0 = time.time()
    def work(p):
        a, b = nodes[p[0]][1:], nodes[p[1]][1:]
        r, st = route(a, b)
        if r is None: return p, None, st
        coords, m = r
        straight = hav(a, b)
        if m > 3 * straight + 5000: return p, None, 'desvio'
        simp = simplify(coords, TOL_M)
        return p, (simp, m), 'ok'
    with ThreadPoolExecutor(4) as ex: results = list(ex.map(work, pairs))
    print('cálculo: %.0f s' % (time.time() - t0))
    counts = {}; edges = []; chunks = {}; npts = 0
    for p, r, st in results:
        counts[st] = counts.get(st, 0) + 1
        if r is None: continue
        simp, m = r; npts += len(simp)
        edges.append([p[0], p[1], int(round(m))])
        na = nodes[p[0]]
        key = 'c_%d_%d' % (math.floor(na[1]), math.floor(na[2]))
        chunks.setdefault(key, {})['%d-%d' % (na[0], nodes[p[1]][0])] = encode(simp)
    # componentes ligadas
    parent = list(range(len(nodes)))
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for a, b, _ in edges: parent[find(a)] = find(b)
    comp = {}
    for i in range(len(nodes)): comp.setdefault(find(i), []).append(i)
    sizes = sorted((len(v) for v in comp.values()), reverse=True)
    names = {c[0]: c[1] for c in cities}
    small = [[names[nodes[i][0]] for i in v][:6] for v in sorted(comp.values(), key=len, reverse=True)[1:25]]
    for f in os.listdir(OUT):
        if f.startswith('c_') and f.endswith('.json'): os.remove(os.path.join(OUT, f))
    total = 0
    for k, v in chunks.items():
        s = json.dumps(v, separators=(',', ':')); total += len(s)
        open(os.path.join(OUT, k + '.json'), 'w').write(s)
    g = {'v': 1, 'paises': PAISES, 'nodes': [[n[0], n[1], n[2]] for n in nodes], 'edges': edges}
    json.dump(g, open(os.path.join(OUT, 'grafo.json'), 'w'), separators=(',', ':'))
    stats = {'gerado': time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime()), 'paises': PAISES, 'nos': len(nodes),
             'candidatas': len(pairs), 'resultado': counts, 'etapas': len(edges),
             'km_total': round(sum(e[2] for e in edges) / 1000), 'pontos': npts, 'bytes_desenho': total,
             'ficheiros': len(chunks), 'componentes': sizes[:15], 'grupos_isolados': small,
             'segundos': round(time.time() - t0)}
    json.dump(stats, open(os.path.join(OUT, 'estatisticas.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps(stats, ensure_ascii=False, indent=1))
    if not edges: sys.exit('nenhuma etapa calculada')

if __name__ == '__main__':
    main()
