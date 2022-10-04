class Queue:
    """Queue implementation as a list"""

    def __init__(self):
        """Create new queue"""
        self._items = []

    def is_empty(self):
        """Check if the queue is empty"""
        return not bool(self._items)

    def enqueue(self, item):
        """Add an item to the queue"""
        self._items.insert(0, item)

    def dequeue(self):
        """Remove an item from the queue"""
        return self._items.pop()

    def size(self):
        """Get the number of items in the queue"""
        return len(self._items)


class Vertex:
    def __init__(self, key, distance=0, predecessor=None, color='white', discovery=0, finish=0):
        self.id = key
        self.connectedTo = {}
        self.distance = distance
        self.predecessor = predecessor
        self.color = color
        self.discovery = discovery
        self.finish = finish

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self, nbr):
        return self.connectedTo[nbr]

    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def getDistance(self):
        return self.distance

    def setDistance(self, num):
        self.distance = num

    def getPred(self):
        return self.predecessor

    def setPred(self, p):
        self.predecessor = p

    def getColor(self):
        return self.color

    def setColor(self, c):
        self.color = c

    def getDiscovery(self):
        return self.discovery

    def setDiscovery(self, t):
        self.discovery = t

    def getFinish(self):
        return self.finish

    def setFinish(self, f):
        self.finish = f


class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self, key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList

    def addEdge(self, f, t, weight=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], weight)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())


class DFSGraph(Graph):
    def __init__(self):
        super().__init__()
        self.time = 0

    def dfs(self):
        for aVertex in self:
            aVertex.setColor('white')
            aVertex.setPred(-1)
        for aVertex in self:
            if aVertex.getColor() == 'white':
                self.dfsvisit(aVertex)

    def dfsvisit(self, startVertex):
        startVertex.setColor('gray')
        self.time += 1
        startVertex.setDiscovery(self.time)
        for nextVertex in startVertex.getConnections():
            if nextVertex.getColor() == 'white':
                nextVertex.setPred(startVertex)
                self.dfsvisit(nextVertex)
        startVertex.setColor('black')
        self.time += 1
        startVertex.setFinish(self.time)


def top_sort(g):
    g.dfs()
    l = []
    for i in g.getVertices():
        a = g.getVertex(i)
        l.append((i, a.getFinish()))
    l.sort(key=lambda tup: tup[1])
    l.reverse()
    l2 = []
    for i in l:
        l2.append(i[0])
    return l2


def main():
    print('\nThis program reads in a list of courses and prerequisites, and determines\na valid ordering subject to '
          'prerequisite constraints via topological sort.\n')
    with open('prereq.txt', 'r') as prereqs:
        stringy = 'Reading input file "prereq.txt"...\n'
        file_stuff = {}
        for line in prereqs:
            stringy += 'Processing input file line->' + line
            file_stuff[line.split(':')[0]] = list(line.split(':')[1].strip('\n').split())
        print(stringy)

    class_graph = DFSGraph()
    for c in file_stuff.keys():
        if len(file_stuff[c]) > 0:
            for p in file_stuff[c]:
                class_graph.addEdge(p, c)

    print('Performing topological sort...')
    print('Ordered list:\n%s' % top_sort(class_graph))


main()
