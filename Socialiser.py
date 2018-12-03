import numpy as np
import concurrent.futures
import operator
import pyprind
import sys

class randomSocial:
    '''

    '''


    def __init__(self,graph, p=0.5):

        self.p = p
        self.graph = graph

    def simpleRandomSocialiserMultipleEdgesSelfConnectedDirected(self, nodes):

        for node1 in nodes:
            if node1.DNA.value == 'random':
                for node2 in nodes:
                    if 1.0-self.p <= np.random.uniform(low=0.0, high=1.0, size=None):
                        if node1 is not node2:
                            node1+node2
                        else:
                            if not node1.selfConnected and self.graph.selfConncetions:
                                 node1+node1

    def simpleRandomSocialiserSingleEdgeSelfConnectedDirected(self, nodes):

        for node1 in nodes:
            if node1.DNA.value == 'random':
                for node2 in nodes:
                    if not self.graph.checkSameEntryAdj(node1, node2,warning=False):
                        if 1.0 - self.p <= np.random.uniform(low=0.0, high=1.0, size=None):
                                node1 + node2


    def simpleRandomSocialiserSingleEdge(self):
        nodes = self.graph.N
        for node1 in nodes:
            if node1.DNA.value == 'random':
                for node2 in nodes:
                    if not self.graph.checkSameEntryAdj(node1, node2, warning=False) or not self.graph.checkSameEntryAdj(node2, node1, warning=False):
                        if 1.0 - self.p <= np.random.uniform(low=0.0, high=1.0, size=None):
                            if node1 is not node2:
                                node1 + node2


    def simpleRandomSocialiserThreaded(self, nodes):

          raise Exception('not implemented!')

class randomSocialwithDNA(randomSocial):

        def __init__(self, graph,percentageOfConnectionNodes, p=0.5):
            super(randomSocialwithDNA, self).__init__(graph, p)

            self.popularityPreferenceIntensity = None
            self.mutualPreferenceIntensity = None
            self.pathLenghtLimit = None

            # self.p = p
            # self.graph = graph
            self.percentageOfConnectionNodes = percentageOfConnectionNodes
            # self.selfConncetions = selfConncetions
        class _NodesScore:
            def __init__(self,node1,node2, score, graph):
                self.node1 = node1
                self.node2 = node2
                self.score = score
                self.graph = graph

            def addNodes(self):
                if not self.graph.checkSameEntryAdj(self.node1, self.node2,
                                                    warning=False) or not self.graph.checkSameEntryAdj(self.node2,
                                                                                                        self.node1,
                                                                                                        warning=False):
                       self.node1 + self.node2


        def simpleRandomSocialiserSingleEdge(self):

            NodesScoreListOfObjects = []
            nodes = self.graph.N

            for node1 in nodes:
                    for node2 in nodes:

                            if 1.0 - self.p <= np.random.uniform(low=0.0, high=1.0, size=None):
                                if node1 is not node2:

                                    NodesScoreListOfObjects.append(self._NodesScore(node1=node1, node2=node2, score=node1.getScore(node2) + node2.getScore(node1), graph=self.graph))

            NodesScoreListOfObjectsSorted = sorted(NodesScoreListOfObjects, key=lambda x: x.score, reverse=True)



            l = 0.0
            stoppingLen = len(NodesScoreListOfObjectsSorted)*self.percentageOfConnectionNodes/100
            for  NodesScoreObj in NodesScoreListOfObjectsSorted:

                        if l>= stoppingLen:
                            break
                        else:
                            NodesScoreObj.addNodes()
                        l +=1

class randomSocialwithDNAadvanced(randomSocialwithDNA):

    def __init__(self,popularityPreferenceIntensity,mutualPreferenceIntensity,pathLenghtLimit,graph,percentageOfConnectionNodes,connectionPercentageWithMatchedNodesWithRandomness=None, **kwargs):
        super(randomSocialwithDNAadvanced, self).__init__(graph=graph,percentageOfConnectionNodes=percentageOfConnectionNodes, p=0.5)
        self.popularityPreferenceIntensity = popularityPreferenceIntensity
        self.mutualPreferenceIntensity = mutualPreferenceIntensity
        self.pathLenghtLimit = pathLenghtLimit





    def simpleRandomSocialiserSingleEdge(self):
        print('socialising')
        NodesScoreListOfObjects = []
        nodes = self.graph.N
        print('Calculating node scores!')
        bar = pyprind.ProgBar(len(nodes)*len(nodes), stream=sys.stdout)


        for node1 in nodes:
            for node2 in nodes:

                if 1.0 - self.p <= np.random.uniform(low=0.0, high=1.0, size=None):
                    if node1 is not node2:
                        NodesScoreListOfObjects.append(self._NodesScore(node1=node1, node2=node2,
                                                                         score=node1.getScoreAdvanced(node2,popularityPreferenceIntensity=self.popularityPreferenceIntensity,mutualPreferenceIntensity=self.mutualPreferenceIntensity) + node2.getScoreAdvanced(
                                                                             node1,popularityPreferenceIntensity=self.popularityPreferenceIntensity,mutualPreferenceIntensity=self.mutualPreferenceIntensity), graph=self.graph))
                        bar.update()
        # NodesScoreListOfObjectsSorted = sorted(NodesScoreListOfObjects, key=lambda x: x.score, reverse=True)
        NodesScoreListOfObjectsSorted = sorted(NodesScoreListOfObjects, key=lambda x: x.score, reverse=True)
        l = 0.0

        stoppingLen = len(NodesScoreListOfObjectsSorted) * self.percentageOfConnectionNodes / 100

        bar = pyprind.ProgBar(stoppingLen, stream=sys.stdout)


        for NodesScoreObj in NodesScoreListOfObjectsSorted:

            if l >= stoppingLen:
                break
            else:
                NodesScoreObj.addNodes()
            bar.update()
            l += 1
        # bar.finish()

        if self.mutualPreferenceIntensity is not None:
                self.graph.adjPower(self.mutualPreferenceIntensity,self.graph._useGPU)








