"""Simula los archivos que genera la aplicación (por_minuto_*.csv y muestra_*.csv)
a partir del conteo manual real, según la indicación del docente de usar datos
simulados en la sección de resultados.

Uso: python simular.py   (en la misma carpeta que conteo_manual.csv)

Supuestos, tomados de lo observado al probar la aplicación con los videos:
- Autos detectados: 90% mañana, 91% tarde, 80% noche.
- Motos detectadas: 32% mañana, 30% tarde, 15% noche.
- Camiones: 68% se registran como auto.
- Combis: 60% se registran como auto; cústers: 30% como auto.
- Falsos positivos (sombras): 0.25 por minuto de día y 0.45 de noche.
"""
# Simulación de los resultados de la aplicación a partir del conteo manual real.
import numpy as np, pandas as pd, random
rng=np.random.default_rng(29); random.seed(29)
man=pd.read_csv('conteo_manual.csv')
P_AUTO={'mañana':0.90,'tarde':0.91,'noche':0.80}
P_MOTO={'mañana':0.32,'tarde':0.30,'noche':0.15}
def label(dist):
    k=list(dist); return rng.choice(k,p=[dist[x] for x in k])
eventos=[]
for _,r in man.iterrows():
    h,m=r.horario,r.minuto
    ev=[]
    for _ in range(r.auto):
        if rng.random()<P_AUTO[h]: ev.append(('auto',label({'auto':.95,'camion':.05})))
    for _ in range(r.moto):
        if rng.random()<P_MOTO[h]: ev.append(('moto',label({'moto':.85,'auto':.15})))
    for _ in range(r.bus):
        sub=label({'bus':.30,'combi':.45,'custer':.25})
        if rng.random()<0.95:
            ev.append((sub,label({'bus':{'bus':.85,'auto':.05,'camion':.10},'combi':{'auto':.60,'bus':.35,'camion':.05},'custer':{'bus':.50,'auto':.30,'camion':.20}}[sub])))
    for _ in range(r.camion):
        if rng.random()<0.92: ev.append(('camion',label({'auto':.68,'camion':.32})))
    for _ in range(rng.poisson(0.25 if h!='noche' else 0.45)): ev.append(('ninguno','auto'))
    for real,pag in ev:
        eventos.append(dict(horario=h,minuto=m,clase_real=real,clase_pagina=pag,tiempo_s=round((m-1)*60+rng.uniform(0,60),1)))
ev=pd.DataFrame(eventos)
C=['auto','moto','bus','camion']
for h,arch in [('mañana','manana'),('tarde','tarde'),('noche','noche')]:
    g=ev[ev.horario==h]
    t=pd.crosstab(g.minuto,g.clase_pagina).reindex(index=range(1,11),columns=C,fill_value=0)
    t.insert(0,'minuto',t.index); t.insert(0,'horario',h); t['total']=t[C].sum(axis=1)
    t.to_csv(f'por_minuto_{arch}.csv',index=False)
    n=17 if h!='noche' else 16
    cuota={'auto':6,'moto':3,'bus':1,'combi':3,'custer':2,'camion':2,'ninguno':1}
    partes=[g[g.clase_real==k].sample(min(q,(g.clase_real==k).sum()),random_state=29) for k,q in cuota.items()]
    s=pd.concat(partes)
    if len(s)<n: s=pd.concat([s,g[(g.clase_real=='auto')&~g.index.isin(s.index)].sample(n-len(s),random_state=29)])
    s=s.head(n) if len(s)>n else s
    s=s.sort_values('tiempo_s').reset_index(drop=True); s.insert(0,'id',range(1,len(s)+1))
    s[['id','horario','clase_real','clase_pagina','tiempo_s']].to_csv(f'muestra_{arch}.csv',index=False)
print(ev.groupby('horario',sort=False).size())
