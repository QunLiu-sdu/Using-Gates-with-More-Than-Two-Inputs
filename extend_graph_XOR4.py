import copy
import random
import re
from CONSTANT import *

OUTNUM = 0
for i in range(1, 10):
    if (i + 1) * COST2 > i * COST3:
        OUTNUM = i
    else:
        break


class SingleGraph:
    def __init__(self):
        self.Node = []
        self.NodeFro = dict()
        self.NodeOut = dict()
        self.TopologyList = []


class ExtendGraph_XOR4:
    def __init__(self, size):
        self.Size = size
        self.Base = []
        self.TargetNode = []
        self.Value = dict()
        self.HammingSet = dict()

        self.Node = []
        self.NodeFro = dict()
        self.NodeOut = dict()
        self.TopologyList = []

        self.XOR3NodeSet = []
        self.XOR4NodeSet = []
        self.CanGetSet = dict()
        self.CanFromSet = dict()
        self.NumberInNode = dict()
        self.CostInNode = dict()
        self.AllSingleGraph = []
        self.Xor2Count = 0
        self.Xor3Count = 0
        self.Xor4Count = 0
        self.MinCost = 100000
        self.MinNum = []
        self.MinDepth = []


    def ReadFromSeq(self):
        num = 1
        for i in range(self.Size):
            self.Value[str(i)] = num
            self.HammingSet[str(i)] = set()
            self.HammingSet[str(i)].add(str(i))
            num *= 2

        FileName = "reduced_seq_from_xiang20_1223_1.txt"
        with open(FileName, 'r') as f:
            line = f.readline().replace('\n', '')
            if len(line) > 0:
                num = re.findall('\d+', line)
                self.Xor2Count = int(num[0])
            while line:
                line = f.readline().replace('\n', '')
                if line == '':
                    break

                symbol120 = 0
                symbol121 = 0
                symbol130 = 0
                symbol131 = 0
                num = re.findall('\d+', line)
                char_y = 0
                char = re.findall('y', line)
                if len(char) != 0:
                    char_y = 1
                if len(num) == 3 and char_y == 0:
                    symbol120 = 1
                elif len(num) == 4 and char_y == 1:
                    symbol121 = 1
                elif len(num) == 4 and char_y == 0:
                    symbol130 = 1
                elif len(num) == 5 and char_y == 1:
                    symbol131 = 1
                else:
                    print('read error')
                    exit()

                self.Node.append(num[0])
                if num[1] not in self.Node:
                    self.Node.append(num[1])
                if num[2] not in self.Node:
                    self.Node.append(num[2])

                if symbol130 or symbol131:
                    if num[3] not in self.Node:
                        self.Node.append(num[3])

                if symbol121 or symbol131:
                    self.TargetNode.append(num[0])


                if num[0] not in self.NodeOut.keys():
                    self.NodeOut[num[0]] = []
                if num[1] not in self.NodeOut.keys():
                    self.NodeOut[num[1]] = []
                if num[2] not in self.NodeOut.keys():
                    self.NodeOut[num[2]] = []
                self.NodeOut[num[1]].append(num[0])
                self.NodeOut[num[2]].append(num[0])

                if symbol130 or symbol131:
                    if num[3] not in self.NodeOut.keys():
                        self.NodeOut[num[3]] = []
                    self.NodeOut[num[3]].append(num[0])


                if num[0] not in self.NodeFro.keys():
                    self.NodeFro[num[0]] = []
                if num[1] not in self.NodeFro.keys():
                    self.NodeFro[num[1]] = []
                if num[2] not in self.NodeFro.keys():
                    self.NodeFro[num[2]] = []

                if symbol130 or symbol131:
                    if num[3] not in self.NodeFro.keys():
                        self.NodeFro[num[3]] = []
                    self.NodeFro[num[0]].append({num[1], num[2], num[3]})
                else:
                    self.NodeFro[num[0]].append({num[1], num[2]})


                if symbol130 or symbol131:
                    self.Value[num[0]] = self.Value[num[1]] ^ self.Value[num[2]] ^ self.Value[num[3]]
                else:
                    self.Value[num[0]] = self.Value[num[1]] ^ self.Value[num[2]]


                if symbol130 or symbol131:
                    self.HammingSet[num[0]] = copy.deepcopy(self.HammingSet[num[1]])
                    for weight in self.HammingSet[num[2]]:
                        if weight not in self.HammingSet[num[0]]:
                            self.HammingSet[num[0]].add(weight)
                        else:
                            self.HammingSet[num[0]].remove(weight)
                    for weight in self.HammingSet[num[3]]:
                        if weight not in self.HammingSet[num[0]]:
                            self.HammingSet[num[0]].add(weight)
                        else:
                            self.HammingSet[num[0]].remove(weight)
                else:
                    self.HammingSet[num[0]] = copy.deepcopy(self.HammingSet[num[1]])
                    for weight in self.HammingSet[num[2]]:
                        if weight not in self.HammingSet[num[0]]:
                            self.HammingSet[num[0]].add(weight)
                        else:
                            self.HammingSet[num[0]].remove(weight)


        for node in self.Node:
            if len(self.NodeFro[node]) == 0:
                self.Base.append(node)
                self.NodeFro.pop(node)

    @staticmethod
    def GetCost(edge):
        assert 2 <= len(edge) <= 4
        if len(edge) == 2:
            return COST2
        elif len(edge) == 3:
            return COST3
        elif len(edge) == 4:
            return COST4

    @staticmethod
    def TopologyOut(Node, NodeFrom, NodeOut, Base):
        ThisNode = copy.deepcopy(Node)


        NodeList = []


        NodeFromNumber = dict()
        NodeOutNumber = dict()
        for node in NodeFrom:
            NodeFromNumber[node] = 0
            fromset = NodeFrom[node]
            for i in range(len(fromset)):
                NodeFromNumber[node] += len(fromset[i])
        for node in NodeOut:
            NodeOutNumber[node] = len(NodeOut[node])


        while True:
            symbol = 0
            for node in ThisNode:
                if node in Base or NodeFromNumber[node] == 0:

                    ThisNode.remove(node)
                    NodeList.append(node)

                    for outnode in NodeOut[node]:
                        NodeFromNumber[outnode] -= 1
                    symbol = 1
                    break
            if symbol == 1:
                continue
            else:
                break


        if len(ThisNode) > 0:
            return []
        else:
            return NodeList

    @staticmethod
    def GetDepth(Base, NodeFro):
        NodeDepth = dict()
        for node in Base:
            NodeDepth[node] = 0
        NodeSet = []
        for node in NodeFro:
            NodeSet.append(node)
        while len(NodeSet) > 0:
            delete = -1
            for node in NodeSet:
                nofound = -1
                depth = -1
                for onenode in NodeFro[node][0]:
                    if onenode in NodeDepth:
                        depth = max(depth, NodeDepth[onenode] + 1)
                    else:
                        nofound = 1
                if nofound == 1:
                    continue
                else:
                    delete = 1
                    NodeDepth[node] = depth
                    NodeSet.remove(node)
                    break
            if delete == 1:
                continue

        MaxDepth = -1
        for node in NodeDepth:
            MaxDepth = max(MaxDepth, NodeDepth[node])
        return MaxDepth

    def ComputeCanGetSet(self):

        self.CanGetSet = dict()
        for node in self.Node:
            if node not in self.Base:
                self.CanGetSet[node] = []
                newNodes = self.NodeOut[node]
                newnewNodes = []
                while len(newNodes):
                    for onenode in newNodes:
                        self.CanGetSet[node].append(onenode)
                        for i in self.NodeOut[onenode]:
                            newnewNodes.append(i)
                    newNodes = copy.deepcopy(newnewNodes)
                    newnewNodes = []

    def GenerateExtendGraph_with_XOR3(self):

        for node in self.XOR3NodeSet:
            if node not in self.Base:
                AvailableNode = []
                for onenode in self.Node:
                    if onenode not in self.CanGetSet[node] and onenode != node:
                        AvailableNode.append(onenode)
                while True:
                    symbol = 0
                    for onenode in AvailableNode:
                        if self.HammingSet[node].issubset(self.HammingSet[onenode]):
                            AvailableNode.remove(onenode)
                            symbol = 1
                            break
                    if symbol == 1:
                        continue
                    else:
                        break

                if len(AvailableNode) < 3:
                    continue
                for i in range(0, len(AvailableNode) - 2):
                    for j in range(i + 1, len(AvailableNode) - 1):
                        for k in range(j + 1, len(AvailableNode)):
                            node1 = AvailableNode[i]
                            node2 = AvailableNode[j]
                            node3 = AvailableNode[k]
                            if self.Value[node] == self.Value[node1] ^ self.Value[node2] ^ self.Value[node3]:
                                if {node1, node2, node3} not in self.NodeFro[node]:
                                    self.NodeFro[node].append({node1, node2, node3})

    def GenerateSingleGraph_with_XOR3(self):
        NodeFromNumber = dict()
        for node in self.NodeFro:
            NodeFromNumber[node] = len(self.NodeFro[node])


        number_single_graph = 1
        for node in self.NodeFro:
            num = len(self.NodeFro[node])
            number_single_graph *= num

        if number_single_graph <= 2**10:
            a = SingleGraph()
            for node in self.Node:
                if node not in self.Base:
                    a.NodeFro[node] = []
            self.AllSingleGraph.append(a)
            for node in self.Node:
                if node not in self.Base:
                    if NodeFromNumber[node] == 1:
                        for onegraph in self.AllSingleGraph:
                            onegraph.NodeFro[node].append(self.NodeFro[node][0])
                    else:
                        times = NodeFromNumber[node]
                        AllSingleGraph_COPY = copy.deepcopy(self.AllSingleGraph)
                        self.AllSingleGraph = []
                        for i in range(0, times):
                            for onegraph in AllSingleGraph_COPY:
                                newgraph = copy.deepcopy(onegraph)
                                newgraph.NodeFro[node].append(self.NodeFro[node][i])
                                self.AllSingleGraph.append(newgraph)
        else:
            a = SingleGraph()
            for node in self.Node:
                if node not in self.Base:
                    line = copy.deepcopy(self.NodeFro[node][0])
                    a.NodeFro[node] = []
                    a.NodeFro[node].append(line)
            self.AllSingleGraph.append(a)
            for node in self.Node:
                if node not in self.Base and len(self.NodeFro[node]) > 1:
                    leng = len(self.NodeFro[node])
                    for num in range(1, leng):
                        b = copy.deepcopy(a)
                        b.NodeFro[node] = []
                        line = copy.deepcopy(self.NodeFro[node][num])
                        b.NodeFro[node].append(line)
                        self.AllSingleGraph.append(b)



        for onegraph in self.AllSingleGraph:

            for node in self.Node:
                onegraph.NodeOut[node] = []

            while True:
                symbol = 0

                for node in onegraph.NodeOut.keys():
                    onegraph.NodeOut[node] = []
                for oneedge in onegraph.NodeFro.keys():
                    node0 = oneedge
                    for node in onegraph.NodeFro[oneedge][0]:
                        onegraph.NodeOut[node].append(node0)
                for node in onegraph.NodeOut.keys():
                    if node not in self.Base and node not in self.TargetNode:
                        if len(onegraph.NodeOut[node]) == 0:
                            onegraph.NodeFro.pop(node)
                            onegraph.NodeOut.pop(node)
                            symbol = 1
                            break
                if symbol == 1:
                    continue
                else:
                    break

            for node in onegraph.NodeOut.keys():
                onegraph.Node.append(node)


        goodGraph = -1
        while True:
            symbol = 0
            for i in range(goodGraph + 1, len(self.AllSingleGraph)):
                onegraph = self.AllSingleGraph[i]

                result = ExtendGraph_XOR4.TopologyOut(onegraph.Node, onegraph.NodeFro, onegraph.NodeOut, self.Base)
                onegraph.TopologyList = copy.deepcopy(result)
                if not result:
                    self.AllSingleGraph.remove(onegraph)
                    goodGraph = i - 1
                    symbol = 1
                    break
            if symbol == 1:
                continue
            else:
                break

    def AlgorithmToReducedXOR4(self):
        Target = copy.deepcopy(self.TargetNode)
        self.XOR3NodeSet = []
        self.XOR4NodeSet = []
        Xor2Count = 0
        Xor3Count = 0
        Xor4Count = 0
        MinCost = 0
        depth = -1


        MAXOUTNUM1 = 1
        MAXOUTNUM2 = 1
        for i in range(2, 10):
            if i * COST2 + COST3 - i * COST4 > 0:
                MAXOUTNUM1 = i
            else:
                break
        for i in range(2, 10):
            if COST2 + COST3 - COST4 - (i - 1) * min((COST3 - COST2), (COST4 - COST3)) > 0:
                MAXOUTNUM2 = i
            else:
                break

        for node in self.NodeFro:
            if len(self.NodeFro[node][0]) == 3:
                Xor3Count += 1
                self.XOR3NodeSet.append(node)
            elif len(self.NodeFro[node][0]) == 2:
                Xor2Count += 1
            else:
                print("XOR number error!")
                assert 2 <= len(self.NodeFro[node][0]) <= 3


        currentOUTNUM1 = 1
        currentOUTNUM2 = 1
        while currentOUTNUM1 <= MAXOUTNUM1 or currentOUTNUM2 <= MAXOUTNUM2:

            S = copy.deepcopy(self.Base)
            for node in self.XOR3NodeSet:
                S.append(node)
            U = []
            Edge = dict()
            for node in self.TopologyList:
                if node not in self.Base and node not in self.XOR4NodeSet and node in self.Node:
                    U.append(node)

            while len(U) > 0:
                NextNode = U[0]
                # if NextNode == '57':
                #     print(1)

                S.append(NextNode)
                U.remove(NextNode)


                if len(self.NodeFro[NextNode][0]) == 2 and currentOUTNUM1 <= MAXOUTNUM1:
                    nodefromset = list(self.NodeFro[NextNode][0])
                    random.shuffle(nodefromset)
                    for nodefrom in nodefromset:

                        if nodefrom not in self.Base and len(self.NodeOut[nodefrom]) == currentOUTNUM1 and nodefrom in self.XOR3NodeSet and nodefrom not in self.XOR4NodeSet and nodefrom not in Target:

                            is_used = 0
                            NeedToReduced = copy.deepcopy(self.NodeOut[nodefrom])
                            for NodeNeedToReduced in NeedToReduced:
                                if NodeNeedToReduced in self.XOR4NodeSet and len(self.NodeFro[NodeNeedToReduced][0]) != 2:
                                    is_used = 1
                            if is_used:
                                continue
                            Xor2Count -= currentOUTNUM1
                            Xor3Count -= 1
                            Xor4Count += currentOUTNUM1

                            self.Node.remove(nodefrom)


                            node1and2and3 = list(self.NodeFro[nodefrom][0])
                            node1 = node1and2and3[0]
                            node2 = node1and2and3[1]
                            node3 = node1and2and3[2]


                            del self.NodeFro[nodefrom]
                            del self.NodeOut[nodefrom]



                            for nodeout in NeedToReduced:
                                self.XOR4NodeSet.append(nodeout)
                                if nodeout in self.XOR3NodeSet:
                                    self.XOR3NodeSet.remove(nodeout)
                                anothernode = ''
                                nodeout1and2 = list(self.NodeFro[nodeout][0])
                                for i in range(2):
                                    if nodeout1and2[i] != nodefrom:
                                        anothernode = nodeout1and2[i]
                                self.NodeFro[nodeout] = [{node1, node2, node3, anothernode}]
                                if nodefrom in self.NodeOut[node1]:
                                    self.NodeOut[node1].remove(nodefrom)
                                if nodeout not in self.NodeOut[node1]:
                                    self.NodeOut[node1].append(nodeout)
                                if nodefrom in self.NodeOut[node2]:
                                    self.NodeOut[node2].remove(nodefrom)
                                if nodeout not in self.NodeOut[node2]:
                                    self.NodeOut[node2].append(nodeout)
                                if nodefrom in self.NodeOut[node3]:
                                    self.NodeOut[node3].remove(nodefrom)
                                if nodeout not in self.NodeOut[node3]:
                                    self.NodeOut[node3].append(nodeout)
                            break

                elif len(self.NodeFro[NextNode][0]) == 3 and currentOUTNUM2 <= MAXOUTNUM2:
                    nodefromset = list(self.NodeFro[NextNode][0])
                    random.shuffle(nodefromset)
                    for nodefrom in nodefromset:

                        if nodefrom not in self.Base and len(self.NodeOut[nodefrom]) == currentOUTNUM2 and len(self.NodeFro[nodefrom][0]) == 2 and nodefrom not in Target:

                            is_used = 0
                            NeedToReduced = copy.deepcopy(self.NodeOut[nodefrom])
                            for NodeNeedToReduced in NeedToReduced:
                                if NodeNeedToReduced in self.XOR4NodeSet:
                                    is_used = 1
                            if is_used:
                                continue

                            NeedToReduced_XOR2 = []
                            NeedToReduced_XOR3 = []
                            for NodeNeedToReduced in NeedToReduced:
                                if len(self.NodeFro[NodeNeedToReduced][0]) == 2:
                                    NeedToReduced_XOR2.append(NodeNeedToReduced)
                                elif len(self.NodeFro[NodeNeedToReduced][0]) == 3:
                                    NeedToReduced_XOR3.append(NodeNeedToReduced)
                                else:
                                    print("error!")
                                    assert 2 <= len(self.NodeFro[NodeNeedToReduced][0]) <= 3


                            Xor2Count -= 1
                            Xor3Count -= 1
                            Xor4Count += 1
                            for leng in range(len(NeedToReduced_XOR2)):
                                Xor2Count -= 1
                                Xor3Count += 1
                            for leng in range(len(NeedToReduced_XOR3)):
                                if leng >= 1:
                                    Xor3Count -= 1
                                    Xor4Count += 1

                            self.Node.remove(nodefrom)


                            node1and2 = list(self.NodeFro[nodefrom][0])
                            node1 = node1and2[0]
                            node2 = node1and2[1]
                            del self.NodeFro[nodefrom]
                            del self.NodeOut[nodefrom]


                            for nodeout in NeedToReduced_XOR2:
                                self.XOR3NodeSet.append(nodeout)
                                anothernode = ''
                                nodeout1and2 = list(self.NodeFro[nodeout][0])
                                for i in range(2):
                                    if nodeout1and2[i] != nodefrom:
                                        anothernode = nodeout1and2[i]
                                self.NodeFro[nodeout] = [{node1, node2, anothernode}]
                                if nodefrom in self.NodeOut[node1]:
                                    self.NodeOut[node1].remove(nodefrom)
                                if nodeout not in self.NodeOut[node1]:
                                    self.NodeOut[node1].append(nodeout)
                                if nodefrom in self.NodeOut[node2]:
                                    self.NodeOut[node2].remove(nodefrom)
                                if nodeout not in self.NodeOut[node2]:
                                    self.NodeOut[node2].append(nodeout)

                            for nodeout in NeedToReduced_XOR3:
                                self.XOR4NodeSet.append(nodeout)
                                nodeout1and2 = list(self.NodeFro[nodeout][0])
                                nodeout1and2.remove(nodefrom)
                                anothernode1 = nodeout1and2[0]
                                anothernode2 = nodeout1and2[1]

                                self.NodeFro[nodeout] = [{node1, node2, anothernode1, anothernode2}]
                                if nodefrom in self.NodeOut[node1]:
                                    self.NodeOut[node1].remove(nodefrom)
                                if nodeout not in self.NodeOut[node1]:
                                    self.NodeOut[node1].append(nodeout)
                                if nodefrom in self.NodeOut[node2]:
                                    self.NodeOut[node2].remove(nodefrom)
                                if nodeout not in self.NodeOut[node2]:
                                    self.NodeOut[node2].append(nodeout)

                            break
            currentOUTNUM1 += 1
            currentOUTNUM2 += 1

        Xor2Count = 0
        Xor3Count = 0
        Xor4Count = 0

        for node in self.NodeFro:
            if len(self.NodeFro[node][0]) == 2:
                Xor2Count += 1
            elif len(self.NodeFro[node][0]) == 3:
                Xor3Count += 1
            elif len(self.NodeFro[node][0]) == 4:
                Xor4Count += 1
        MinCost = COST2 * Xor2Count + COST3 * Xor3Count + COST4 * Xor4Count

        # if MinCost < 150.17:
        #     print(1)
        depth = ExtendGraph_XOR4.GetDepth(self.Base, self.NodeFro)
        return [MinCost, depth]

    def FromAllSingleToBestXOR4(self):
        self.MinCost = 100000
        self.MinNum = []
        self.MinDepth = []
        OnlyPrintOnce = 0

        for i in range(len(self.AllSingleGraph)):

            self.Node = copy.deepcopy(self.AllSingleGraph[i].Node)
            self.NodeFro = copy.deepcopy(self.AllSingleGraph[i].NodeFro)
            self.NodeOut = copy.deepcopy(self.AllSingleGraph[i].NodeOut)
            self.TopologyList = copy.deepcopy(self.AllSingleGraph[i].TopologyList)

            require_nodefro = copy.deepcopy(self.AllSingleGraph[i].NodeFro)


            [ThisCost, depth] = self.AlgorithmToReducedXOR4()

            if ThisCost <= 10000 and OnlyPrintOnce == 0:
                OnlyPrintOnce += 1
                print("-------{}---------".format(ThisCost))
                num_xor2 = 0
                num_xor3 = 0
                num_xor4 = 0
                for node in self.NodeFro.keys():
                    if len(self.NodeFro[node][0]) == 2:
                        num_xor2 += 1
                    if len(self.NodeFro[node][0]) == 3:
                        num_xor3 += 1
                    if len(self.NodeFro[node][0]) == 4:
                        num_xor4 += 1
                print("XOR2:{}, XOR3:{}, XOR4:{}".format(num_xor2, num_xor3, num_xor4))
                for node in self.NodeFro.keys():
                    nodes = []
                    for onenode in self.NodeFro[node][0]:
                        nodes.append(onenode)
                    print("{}:{}".format(node, nodes))
                print("-------previous------")
                for node in require_nodefro.keys():
                    nodes = []
                    for onenode in require_nodefro[node][0]:
                        nodes.append(onenode)
                    print("{}:{}".format(node, nodes))



            if ThisCost < self.MinCost:
                self.MinCost = ThisCost
                self.MinNum = [i]
                self.MinDepth = [depth]
            elif ThisCost == self.MinCost:
                self.MinNum.append(i)
                self.MinDepth.append(depth)

        print("XOR4")
        print(self.MinCost)
        print(self.MinDepth)
        print(self.MinNum)
