class Node(object):
    def __init__(self, name):
        self.name = name
    def getName(self):
        return self.name
    def __str__(self):
        return self.name

class Edge(object):
    def __init__(self, src, dst, weight):
        self.src = src
        self.dst = dst
        self.weight = weight
    
    def getSource(self):
        return self.src

    def getDestination(self):
        return self.getDestination

    def getWeight(self):
        return self.weight
    def __str__(self):
        return str(self.src) + '->' + str(self.dst)

class Digraph(object):
    def __init__(self):
        self.nodes = set([])
        self.edges = {}
    def addNode(self, node):
        if node.getName() in self.nodes:
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not (src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = res + str(k) + '->' + str(d) + '\n'
        return res[:-1]

class Graph(Digraph):
    def addEdge(self, edge):
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        Digraph.addEdge(self, rev) 


def shortestPath(graph, start, end, toPrint = Flase, visited = []):
    if toPrint:
        print start, end
    if not (graph.hasNode(start) and graph.hasNode(end)):
        raise ValueError('Start or end not in grahp')
    path = [str(start)]