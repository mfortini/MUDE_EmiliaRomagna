import igraph as G
import pandas as pd
import numpy as np
import json
import os
from matplotlib import pyplot as plt
import codicefiscale as cf
import itertools
import Levenshtein as pL
from datetime import datetime
import re
import sys

# avanzamento-lavori_dati_2016-09-01.csv
# avanzamento-lavori_dati_2016-09-01.ods
# avanzamento-lavori_dati_2016-09-01.xlsx
# avanzamento_lavori_descrizione.txt
# contributi_descrizione_2016-08-31.csv
# contributi_descrizione_2016-08-31.ods
# contributi_descrizione_2016-08-31.xlsx
# contributi_descrizione.txt
# licenza_dati_ricostruzione_CC-BY.pdf
# pagamenti_dati_2016-09-01.csv
# pagamenti_dati_2016-09-01.ods
# pagamenti_dati_2016-09-01.xls
# pagamenti_descrizione.txt
# SOGGETTI_DESCRIZIONE_2016-09-01.csv
# SOGGETTI_DESCRIZIONE_2016-09-01.ods
# SOGGETTI_DESCRIZIONE_2016-09-01.xlsx
# soggetti_descrizione.txt


g=G.read('soggetti.pickle')

def comuneCF(cf):
    return cf[-5:-1]

def noncomuneCF(cf):
    return cf[:11]

for v in g.vs:
    if not pd.isnull(v['denom']):
        v['ident']=v['name']+" "+v['denom']
    else:
        v['ident']=v['name']
    if not v['name'].isnumeric():
        if v['type'] == 'comune':
            v['denomecomune']=v['denom']
        else:
            v['denomecomune']=str(v['denom'])+' '+comuneCF(v['name'])

df=pd.DataFrame({'index':g.vs.indices,'denomecomune':g.vs['denomecomune']})

nomiDup=df[(~pd.isnull(df['denomecomune']))&df.duplicated('denomecomune')]

from IPython import embed; embed()

def d(words,coord):
    i, j = coord
    return (100 - fuzz.ratio(words[i], words[j]))/100.

def hcluster(words):
    indices=np.triu_indices(len(words), 1)
    distances=np.apply_along_axis(lambda x: d(words,x), 0, indices)
    h=scipy.cluster.hierarchy.linkage(distances)
    from IPython import embed; embed()

def cfCorrectName(codice,fullname):
    match=re.match(r"(\S*)\s*(.*)",fullname)
    (surname,name)=match.groups()
    bday=datetime.strptime(cf.get_birthday(codice),'%d-%m-%y')
    sex=cf.get_sex(codice)
    comune=comuneCF(codice)
    return cf.build(surname, name, bday, sex, comune)


# Elementi che hanno lo stesso nominativo
toMerge=[]
for (i,n) in nomiDup.iterrows():
    vs=list(g.vs(denomecomune=n.denomecomune))
    print (n.denomecomune)
    mergeSet=set([])
    for cc in itertools.combinations(vs,2):
        cf0=(cc[0]['name'],cc[0]['denom'])
        cf1=(cc[1]['name'],cc[1]['denom'])
        # Che non sono numerici
        if not cf0[0].isnumeric() and not cf1[0].isnumeric():
            # Correggiamo la parte del nome
            print (noncomuneCF(cf0[0]),noncomuneCF(cf1[0]),pL.distance(noncomuneCF(cf0[0]),noncomuneCF(cf1[0])))
            if pL.distance(noncomuneCF(cf0[0]),noncomuneCF(cf1[0]))<=4:
                mergeSet.update((cc[0],))
                mergeSet.update((cc[1],))
    if len(mergeSet) > 0:
        toMerge.append(mergeSet)

gg=g.copy()
mergeMap={}
for m in toMerge:
    # scegliamo il compleanno con piu' frequenza
    print ("")
    print ("")
    print (m)
    sex=map(cf.get_sex,[mm['name'] for mm in m if cf.isvalid(mm['name'])])
    bdays=list(map(cf.get_birthday,[mm['name'] for mm in m if cf.isvalid(mm['name'])]))
    bdaysDT=[]
    for bd in bdays:
        try:
            bdDT=datetime.strptime(bd,'%d-%m-%y')
            bdaysDT.append(bdDT)
        except:
            pass

    comune=comuneCF(list(m)[0]['name'])
    likelyBdayDT=pd.value_counts(bdaysDT).index[0]
    likelySex=pd.value_counts(sex).index[0]
    match=re.match(r"\s*((?:(?:DI|DEL|DELLA|DE) )?\s*\S*)\s*(.*)",list(m)[0]['denom'])
    (surname,name)=match.groups()
    print (bdays, bdaysDT, likelySex, surname,",", name)
    print (likelyBdayDT)
    newCF=cf.build(surname, name, likelyBdayDT, likelySex, comune)
    for mm in m:
        if mm['name']!=newCF:
            mergeMap[mm.index]=newCF
        mm['name']=newCF

    if len(bdays) == 0:
        print ("NO BIRTHDAYS")
        from IPython import embed; embed()

from IPython import embed; embed()

g.vs['denomtipo']=list(map(",".join,zip(g.vs['name'],g.vs['type'])))

gCFTipo=g.copy()

newCFIdx={}
for idx,cf in enumerate(set(gCFTipo.vs['denomtipo'])):
    newCFIdx[cf]=idx

newVMap=[]
for v in gCFTipo.vs:
    newVMap.append(newCFIdx[v['denomtipo']])

gCFTipo.contract_vertices(newVMap,combine_attrs='first')

gCFTipo.es['count']=1.

gCF=g.copy()

newCFIdx={}
for idx,cf in enumerate(set(gCF.vs['name'])):
    newCFIdx[cf]=idx

newVMap=[]
for v in gCF.vs:
    newVMap.append(newCFIdx[v['name']])

gCF.contract_vertices(newVMap,combine_attrs='first')
gCF.es['count']=1.
gCF.vs['ident']=list(map(lambda x:str.encode(x,'ascii','ignore'),gCF.vs['ident']))
gCF.vs['denom']=list(map(lambda x:str.encode(x,'ascii','ignore'),map(str,gCF.vs['denom'])))
gCF.vs['denom']=[x.decode() for x in gCF.vs['denom']]
from IPython import embed; embed()
gCF.write_graphml('gCF.graphml')
gCF.write_pickle('gCF.pickle')

sys.exit()



# f=open('soggettiPulire.csv','w+')
# f.write(','.join(("oldIdent","newIdent"))+'\n')
# for v in g.vs:
#     f.write(','.join(('"'+v['ident'].encode('utf-8')+'"','"'+v['ident'].encode('utf-8')+'"'))+'\n')
# f.close()

soggettiCluster=pd.read_csv('soggettiCluster.csv',sep='|')

oldMap=[]
newMap=[]
for (idx,r) in soggettiCluster.iterrows():
    oldMap.append(g.vs(ident=r.oldIdent.decode('utf-8'))[0].index)
    newMap.append(g.vs(ident=r.newIdent.decode('utf-8'))[0].index)

g1=G.Graph(directed=True)

newMapSet=list(set(newMap))

for v in g.vs[newMapSet]:
    g1.add_vertex(**v.attributes())

for e in g.es:
    s,t=e.tuple
    g1.add_edge(newMapSet.index(newMap[s]),newMapSet.index(newMap[t]),**e.attributes())

g1.write_pickle('soggettiPuliti.pickle')

