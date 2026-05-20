import copy
import itertools
import random

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._teams = []
        self._idMapTeams = None
        self._bestPath = []
        self._bestObjVal = 0

    def getPath(self, v0):
        self._bestPath = []
        self._bestObjVal = 0

        parziale = [v0]

        for v in self._grafo.neighbors(v0):
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()

    def getPathV2(self, v0):
        self._bestPath = []
        self._bestObjVal = 0

        parziale = [v0]

        listaVicini = self.getVicini(parziale[-1])  # ordinata
        parziale.append(listaVicini[0][0])#arco con peso maggiore
        self._ricorsioneV2(parziale)
        return self._bestPath, self._objVal


    def _ricorsione(self, parziale):
        #1) condizione di ottimalità, verificare se parziale migliore del best
        if self._score(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._objVal = self._score(parziale)

        #2) condizione di terminazione, verifico se posso continuare
        #in quetsto caso non c'è

        #3) faccio la mia ricorsione
        for v in self._grafo.neighbors(parziale[-1]):
            pesoE = self._grafo[parziale[-1]][v]["weight"] #arco da utimo nodo aggiunto a v

            if self._grafo[parziale[-2]][parziale[-1]]["weight"] > pesoE and v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    def _ricorsioneV2(self, parziale):
        # 1) condizione di ottimalità, verificare se parziale migliore del best
        if self._score(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._objVal = self._score(parziale)

        # 2) condizione di terminazione, verifico se posso continuare
        # in quetsto caso non c'è

        # 3) faccio la mia ricorsione
        #listavicini = []
        #for v in self._grafo.neighbors(parziale[-1]):
            #edgeV =self._grafo[parziale[-1]][v]["weight"]
            #listavicini.append((v, edgeV))

        #listavicini.sort(key=lambda x: x[1], reverse=True)

        listaVicini = self.getVicini(parziale[-1]) #ordinata

        for v in listaVicini:
            if v[0] not in parziale and self._grafo[parziale[-2]][parziale[-1]]["weight"] > v[1]:
                parziale.append(v[0])
                self._ricorsioneV2(parziale)
                parziale.pop()
                return

    def _score(self, parziale):
        score = 0
        for i in range(0, len(parziale)-1):
            score += self._grafo[parziale[i]][parziale[i+1]]["weight"]
        return score

    def creaGrafo(self, year):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._teams)

        #for u in self._grafo.nodes: #aggiungere arco ad ogni coppia di nodi, grafo completo
            #for v in self._grafo.nodes:
                #if u != v:
                    #self._grafo.add_edge(u, v)

        myedges = list(itertools.combinations(self._teams, 2))
        self._grafo.add_edges_from(myedges)

        mapSalary = DAO.getSalariesTeam(year, self._idMapTeams)

        for e in self._grafo.edges:
            sal1 = mapSalary[e[0]] #slario primo team dell'arco
            sal2 = mapSalary[e[1]]
            peso = sal1 + sal2
            self._grafo[e[0]][e[1]]["weight"]=peso

            #self._grafo[e[1]][e[0]]["weight"]= mapSalary[e[0]] +mapSalary[e[1]]

    def getVicini(self, source):
        vicini = self._grafo.neighbors(source)
        viciniTuples = []
        for v in vicini:
            viciniTuples.append((v, self._grafo[source][v]["weight"]))

        viciniTuples.sort(key=lambda x: x[1], reverse=True)
        return viciniTuples

    def getTeamsOfYear(self, year):
        self._teams = DAO.getTeamsOfYear(year)
        self._idMapTeams = {t.ID: t for t in self._teams}
        return self._teams

    def getAllYears(self):
        return DAO.getAllYears()

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getRandomNode(self):
        index = random.randint(0, len(self._teams))
        return self._teams[index]