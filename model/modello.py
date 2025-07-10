import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}

    def getStores(self):
        return DAO.getAllStores()

    def getYearsByStores(self, store):
        return DAO.getYearsByStores(store)
    def buildGraph(self, store, qty, year=None):
        self._graph.clear()
        self._products = DAO.get_Products(store, 10)
        for p in self._products:
            self._idMap[p.product_id] = p

        self._graph.add_nodes_from(self._products)

        allEdges = DAO.get_EdgesWeight(store, self._idMap, year)
        for e in allEdges:
                self._graph.add_edge(e[0], e[1], weight=e[2])

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getAllNodes(self):
        nodes = list(self._graph.nodes)
        return nodes

    def getBFSNodesFromTree(self, source):
        """Performs a breadth-first search (BFS) tree from a source node and returns
            the list of reached nodes (excluding the source).

            :param source: external identifier for the source node
            :return: list of external node identifiers in BFS order, excluding the source"""

        tree = nx.bfs_tree(self._graph, self._idMap[int(source)])
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi[1:]

    def getDFSNodesFromTree(self, source):
        tree = nx.dfs_tree(self._graph, source)
        nodi = list(tree.nodes())
        return nodi[1:]

    def getCammino(self, sourceStr):
        # 1. Converte la stringa di input nel nodo interno corrispondente
        #    sourceStr è probabilmente un ID di nodo selezionato dall’utente (stringa)
        source = self._idMap[int(sourceStr)]

        # 2. Inizializza la variabile per tenere traccia del cammino più lungo trovato
        lp = []

        # 3. Costruisce l’albero di ricerca in profondità (DFS tree) a partire da `source`
        #    tree è un subgrafo orientato che contiene tutti i nodi raggiungibili da `source`
        tree = nx.dfs_tree(self._graph, source)

        # 4. Estrae in lista tutti i nodi visitati nell’ordine DFS
        nodi = list(tree.nodes())

        # 5. Per ciascun nodo raggiungibile, ricostruisce il percorso dal source fino a quel nodo
        for node in nodi:
            # tmp inizia con l’unico nodo di destinazione
            tmp = [node]

            # 5.a. Risale i predecessori finché non raggiunge il source
            #      nx.predecessor(tree, source, x) restituisce la lista dei predecessori di x
            while tmp[0] != source:
                pred = nx.predecessor(tree, source, tmp[0])
                tmp.insert(0, pred[0])  # inserisce il predecessore all’inizio di tmp

            # 5.b. Se il percorso tmp è più lungo di quello memorizzato in lp,
            #      aggiorna lp con una copia profonda di tmp
            if len(tmp) > len(lp):
                lp = copy.deepcopy(tmp)

        # 6. Restituisce il cammino più lungo trovato, escludendo il nodo di partenza
        #    (lp[1:] taglia il primo elemento, cioè `source`)
        return lp[1:]

    def getBestPath(self, startStr):
        """
        Inizia la ricerca della catena ottimale da startStr (stringa di product_id).
        """
        # reset
        self._bestPath = []
        self._bestScore = 0.0

        # mappa lo start node
        start_id = int(startStr[0])
        start = self._idMap[start_id]

        # se vuoi includere anche il singolo nodo come path valido,
        # potresti valutare getScore([start]) qui.

        # prova ad espandere la catena su ciascun vicino
        for v in self._graph.neighbors(start):
            path = [start, v]
            self._ricorsione(path)

        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale):
        """
        Backtracking: estende `parziale`, rispettando il vincolo di categoria,
        aggiornando bestPath/bestScore quando trova un punteggio migliore.
        """
        # 1) valuta il percorso corrente
        score = self.getScore(parziale)
        if score > self._bestScore:
            self._bestScore = score
            self._bestPath = copy.deepcopy(parziale)

        # 2) calcola le categorie già usate
        used_cats = {n.category_id for n in parziale}

        # 3) esplora i vicini dell'ultimo nodo
        last = parziale[-1]
        for n in parziale:
            print(n, n.list_price)
        print("-"*10)
        for nbr in self._graph.neighbors(last):
            # non visitare due volte e rispetta il vincolo di categoria
            if nbr not in parziale and nbr.category_id not in used_cats:
                parziale.append(nbr)
                self._ricorsione(parziale)
                parziale.pop()

    def getScore(self, listOfNodes):
        """
        Restituisce la somma dei list_price dei prodotti nel percorso.
        """
        return sum(node.list_price for node in listOfNodes)

    def getNode(self):
        pass

if __name__ == '__main__':

    provaModel = Model()
    provaModel.buildGraph(1, 10)
    mappa = provaModel._idMap
    print(mappa)
    bestPercorso = provaModel.getBestPath(str(mappa[2].product_id))
    for b in bestPercorso:
        print(f"{b}\n")