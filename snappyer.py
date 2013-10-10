__author__ = 'trusheim'
# Author: Stephen Trusheim (tru@cs.stanford.edu, github.com/trusheim)
# License: CC BY-SA 3.0
# requires snap.py 0.8.1 or above.
# version: 2013-10-10, way too late in the AM

import snap
import collections

class SnapGraph(object):
    TYPE_UNKNOWN = -1 # ???
    TYPE_NONE = 0
    TYPE_DIRECTED = 1
    TYPE_UNDIRECTED = 2
    TYPE_NETWORK = 3

    rawGraph = None
    rawGraphType = TYPE_NONE

    # creators

    def __init__(self, rawGraph=None):
        self.__setGraph(rawGraph)

    def __setGraph(self, graph_):
        self.rawGraph = graph_

        gType = type(self.rawGraph)
        if gType == snap.PNGraph:
            self.rawGraphType = self.TYPE_DIRECTED
        elif gType == snap.PUNGraph:
            self.rawGraphType = self.TYPE_UNDIRECTED
        elif gType == snap.PNEANet:
            self.rawGraphType = self.TYPE_NETWORK
        else:
            self.rawGraphType = self.TYPE_UNKNOWN

    @staticmethod
    def fromEdgeFile(filename, graphType, sourceColId, destColId, separator="\t"):
        snapType = SnapUtil.snappyerToSnapType(graphType)
        newGraph = snap.LoadEdgeList(snapType, filename, sourceColId, destColId, separator)
        return SnapGraph(newGraph)

    @staticmethod
    def Empty(graphType):
        if graphType == SnapGraph.TYPE_DIRECTED:
            return SnapGraph(snap.TNGraph.New())
        elif graphType == SnapGraph.TYPE_UNDIRECTED:
            return SnapGraph(snap.TNGraph.New())
        else:
            raise IndexError, "Illegal type of graph to create"

    @staticmethod
    def Random(graphType):
        raise NotImplementedError

    @staticmethod
    def SmallWorld(graphType):
        raise NotImplementedError

    # node getters
    def node(self,nodeId):
        return SnapNode(self.rawGraph.GetNI(nodeId), self)

    def randomNode(self):
        return SnapNode(self.rawGraph.GetNI(self.rawGraph.GetRndNId()), self)

    def __getitem__(self,item):
        return self.node(item)

    # iterators over nodes and edges
    @property
    def nodes(self):
        for node in self.rawGraph.Nodes():
            yield SnapNode(node, self)

    # idk why this doesnt work
    # @property
    # def nodeSet(self):
    #     nodeset = set()
    #     for node in self.nodes:
    #         nodeset.add(node)
    #     return nodeset

    @property
    def edges(self):
        for node in self.rawGraph.Edges():
            yield SnapEdge(node, self)

    # idk why this doesnt work either
    # @property
    # def edgeSet(self):
    #     edgeset = set()
    #     for edge in self.edges:
    #         edgeset.add(edge)
    #     return edgeset

    # graph properties
    @property
    def numNodes(self):
        return self.rawGraph.GetNodes()

    @property
    def numEdges(self):
        return self.rawGraph.GetEdges()

    @property
    def numUniqueBidirectionalEdges(self):
        return snap.CntUniqBiDirEdges(self.rawGraph)

    @property
    def numSelfEdges(self):
        return snap.CntSelfEdges(self.rawGraph)

    @property
    def numUniqueDirectedEdges(self):
        return snap.CntUniqDirEdges(self.rawGraph)

    @property
    def numUniqueUndirectedEdges(self):
        return snap.CntUniqUndirEdges(self.rawGraph)

    @property
    def isConnected(self):
        return snap.IsConnected(self.rawGraph)

    @property
    def isWeaklyConnected(self):
        return snap.IsWeaklyConn(self.rawGraph)

    # more complicated properties
    # TODO: why are some of these getX and others properties? Do I really have a purpose for that?
    @property
    def degreeDistribution(self):
        result = snap.TFltPrV()
        resultMap = collections.defaultdict(lambda:0)
        snap.GetDegCnt(self.rawGraph, result)
        for x in result:
            resultMap[int(x.GetVal1())] = int(x.GetVal2())
        return resultMap

    def getNodesByDegree(self):
        result = snap.TIntPrV()
        nodesByDegree = collections.defaultdict(lambda: [])
        snap.GetNodeInDegV(self.rawGraph, result)
        for x in result:
            nodesByDegree[x.GetVal2()].append(self.node(x.GetVal1()))

        return nodesByDegree

    def getDegreeProportions(self):
        degrees = self.degreeDistribution
        for degree in degrees:
            degrees[degree] = float(degrees[degree]) / float(self.numNodes)

        return degrees

    # search

    def BFSTree(self, startNode, followOut=True, followIn=False):
        snid = SnapNode.toId(startNode)
        return SnapGraph(snap.GetBfsTree(self.rawGraph, snid, followOut, followIn))

    # connected components
    def sccs(self, returnNodes=True):
        """
        Returns a list of sets of nodes, or just the IDs if returnNodes is false (note that getting the nodes
        themselves adds overhead)
        """
        sccs = snap.TCnComV()
        sccList = []

        snap.GetSccs(self.rawGraph, sccs)

        for scc in sccs:
            sccList.append(SnapUtil.rawComponentToNodeSet(scc, self, returnNodes))
        sccList.sort(key=lambda x: len(x),reverse=True)
        return sccList

    def maxSccGraph(self):
        return SnapGraph(snap.GetMxScc(self.rawGraph))

    def wccs(self, returnNodes=True):
        """
        Returns a list of sets of nodes, or just the IDs if returnNodes is false (note that getting the nodes
        themselves adds overhead)
        """
        wccs = snap.TCnComV()
        wccList = []

        snap.GetWccs(self.rawGraph, wccs)

        for wcc in wccs:
            wccList.append(SnapUtil.rawComponentToNodeSet(wcc, self, returnNodes))
        wccList.sort(key=lambda x: len(x),reverse=True)
        return wccList

    def maxWccGraph(self):
        return SnapGraph(snap.GetMxWcc(self.rawGraph))

    # graph manipulation
    def addNode(self, nodeId):
        return self.rawGraph.AddNode(nodeId)

    def addEdge(self,source, destination):
        sourceId = SnapNode.toId(source)
        destId = SnapNode.toId(destination)
        return self.rawGraph.AddEdge(sourceId, destId)

    def deleteSelfEdges(self):
        snap.DelSelfEdges(self.rawGraph)

    def deleteZeroDegreeNodes(self):
        snap.DelZeroDegNodes(self.rawGraph)

    def __str__(self):
        return "SnapGraph (%d nodes, %d edges)" % (self.numNodes, self.numEdges)

