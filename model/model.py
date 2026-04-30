from datetime import datetime

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()          # abbiamo istanziato una variabile di tipo grafo
        self._idMapFermate = {}
        for f in self._fermate:             # dato id fermata ritorno l'oggetto fermata corrispondente
            self._idMapFermate[f.id_fermata] = f

    def getBFSNodesFromEdges(self, source):
        archi = nx.bfs_edges(self._grafo, source)
        nodiBFS = []
        for u, v in archi:
            nodiBFS.append(v)
        return nodiBFS

    def getDFSNodesFromEdges(self, source):
        archi = nx.bfs_edges(self._grafo, source)
        nodiDFS = []
        for u, v in archi:
            nodiDFS.append(v)
        return nodiDFS

    # usando albero di visita
    def getBFSNodesFromTree(self, source):
        tree = nx.bfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi

    def getDFSNodesFromTree(self, source):
        tree = nx.dfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi

    def buildGraph(self):
        # bisogna sempre assicurasi prima che il grafo sia vuoto prima di aggiungere le cose
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)       # _fermate è già una lista

        # tic = datetime.now()
        # self.addedges()
        # toc = datetime.now()
        # print("Tempo impiegato da modo 1: ", toc - tic)
        #
        # tic = datetime.now()
        # self.addedges2()
        # toc = datetime.now()
        # print("Tempo impiegato da modo 2: ", toc - tic)

        tic = datetime.now()
        self.addedges3()
        toc = datetime.now()
        print("Tempo impiegato da modo 3: ", toc-tic)

    def get_numnodi(self):
        return len(self._grafo.nodes())

    def get_numarchi(self):
        return len(self._grafo.edges())

    @property
    def fermate(self):
        return self._fermate

    def addedges(self):                 # fare 2 for annidati è costoso, ci mette tantissimo tempo a darmi il risultato
        self._grafo.clear_edges()       # ha senso farlo quando ho grafi piccoli
        for u in self._fermate:
            for v in self._fermate:
                if DAO.hasconn(u, v):
                    self._grafo.add_edge(u, v)

    def addedges2(self):                # più veloce
        self._grafo.clear_edges()
        for u in self._fermate:
            for conn in DAO.getvicini(u):
                v = self._idMapFermate[conn.id_stazA]
                self._grafo.add_edge(u, v)

    def addedges3(self):                # ancora più veloce
        self._grafo.clear_edges()
        alledges = DAO.getAllEdges()
        for conn in alledges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]
            self._grafo.add_edge(u, v)