import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._teams = []

    def creaGrafo(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._teams)

        #for u in self._grafo.nodes: #aggiungere arco ad ogni coppia di nodi, grafo completo
            #for v in self._grafo.nodes:
                #if u != v:
                    #self._grafo.add_edge(u, v)

        myedges = list(itertools.combinations(self._teams, 2))
        self._grafo.add_edges_from(myedges)

    def getTeamsOfYear(self, year):
        self._teams = DAO.getTeamsOfYear(year)
        return self._teams

    def getAllYears(self):
        return DAO.getAllYears()

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)