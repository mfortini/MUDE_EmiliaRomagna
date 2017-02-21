import igraph as G
import pandas as pd
import numpy as np
import os
#from progressbar import ProgressBar
from matplotlib import pyplot as plt

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


BASE_DIR='../../download/2017-01-21/160901/'

avLavori=pd.read_excel(os.path.join(BASE_DIR, "avanzamento-lavori_dati_2016-09-01.xlsx"), decimal=",")
cDescr=pd.read_excel(os.path.join(BASE_DIR, "contributi_descrizione_2016-08-31.xlsx"), decimal=",")
pagamenti=pd.read_excel(os.path.join(BASE_DIR, "pagamenti_dati_2016-09-01.xls"), decimal=",")
soggetti=pd.read_excel(os.path.join(BASE_DIR, "SOGGETTI_DESCRIZIONE_2016-09-01.xlsx"), decimal=",")

avLavori.index=avLavori.RICHIESTA_MUDE
cDescr.index=cDescr.ID_PROGETTO

soggDescr=cDescr.merge(soggetti,on='CODICE_CUP')

g=G.Graph(directed=True)

from IPython import embed; embed()

g.add_vertices(list(set(soggDescr.COMUNE_DENOMINAZIONE.str.strip())))
g.vs['type']='comune'
g.vs['denom']=g.vs['name']

from IPython import embed; embed()

def addEdge(g,_from,_to,_denom,_type,n_attribs={},e_attribs={}):
    if len(g.vs(name=_to))==0:
        g.add_vertex(_to,denom=_denom,type=_type,**n_attribs)
    g.add_edge(_from,_to,rel=_type,**e_attribs)

    return g


#pb=ProgressBar(maxval=len(soggDescr))
#pb.start()
for (i,d) in enumerate(soggDescr.iterrows()):
    #pb.update(i)
    sd=d[1]
    CF=sd.BENEFICIARIO_CF.strip()
    g=addEdge(g,sd.COMUNE_DENOMINAZIONE.strip(),CF,sd.BENEFICIARIO_NOME_x,"beneficiario",e_attribs={"id_progetto":sd.ID_PROGETTO_x,"codice_cup":sd.CODICE_CUP})

    PROG_PIVA=sd.PROGETTISTA_PIVA.strip()
    g=addEdge(g,CF,PROG_PIVA,sd.PROGETTISTA_NOME,"progettista")

    PIVA=sd.IMPRESA_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        g=addEdge(g,PROG_PIVA,PIVA,sd.IMPRESA_NOME,"impresa",n_attribs={"comune":sd.IMPRESA_COMUNE})

    PIVA=sd.STRUTTURISTA_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        g=addEdge(g,PROG_PIVA,PIVA,sd.STRUTTURISTA_NOME,"strutturista")

    PIVA=sd.PROG_IMP_ELETT_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        g=addEdge(g,PROG_PIVA,PIVA,sd.PROG_IMP_ELETT_NOME,"progImpElett")

    PIVA=sd.PROG_IMP_TERM_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        g=addEdge(g,PROG_PIVA,PIVA,sd.PROG_IMP_TERM_NOME,"progImpTerm")

    PIVA=sd.COORD_SIC_PROG_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        g=addEdge(g,PROG_PIVA,PIVA,sd.COORD_SIC_PROG_NOME,"progSicProg")

    PIVA=sd.COORD_SIC_ESEC_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        g=addEdge(g,PROG_PIVA,PIVA,sd.COORD_SIC_ESEC_NOME,"progSicEsec")

    PIVA=sd.DIR_LAV_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        g=addEdge(g,PROG_PIVA,PIVA,sd.DIR_LAV_NOME,"dirLav")

    PIVA=sd.DIR_LAV_STRUTT_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        g=addEdge(g,PROG_PIVA,PIVA,sd.DIR_LAV_STRUTT_NOME,"dirLavStrutt")

    PIVA=sd.COLLAUDATORE_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        g=addEdge(g,PROG_PIVA,PIVA,sd.COLLAUDATORE_NOME,"collaudatore")

    PIVA=sd.CERT_ENERG_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        g=addEdge(g,PROG_PIVA,PIVA,sd.CERT_ENERG_NOME,"certEnerg")

    PIVA=sd.GEOLOGO_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        g=addEdge(g,PROG_PIVA,PIVA,sd.GEOLOGO_NOME,"geologo")

#pb.finish()

g.write_graphml('soggetti.graphml')
g.write_pickle('soggetti.pickle')

from IPython import embed; embed()