class SnapNode(object):
    rawNode = None
    parentGraph = None

    def __init__(self, rawNode, parentGraph):
        self.rawNode = rawNode
        self.parentGraph = parentGraph

    @property
    def id(self):
        return self.rawNode.GetId()

    @property
    def outDegree(self):
        return self.rawNode.GetOutDeg()

    @property
    def inDegree(self):
        return self.rawNode.GetInDeg()

    @property
    def outNodes(self):
        # intentional convert to list (iterator isn't as useful)
        return [self.parentGraph[node] for node in self.rawNode.GetOutEdges()]

    @property
    def inNodes(self):
        # intentional convert to list (iterator isn't as useful)
        return [self.parentGraph[node] for node in self.rawNode.GetInEdges()]

    def hasEdgeTo(self,otherNode):
        oid = self.toId(otherNode)
        return self.rawNode.IsOutNId(oid)

    def hasEdgeFrom(self,otherNode):
        oid = self.toId(otherNode)
        return self.rawNode.IsInNId(oid)

    def isNeighborTo(self,otherNode):
        oid = self.toId(otherNode)
        return self.rawNode.IsNbrNId(oid)

    def nodesInWcc(self, returnNodes=True):
        nodes = snap.TIntV()
        snap.GetNodeWcc(self.parentGraph.rawGraph, self.id, nodes)
        return SnapUtil.rawComponentToNodeSet(nodes, self.parentGraph, returnNodes)

    def __repr__(self):
        return "<node %d>" % self.id

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id

    @staticmethod
    def toId(nodeOrInt):
        """
        Used by functions to instantly convert SnapNode -> its ID, or int (assumed to be ID) -> int.
        The idea is that you can pass a SnapNode or an int into any function, and it will work the same.
        """
        if isinstance(nodeOrInt,SnapNode):
            return nodeOrInt.id
        elif isinstance(nodeOrInt,int):
            return nodeOrInt
        else:
            raise ValueError, "Must pass a SnapNode or an integer ID"

class SnapEdge(object):
    edge = None
    parentGraph = None

    def __init__(self, rawEdge, parentGraph):
        self.edge = rawEdge
        self.parentGraph = parentGraph

    @property
    def sourceId(self):
        return self.edge.GetSrcNId()

    @property
    def destId(self):
        return self.edge.GetDstNId()

    @property
    def source(self):
        return self.parentGraph[self.sourceId]

    @property
    def destination(self):
        return self.parentGraph[self.destId]

class SnapUtil(object):
    @staticmethod
    def snappyerToSnapType(snappyerGraphType):
        mapping = {
            SnapGraph.TYPE_UNKNOWN: None,
            SnapGraph.TYPE_NONE: None,
            SnapGraph.TYPE_DIRECTED: snap.PNGraph,
            SnapGraph.TYPE_UNDIRECTED: snap.PUNGraph,
            SnapGraph.TYPE_NETWORK: snap.PNEANet
        }
        return mapping[snappyerGraphType]

    @staticmethod
    def rawComponentToNodeSet(component, graph, getNodes=True):
        nodeSet = set()
        for j in xrange(0,component.Len()):
            if getNodes:
                nodeSet.add(graph.node(component[j]))
            else:
                nodeSet.add(component[j])

        return nodeSet