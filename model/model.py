import copy
from database.DAO import DAO
import networkx as nx
class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}

    def getBestPath(self, startStr):
        # Inizializza il percorso migliore e il punteggio massimo trovati
        self._bestPath = []
        self._bestScore = 0

        # Converte l'identificatore di partenza da stringa a intero
        # e lo mappa all'oggetto nodo corrispondente
        start = self._idMap[int(startStr)]

        # Lista temporanea che terrà il percorso corrente, parte da 'start'
        parziale = [start]

        # Prende tutti i vicini diretti del nodo di partenza
        vicini = self._graph.neighbors(start)
        for v in vicini:
            # Aggiunge ciascun vicino al percorso parziale
            parziale.append(v)
            # Avvia la ricorsione per esplorare i cammini che partono da questa estensione
            self._ricorsione(parziale)
            # Togli il nodo aggiunto, per provare il prossimo vicino
            parziale.pop()

        # Alla fine restituisce il miglior percorso e il relativo punteggio
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale):
        # Calcola il punteggio del percorso corrente
        current_score = self.getScore(parziale)
        # Se è migliore di quello registrato, aggiorna bestScore e bestPath
        if current_score > self._bestScore:
            self._bestScore = current_score
            # deepcopy per non avere riferimenti condivisi con 'parziale'
            self._bestPath = copy.deepcopy(parziale)

        # Esplora ulteriori estensioni del percorso
        # Prende i vicini dell’ultimo nodo del percorso
        ultimo = parziale[-1]
        precedente = parziale[-2]  # nodo prima dell'ultimo

        for v in self._graph.neighbors(ultimo):
            # 1) Evita di tornare su nodi già visitati (nessuna ripetizione)
            # 2) Controlla che il peso del nuovo arco (ultimo→v) sia minore
            #    di quello dell’arco precedente (precedente→ultimo)
            peso_precedente = self._graph[precedente][ultimo]["weight"]
            peso_nuovo = self._graph[ultimo][v]["weight"]
            if v not in parziale and peso_nuovo < peso_precedente:
                # Aggiunge il nuovo nodo e continua la ricorsione
                parziale.append(v)
                self._ricorsione(parziale)
                # Rimuove il nodo per backtracking
                parziale.pop()

    def getScore(self, listOfNodes):
        """
        Calcola il “punteggio” di un percorso sommando i pesi
        di tutti gli archi che collegano i nodi consecutivi.
        """
        tot = 0
        # Scorri ogni coppia di nodi adiacenti e somma il peso dell’arco
        for i in range(len(listOfNodes) - 1):
            src = listOfNodes[i]
            dst = listOfNodes[i + 1]
            tot += self._graph[src][dst]["weight"]
        return tot



    def getStores(self):
        return DAO.getAllStores()


    def buildGraph(self, store, k):
        self._graph.clear()
        self._orders = DAO.getAllOrdersbyStore(store)
        for o in self._orders:
            self._idMap[o.order_id] = o

        self._graph.add_nodes_from(self._orders)

        allEdges = DAO.getEdges(store, k, self._idMap)
        for e in allEdges:
                self._graph.add_edge(e[0], e[1], weight=e[2])

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getAllNodes(self):
        nodes = list(self._graph.nodes)
        return nodes

    def getBFSNodesFromTree(self, source):
        tree = nx.bfs_tree(self._graph, self._idMap[int(source)])
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi[1:]

    def getDFSNodesFromTree(self, source):
        tree = nx.dfs_tree(self._graph, source)
        nodi = list(tree.nodes())
        return nodi[1:]

    def getCammino(self, sourceStr):
        source = self._idMap[int(sourceStr)]
        lp = []

        #for source in self._graph.nodes:
        tree = nx.dfs_tree(self._graph, source)
        nodi = list(tree.nodes())

        for node in nodi:
            tmp = [node]

            while tmp[0] != source:
                pred = nx.predecessor(tree, source, tmp[0])
                tmp.insert(0, pred[0])

            if len(tmp) > len(lp):
                lp = copy.deepcopy(tmp)

        return lp