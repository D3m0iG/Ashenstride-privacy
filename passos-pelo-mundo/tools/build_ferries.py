#!/usr/bin/env python3
"""Acrescenta as travessias marítimas da Europa a data/travessias.json (por nome de cidade).
Cada par liga duas cidades do grafo; o jogo atravessa o mar instantaneamente entre elas."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
cities = json.load(open(os.path.join(DATA, 'cidades.json'), encoding='utf-8'))
PAIRS = [
 # Canal da Mancha, Mar do Norte e Atlântico
 ('Dover','GB','Calais','FR'), ('Portsmouth','GB','Le Havre','FR'), ('Portsmouth','GB','Caen','FR'),
 ('Hull','GB','Rotterdam','NL'), ('Newcastle upon Tyne','GB','Amsterdam','NL'), ('Harwich','GB','Rotterdam','NL'),
 ('Plymouth','GB','Santander','ES'), ('Liverpool','GB','Dublin','IE'), ('Liverpool','GB','Belfast','GB'),
 ('Swansea','GB','Cork','IE'), ('Dublin','IE','Cherbourg','FR'), ('Portsmouth','GB','Ryde','GB'), ('Southampton','GB','Cowes','GB'),
 # Escandinávia e Báltico
 ('Helsingør','DK','Helsingborg','SE'), ('Copenhagen','DK','Malmö','SE'), ('Slagelse','DK','Odense','DK'),
 ('Rostock','DE','Trelleborg','SE'), ('Karlskrona','SE','Gdynia','PL'), ('Ystad','SE','Świnoujście','PL'),
 ('Stockholm','SE','Helsinki','FI'), ('Stockholm','SE','Tallinn','EE'), ('Helsinki','FI','Tallinn','EE'),
 ('Stockholm','SE','Turku','FI'), ('Stockholm','SE','Riga','LV'), ('Kiel','DE','Gothenburg','SE'),
 ('Copenhagen','DK','Oslo','NO'), ('Frederikshavn','DK','Gothenburg','SE'), ('Aalborg','DK','Kristiansand','NO'),
 ('Stockholm','SE','Visby','SE'), ('Klaipėda','LT','Karlskrona','SE'), ('Nykøbing Falster','DK','Rostock','DE'),
 # Mediterrâneo
 ('Genoa','IT','Olbia','IT'), ('Genoa','IT','Sassari','IT'), ('Civitavecchia','IT','Olbia','IT'), ('Civitavecchia','IT','Cagliari','IT'),
 ('Naples','IT','Palermo','IT'), ('Naples','IT','Cagliari','IT'), ('Reggio Calabria','IT','Messina','IT'),
 ('Livorno','IT','Bastia','FR'), ('Livorno','IT','Olbia','IT'), ('Nice','FR','Bastia','FR'), ('Marseille','FR','Ajaccio','FR'),
 ('Marseille','FR','Bastia','FR'), ('Genoa','IT','Barcelona','ES'), ('Barcelona','ES','Civitavecchia','IT'),
 ('Genoa','IT','Palermo','IT'), ('Naples','IT','Ischia','IT'), ('Naples','IT','Catania','IT'),
 ('Bari','IT','Dubrovnik','HR'), ('Bari','IT','Durrës','AL'), ('Brindisi','IT','Corfu','GR'), ('Brindisi','IT','Patras','GR'),
 ('Ancona','IT','Split','HR'), ('Ancona','IT','Zadar','HR'), ('Catania','IT','Valletta','MT'),
 ('Piraeus','GR','Irákleion','GR'), ('Piraeus','GR','Chania','GR'), ('Piraeus','GR','Rhodes','GR'), ('Piraeus','GR','Chios','GR'),
 ('Piraeus','GR','Mytilene','GR'), ('Piraeus','GR','Kos','GR'), ('Rhodes','GR','Limassol','CY'),
 ('Santa Cruz de Tenerife','ES','Santa Cruz de la Palma','ES'),
 # Europa–África e Mediterrâneo sul
 ('Algeciras','ES','Tangier','MA'), ('Barcelona','ES','Tangier','MA'), ('Almería','ES','Nador','MA'),
 ('Marseille','FR','Algiers','DZ'), ('Marseille','FR','Tunis','TN'), ('Genoa','IT','Tunis','TN'), ('Palermo','IT','Tunis','TN'),
 ('Civitavecchia','IT','Tunis','TN'), ('Alicante','ES','Oran','DZ'), ('Alicante','ES','Algiers','DZ'), ('Piraeus','GR','Alexandria','EG'),
 ('Valletta','MT','Tripoli','LY'), ('Bergen','NO','Newcastle upon Tyne','GB'),
]
def find(name, cc):
    n = name.lower(); best = None
    for c in cities:
        if c[3] != cc: continue
        if c[2].lower() == n or c[1].lower() == n:
            if not best or c[6] > best[6]: best = c
    if not best:
        for c in cities:
            if c[3] == cc and (n in c[2].lower() or n in c[1].lower()):
                if not best or c[6] > best[6]: best = c
    return best
tp = os.path.join(DATA, 'travessias.json')
cur = json.load(open(tp, encoding='utf-8'))
have = {(l[0], l[2]) for l in cur['links']}
miss = []; added = 0
for a, ca, b, cb in PAIRS:
    A, B = find(a, ca), find(b, cb)
    if not A or not B: miss.append((a, ca, b, cb, bool(A), bool(B))); continue
    k = (A[1], B[1])
    if k in have or (B[1], A[1]) in have: continue
    cur['links'].append([A[1], [A[4], A[5]], B[1], [B[4], B[5]]]); have.add(k); added += 1
cur['nota'] = 'Travessias marítimas instantâneas entre portos (Península Ibérica, ilhas e Europa).'
json.dump(cur, open(tp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('acrescentadas:', added, 'total:', len(cur['links']))
for m in miss: print('FALTA:', m)
