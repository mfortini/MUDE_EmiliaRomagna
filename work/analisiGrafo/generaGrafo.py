import igraph as G
import pandas as pd
import numpy as np
import os
from progressbar import ProgressBar
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

USA_NOME_BENEFICIARIO=False

pb=ProgressBar(maxval=len(soggDescr))
pb.start()
for (i,d) in enumerate(soggDescr.iterrows()):
    pb.update(i)
    sd=d[1]
    if USA_NOME_BENEFICIARIO:
        if len(g.vs(name=sd.BENEFICIARIO_NOME_x))==0:
            g.add_vertex(sd.BENEFICIARIO_NOME_x,denom=sd.BENEFICIARIO_NOME_x)
        g.add_edge(sd.COMUNE_DENOMINAZIONE,sd.BENEFICIARIO_NOME_x,rel="beneficiario",id_progetto=sd.ID_PROGETTO_x,codice_cup=sd.CODICE_CUP)

        if len(g.vs(name=sd.PROGETTISTA_PIVA))==0:
            g.add_vertex(sd.PROGETTISTA_PIVA,denom=sd.PROGETTISTA_NOME)
        g.add_edge(sd.BENEFICIARIO_NOME_x,sd.PROGETTISTA_PIVA,rel="progettista")
    else:
        CF=sd.BENEFICIARIO_CF.strip()
        if len(g.vs(name=CF))==0:
            g.add_vertex(CF,denom=sd.BENEFICIARIO_NOME_x)
        g.add_edge(sd.COMUNE_DENOMINAZIONE.strip(),CF,rel="beneficiario",id_progetto=sd.ID_PROGETTO_x,codice_cup=sd.CODICE_CUP)

        PIVA=sd.PROGETTISTA_PIVA.strip()
        if len(g.vs(name=PIVA))==0:
            g.add_vertex(PIVA,denom=sd.PROGETTISTA_NOME)
        g.add_edge(sd.BENEFICIARIO_CF,PIVA,rel="progettista")

    PIVA=sd.IMPRESA_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        if len(g.vs(name=PIVA))==0:
            g.add_vertex(PIVA,denom=sd.IMPRESA_NOME,comune=sd.IMPRESA_COMUNE)
        g.add_edge(sd.PROGETTISTA_PIVA.strip(),PIVA,rel="impresa")

    PIVA=sd.STRUTTURISTA_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        if len(g.vs(name=PIVA))==0:
            g.add_vertex(PIVA,denom=sd.STRUTTURISTA_NOME)
        g.add_edge(sd.PROGETTISTA_PIVA.strip(),PIVA,rel="strutturista")

    PIVA=sd.PROG_IMP_ELETT_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        if len(g.vs(name=PIVA))==0:
            g.add_vertex(PIVA,denom=sd.PROG_IMP_ELETT_NOME)
        g.add_edge(sd.PROGETTISTA_PIVA.strip(),PIVA,rel="progImpElett")

    PIVA=sd.PROG_IMP_TERM_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        if len(g.vs(name=PIVA))==0:
            g.add_vertex(PIVA,denom=sd.PROG_IMP_TERM_NOME)
        g.add_edge(sd.PROGETTISTA_PIVA.strip(),PIVA,rel="progImpTerm")

    PIVA=sd.COORD_SIC_PROG_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        if len(g.vs(name=PIVA))==0:
            g.add_vertex(PIVA,denom=sd.COORD_SIC_PROG_NOME)
        g.add_edge(sd.PROGETTISTA_PIVA.strip(),PIVA,rel="coordSicProg")

    PIVA=sd.COORD_SIC_ESEC_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        if len(g.vs(name=PIVA))==0:
            g.add_vertex(PIVA,denom=sd.COORD_SIC_ESEC_NOME)
        g.add_edge(sd.PROGETTISTA_PIVA.strip(),PIVA,rel="coordSicEsec")

    PIVA=sd.DIR_LAV_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        if len(g.vs(name=PIVA))==0:
            g.add_vertex(PIVA,denom=sd.DIR_LAV_NOME)
        g.add_edge(sd.PROGETTISTA_PIVA.strip(),PIVA,rel="dirLav")

    PIVA=sd.DIR_LAV_STRUTT_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        if len(g.vs(name=PIVA))==0:
            g.add_vertex(PIVA,denom=sd.DIR_LAV_STRUTT_NOME)
        g.add_edge(sd.PROGETTISTA_PIVA.strip(),PIVA,rel="dirLavStrutt")

    PIVA=sd.COLLAUDATORE_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        if len(g.vs(name=PIVA))==0:
            g.add_vertex(PIVA,denom=sd.COLLAUDATORE_NOME)
        g.add_edge(sd.PROGETTISTA_PIVA.strip(),PIVA,rel="collaudatore")

    PIVA=sd.CERT_ENERG_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        if len(g.vs(name=PIVA))==0:
            g.add_vertex(PIVA,denom=sd.CERT_ENERG_NOME)
        g.add_edge(sd.PROGETTISTA_PIVA.strip(),PIVA,rel="certEnerg")

    PIVA=sd.GEOLOGO_PIVA
    if not pd.isnull(PIVA):
        PIVA=PIVA.strip()
        if len(g.vs(name=PIVA))==0:
            g.add_vertex(PIVA,denom=sd.GEOLOGO_NOME)
        g.add_edge(sd.PROGETTISTA_PIVA.strip(),PIVA,rel="geologo")

pb.finish()

g.write_graphml('soggetti.graphml')
g.write_pickle('soggetti.pickle')

from IPython import embed; embed()

