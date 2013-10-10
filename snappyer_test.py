__author__ = 'trusheim'

from snappyer import *
import snap # not necessary, just for test

# ---
# Create a graph from an edge file
graph = SnapGraph.fromEdgeFile("test_graph.txt",SnapGraph.TYPE_DIRECTED, 0, 1) # also TYPE_UNDIRECTED, TYPE_NETWORK

# ---
# Use raw snap.py functions to create, then import to Snappyer
rawGraph = snap.GenSmallWorld(100, 10, 0.5)
graph = SnapGraph(rawGraph)

# or make a blank graph
blankGraph = SnapGraph.Empty(SnapGraph.TYPE_UNDIRECTED)
blankGraph.addNode(1)
blankGraph.addNode(2)
blankGraph.addEdge(1,2)

# ---
# the niceness of all functions is >= snap.py niceness
# in general, we try to use properties wherever possible, instead of functions.

nodeTen = graph.node(10)
nodeTen = graph[10] # alias for .node()

for node in graph.nodes: # graph.nodes returns an iterator of SnapNodes
    print node.id # or any other SnapNode property

for edge in graph.edges:
    print edge.destination # SnapNode
    print edge.source # SnapNode

# ---
# all functions take ints (assumed to be node IDs) or SnapNodes
source = 1
destination = 2
graph.addEdge(source,destination)

source = graph[1] # SnapNode
destination = graph[2]
graph.addEdge(source,destination) # works the same!

# ---
# fun with graph properties

boolVar = graph.isConnected
boolVar = graph.isWeaklyConnected

x = graph.numEdges
x = graph.numNodes
x = graph.numSelfEdges
x = graph.numUniqueBidirectionalEdges
x = graph.numUniqueDirectedEdges
x = graph.numUniqueUndirectedEdges

r = graph.degreeDistribution # dict of degree [int] => count [int]
r = graph.getDegreeProportions() # dict of degree [int] => proportion of that degree to total [float]
r = graph.getNodesByDegree() # dict of degree [int] => list of SnapNodes with that degree

# ---
# get components without dicking around with pointers

sccs = graph.sccs() # returns a list of sets of SnapNodes
maxSccGraph = graph.maxSccGraph() # returns a SnapGraph of the max SCC graph
wccs = graph.wccs() # list of sets of SnapNodes
maxWccGraph = graph.maxWccGraph() # SnapGraph of max WCC graph

# for faster performance, turn off node ID -> SnapNode resolution
sccs = graph.sccs(False) # this now returns a list of sets of ints (which are node IDs)

# ---
# adjust graphs
graph.addNode(101)
graph.addEdge(1,101)
graph.deleteSelfEdges()
graph.deleteZeroDegreeNodes()

# ---
# fun with nodes

nodeTen = graph.node(10) # returns a SnapNode
nodeTen = graph[10] # same as above
randomNode = graph.randomNode()

outNodes = nodeTen.outNodes # list of SnapNodes
for node in outNodes:
    print "Node 10 goes has an out edge to %d" % node.id

inNodes = nodeTen.inNodes # list of SnapNodes
for node in inNodes:
    print "Node 10 has incoming from %d" % node.id

x = nodeTen.id # 10
x = nodeTen.inDegree
x = nodeTen.outDegree

nodeTen.hasEdgeTo(randomNode) # bool
nodeTen.hasEdgeFrom(randomNode) # bool
nodeTen.isNeighborTo(randomNode) # bool

nodeTen.nodesInWcc() # returns a set of SnapNodes that are within the same connected component as nodeTen