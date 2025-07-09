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

        return lp[1:]

if __name__ == '__main__':
    provaModel = Model()
    provaModel.buildGraph(1, 10)

    nodi = provaModel.getGraphDetails()[0]
    print(nodi)

    archi = provaModel.getGraphDetails()[1]
    print(archi)