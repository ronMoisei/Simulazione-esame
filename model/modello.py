import copy
from database.DAO import DAO
import networkx as nx
class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}

    def getStores(self):
        return DAO.getAllStores()

    def get_nodes(self, store):
        return DAO.get_nodes(store)

    def get_edges(self, idMap, product):
        return DAO.get_edges(idMap, product)

    def getProductsByStores(self, store_id):
        return DAO.getProductsByStores(store_id)

    def buildGraph(self, store, product = None):
        self._graph.clear()
        self._nodes = self.get_nodes(store)
        for n in self._nodes:
            self._idMap[n.customer_id] = n
        self._graph.add_nodes_from(self._nodes)

        allEdges = self.get_edges(self._idMap, product)
        for e in allEdges:
            self._graph.add_edge(e[0], e[1], weight=e[2])

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

if __name__ == '__main__':
    m = Model()
    m.buildGraph(1)
    print(m._idMap)