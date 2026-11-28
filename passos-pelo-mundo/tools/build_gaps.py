#!/usr/bin/env python3
"""Acrescenta a data/travessias.json as ligações que faltam no grafo de etapas:
 - curadas: mar (4 elementos) e ligações virtuais 'g' (deserto/zonas sem estradas, 5.º elemento);
 - automáticas: cada componente solto liga-se ao ponto mais próximo de outro componente
   ('r' = reta a pé até 40 km, 'g' = ligação virtual acima disso, até MAX_AUTO_KM).
Idempotente: remove primeiro as ligações 'g' e 'r' geradas antes."""
import json, math, os, collections
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
cities = json.load(open(os.path.join(DATA, 'cidades.json'), encoding='utf-8'))
g = json.load(open(os.path.join(DATA, 'etapas', 'grafo.json')))
nodes = g['nodes']; edges = g['edges']
byg = {c[0]: c for c in cities}
tp = os.path.join(DATA, 'travessias.json')
cur = json.load(open(tp, encoding='utf-8'))
cur['links'] = [l for l in cur['links'] if len(l) < 5]  # tira 'g'/'r' antigos
MAX_AUTO_KM = 1500
SEA = [('Mahajanga','MG','Pemba','MZ'), ('Toamasina','MG','Port Louis','MU'), ('Moroni','KM','Mahajanga','MG'),
 ('Moroni','KM','Moutsamoudou','KM'), ('Moroni','KM','Fomboni','KM'), ('Victoria','SC','Mombasa','KE'),
 ('Dar es Salaam','TZ','Zanzibar','TZ'), ('Zanzibar','TZ','Chake Chake','TZ'), ('Kilindoni','TZ','Dar es Salaam','TZ'),
 ('Nansio','TZ','Mwanza','TZ'), ('Kirando','TZ','Kigoma','TZ'), ('Lamu','KE','Mombasa','KE'),
 ('Praia','CV','Dakar','SN'), ('Praia','CV','Mindelo','CV'), ('Mindelo','CV','Espargos','CV'),
 ('Santa Cruz de Tenerife','ES','Las Palmas de Gran Canaria','ES'), ('Las Palmas de Gran Canaria','ES','Puerto del Carmen','ES'),
 ('Malabo','GQ','Douala','CM'), ('Port-Gentil','GA','Libreville','GA')]
GAP = [('Cairo','EG','Wadi Halfa','SD'), ('Wadi Halfa','SD','Khartoum','SD'), ('Ghardaïa','DZ','Tamanghasset','DZ'),
 ('Tamanghasset','DZ','Agadez','NE'), ('Dakhla','MA','Nouadhibou','MR'), ('Nouadhibou','MR','Nouakchott','MR'),
 ('Alexandria','EG','Tobruk','LY'), ('Benghazi','LY','Sirte','LY'), ('Al Jawf','LY','Benghazi','LY'),
 ('Brazzaville','CG','Mindouli','CG'), ('Kinshasa','CD','Mbandaka','CD'), ('Mbandaka','CD','Lisala','CD'), ('Lisala','CD','Kisangani','CD'),
 ('Kinshasa','CD','Nioki','CD'), ('Lubumbashi','CD','Manono','CD')]
ing = {n[0] for n in nodes}
def find(name, cc):
    n = name.lower(); best = None
    for c in cities:
        if c[3] != cc or c[0] not in ing: continue
        if c[2].lower() == n or c[1].lower() == n:
            if not best or c[6] > best[6]: best = c
    if not best:
        for c in cities:
            if c[3] == cc and c[0] in ing and (n in c[2].lower() or n in c[1].lower()):
                if not best or c[6] > best[6]: best = c
    return best
def hav(lo1, la1, lo2, la2):
    R = 6371000; p1 = math.radians(la1); p2 = math.radians(la2)
    dl = math.radians(lo2 - lo1); dp = p2 - p1
    h = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(h))
idx = {n[0]: i for i, n in enumerate(nodes)}
par = list(range(len(nodes)))
def f(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
def un(a, b): par[f(a)] = f(b)
for a, b, m in edges: un(idx[a], idx[b])
grid = collections.defaultdict(list)
for i, n in enumerate(nodes): grid[(int(math.floor(n[1])), int(math.floor(n[2])))].append(i)
def snap(lo, la):
    best = None; bd = 25000
    for i in grid.get((int(math.floor(lo)), int(math.floor(la))), []) + [j for k in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(-1,1),(1,-1)] for j in grid.get((int(math.floor(lo))+k[0], int(math.floor(la))+k[1]), [])]:
        d = hav(lo, la, nodes[i][1], nodes[i][2])
        if d < bd: bd = d; best = i
    return best
for t in cur['links']:
    a = snap(*t[1]); b = snap(*t[3])
    if a is not None and b is not None: un(a, b)
added = collections.Counter(); miss = []
def add(A, B, kind):
    link = [A[2], [A[4], A[5]], B[2], [B[4], B[5]]]
    if kind: link.append(kind)
    cur['links'].append(link); un(idx[A[0]], idx[B[0]]); added[kind or 'mar'] += 1
for lst, kind in ((SEA, None), (GAP, 'g')):
    for a, ca, b, cb in lst:
        A, B = find(a, ca), find(b, cb)
        if not A or not B: miss.append((a, ca, b, cb, bool(A), bool(B))); continue
        add(A, B, kind)
def comps():
    d = collections.defaultdict(list)
    for i in range(len(nodes)): d[f(i)].append(i)
    return sorted(d.values(), key=len)
def nearest_outside(c):
    inside = set(f(i) for i in c); root = f(c[0]); best = (1e18, None, None)
    for i in c:
        lo, la = nodes[i][1], nodes[i][2]; cx, cy = int(math.floor(lo)), int(math.floor(la))
        for r in range(0, 16):
            found = False
            for x in range(cx - r, cx + r + 1):
                for y in range(cy - r, cy + r + 1):
                    if max(abs(x - cx), abs(y - cy)) != r: continue
                    for j in grid.get((x, y), []):
                        if f(j) == root: continue
                        d = hav(lo, la, nodes[j][1], nodes[j][2])
                        if d < best[0]: best = (d, i, j)
            if best[1] is not None and best[0] < r * 90000: break
    return best
while True:
    cs = comps()
    if len(cs) <= 1: break
    done = False
    for c in cs[:-1]:
        d, i, j = nearest_outside(c)
        if i is None or d > MAX_AUTO_KM * 1000: continue
        A, B = byg[nodes[i][0]], byg[nodes[j][0]]
        add(A, B, 'r' if d <= 40000 else 'g'); done = True; break
    if not done: break
cur['nota'] = 'Travessias marítimas e ligações virtuais instantâneas (5.º elemento: g = virtual, r = reta a pé); sem 5.º elemento = mar.'
json.dump(cur, open(tp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
cs = comps()
print('acrescentadas:', dict(added), 'total:', len(cur['links']), 'em falta:', miss)
print('componentes:', [len(c) for c in cs[::-1][:10]], 'total', len(cs))
