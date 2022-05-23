import random
import re
import copy
from extend_graph_XOR4 import ExtendGraph_XOR4
from CONSTANT import *


class SingleGraph:
    def __init__(self):
        self.Node = []
        self.NodeFro = dict()  # in-node
        self.NodeOut = dict()  # out-node
        self.TopologyList = []  # Topology


class SingleReduceGraph:
    def __init__(self):
        self.S = []
        self.Edge = []
        self.Cost = 0
        self.NodeOut = dict()

    def ComputeNodeOut(self):
        for i in range(len(self.S)):
            node = self.S[i]
            # for

            node1 = self.Edge[i][0]
            node2 = self.Edge[i][1]
            if node1 not in self.NodeOut.keys():
                self.NodeOut[node1] = set()
            if node2 not in self.NodeOut.keys():
                self.NodeOut[node2] = set()
            self.NodeOut[node1].add(node)
            self.NodeOut[node2].add(node)


class ExtendGraph:
    def __init__(self, size):
        self.Size = size
        self.Base = []  # base node
        self.TargetNode = []  # target node
        self.Value = dict()  # value of node
        self.HammingSet = dict()

        self.Node = []
        self.NodeFro = dict()
        self.NodeOut = dict()
        self.TopologyList = []

        self.XOR3NodeSet = []  # node representing a 3-input xor gate
        self.XOR4NodeSet = []  # node representing a 4-input xor gate
        self.CanGetSet = dict()  # ReachablitySet
        self.CanFromSet = dict()  # input node
        self.NumberInNode = dict()
        self.CostInNode = dict()
        self.AllSingleGraph = []
        self.outputdict = dict()
        self.Xor2Count = 0
        self.Xor3Count = 0
        self.Xor4Count = 0
        # for XOR3
        self.MinCost1 = 100000
        self.MinNum1 = []
        self.MinDepth1 = []
        self.MinCost0 = []
        self.MinNum0 = []
        self.MinDepth0 = []
        # for XOR4
        self.MinCost = 100000
        self.MinNum = []
        self.MinDepth = []

    def ReadFromLS19(self):
        FileName = "seq.txt"
        outfile = "myseq.txt"
        nodedict = dict()
        nextnodenum = self.Size
        for i in range(self.Size):
            nodedict[i] = i
        with open(FileName, 'r') as f:
            with open(outfile, 'w') as g:
                line = f.readline().replace('\n', '')
                if line != '':
                    g.write("{}\n".format(line))
                    line = f.readline().replace('\n', '')

                while line:
                    num = re.findall('[a-z]\d+', line)
                    num0 = int(num[0][1:])
                    num1 = int(num[1][1:])
                    num2 = int(num[2][1:])
                    symbol_0 = num[0][0]
                    symbol_1 = num[1][0]
                    symbol_2 = num[2][0]

                    if symbol_1 == 't':
                        num1 = nodedict[num1]
                    if symbol_2 == 't':
                        num2 = nodedict[num2]
                    nodedict[num0] = nextnodenum
                    num0 = nextnodenum
                    nextnodenum += 1
                    if len(num) == 3:
                        g.write("t[{}] = t[{}] + t[{}]\n".format(num0, num1, num2))
                    else:
                        g.write("t[{}] = t[{}] + t[{}]  y[{}]\n".format(num0, num1, num2, num[3]))
                    line = f.readline().replace('\n', '')

    def ReadFromSLP(self):
        FileName = "seq.txt"
        outfile = "myseq.txt"
        nodedict = dict()
        nextnodenum = self.Size
        for i in range(self.Size):
            nodedict[i] = i
        nodedict_y = dict()
        for i in range(self.Size):
            nodedict_y[i] = i
        with open(FileName, 'r') as f:
            with open(outfile, 'w') as g:
                line = f.readline().replace('\n', '')
                if line != '':
                    g.write("{}\n".format(line))
                    line = f.readline().replace('\n', '')

                while line:
                    num = re.findall('[a-z]\d+', line)
                    num0 = int(num[0][1:])
                    num1 = int(num[1][1:])
                    num2 = int(num[2][1:])
                    symbol_0 = num[0][0]
                    symbol_1 = num[1][0]
                    symbol_2 = num[2][0]
                    outnode = -1
                    if line[0] == 'y':
                        outnode = num0

                    if symbol_1 == 'y':
                        num1 = nodedict_y[num1]
                    elif symbol_1 == 't':
                        num1 = nodedict[num1]
                    if symbol_2 == 'y':
                        num2 = nodedict_y[num2]
                    elif symbol_2 == 't':
                        num2 = nodedict[num2]
                    if symbol_0 == 'y':
                        nodedict_y[num0] = nextnodenum
                    else:
                        nodedict[num0] = nextnodenum
                    num0 = nextnodenum
                    nextnodenum += 1
                    if line[0] != 'y':
                        g.write("t[{}] = t[{}] + t[{}]\n".format(num0, num1, num2))
                    else:
                        g.write("t[{}] = t[{}] + t[{}]  y[{}]\n".format(num0, num1, num2, outnode))
                    line = f.readline().replace('\n', '')

    def ReadFromXiang(self):
        FileName = "seq.txt"
        outfile = "myseq.txt"
        nodedict = dict()
        nextnodenum = self.Size
        for i in range(self.Size):
            nodedict[i] = i
        with open(FileName, 'r') as f:
            with open(outfile, 'w') as g:
                line = f.readline().replace('\n', '')
                if line != '':
                    g.write("{}\n".format(line))
                    line = f.readline().replace('\n', '')

                while line:
                    num = re.findall('\d+', line)
                    num0 = int(num[0])
                    num1 = int(num[1])
                    num2 = int(num[2])

                    num1 = nodedict[num1]
                    num2 = nodedict[num2]
                    nodedict[num0] = nextnodenum
                    num0 = nextnodenum
                    nextnodenum += 1
                    if len(num) == 3:
                        g.write("t[{}] = t[{}] + t[{}]\n".format(num0, num1, num2))
                    else:
                        g.write("t[{}] = t[{}] + t[{}]  y[{}]\n".format(num0, num1, num2, num[3]))
                    line = f.readline().replace('\n', '')

    def ReadFromXiang21(self):
        FileName = "seq.txt"
        outfile = "myseq.txt"
        nodedict = dict()
        nextnodenum = self.Size
        for i in range(self.Size):
            nodedict[i] = i
        with open(FileName, 'r') as f:
            with open(outfile, 'w') as g:
                line = f.readline().replace('\n', '')
                if line != '':
                    g.write("{}\n".format(line))
                    line = f.readline().replace('\n', '')

                while line:
                    num = re.findall('\d+', line)
                    num0 = int(num[1])
                    num1 = int(num[2])
                    num2 = int(num[3])

                    num1 = nodedict[num1]
                    num2 = nodedict[num2]
                    nodedict[num0] = nextnodenum
                    num0 = nextnodenum
                    nextnodenum += 1
                    if len(num) == 4:
                        g.write("t[{}] = t[{}] + t[{}]\n".format(num0, num1, num2))
                    else:
                        g.write("t[{}] = t[{}] + t[{}]  y[{}]\n".format(num0, num1, num2, num[4]))
                    line = f.readline().replace('\n', '')

    def ReadFromSeq(self):

        num = 1
        for i in range(self.Size):
            self.Value[str(i)] = num
            self.HammingSet[str(i)] = set()
            self.HammingSet[str(i)].add(str(i))
            num *= 2

        FileName = "myseq.txt"
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
                    if symbol121:
                        self.outputdict[int(num[3])] = int(num[0])
                    if symbol131:
                        self.outputdict[int(num[4])] = int(num[0])

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
    def outputHWfile(NodeFro, outputnode):
        file = "HWfile"
        with open(file, 'w') as f:
            for node in NodeFro:
                f.write("a{},".format(int(node)))
            f.write('\n')

            iiii = 1
            for node in NodeFro:
                list111 = list(NodeFro[node][0])
                if len(NodeFro[node][0]) == 2:

                    f.write("XOR2 n{}(a{},a{},a{});\n".format(iiii, list111[0], list111[1], node))
                elif len(NodeFro[node][0]) == 3:
                    f.write("XOR3 n{}(a{},a{},a{},a{});\n".format(iiii, list111[0], list111[1], list111[2], node))
                elif len(NodeFro[node][0]) == 4:
                    f.write("XOR4 n{}(a{},a{},a{},a{},a{});\n".format(iiii, list111[0], list111[1], list111[2], list111[3], node))
                iiii += 1
            listnum = []
            for i in range(0, 8):
                listnum.append(outputnode[7-i])
            for i in range(0, 8):
                listnum.append(outputnode[15-i])
            for i in range(0, 8):
                listnum.append(outputnode[23-i])
            for i in range(0, 8):
                listnum.append(outputnode[31-i])
            for i in range(len(listnum)):
                f.write("a{},".format(listnum[i]))

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

    def ComputeCanFromSet(self):
        self.CanFromSet = dict()
        for node in self.Node:
            if node not in self.Base:
                self.CanFromSet[node] = []
                newNodes = []
                test = self.NodeFro[node][0]
                for i in self.NodeFro[node][0]:
                    newNodes.append(i)
                newnewNodes = []
                while len(newNodes):
                    for onenode in newNodes:
                        self.CanFromSet[node].append(onenode)
                        if onenode not in self.Base:
                            for i in self.NodeFro[onenode][0]:
                                newnewNodes.append(i)
                    newNodes = copy.deepcopy(newnewNodes)
                    newnewNodes = []

    def GenerateExtendGraph_with_XOR2(self):
        for node in self.Node:
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

                if len(AvailableNode) < 2:
                    continue
                for i in range(0, len(AvailableNode) - 1):
                    for j in range(i + 1, len(AvailableNode)):
                        node1 = AvailableNode[i]
                        node2 = AvailableNode[j]
                        if self.Value[node] == self.Value[node1] ^ self.Value[node2]:
                            if {node1, node2} not in self.NodeFro[node]:
                                self.NodeFro[node].append({node1, node2})

    def GenerateSingleGraph_with_XOR2(self):

        NodeFromNumber = dict()
        for node in self.NodeFro:
            NodeFromNumber[node] = len(self.NodeFro[node])


        number_single_graph = 1
        for node in self.NodeFro:
            num = len(self.NodeFro[node])
            number_single_graph *= num

        if number_single_graph <= 2 ** 12:
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

                result = ExtendGraph.TopologyOut(onegraph.Node, onegraph.NodeFro, onegraph.NodeOut, self.Base)
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

    def AlgorithmToReducedXOR3(self):
        Target = copy.deepcopy(self.TargetNode)
        self.XOR3NodeSet = []
        Xor2Count = self.Xor2Count
        Xor3Count = self.Xor3Count
        MinCost0 = -1
        depth0 = -1

        OUTNUM = 1
        for i in range(1, 10):
            if (i + 1) * COST2 > i * COST3:
                OUTNUM = i
            else:
                break

        currentOUTNUM = 1
        while currentOUTNUM <= OUTNUM:

            S = copy.deepcopy(self.Base)
            for node in self.XOR3NodeSet:
                S.append(node)
            U = []
            Edge = dict()
            for node in self.TopologyList:
                if node not in self.Base and node not in self.XOR3NodeSet and node in self.Node:
                    U.append(node)

            while len(U) > 0:
                NextNode = U[0]

                S.append(NextNode)
                U.remove(NextNode)

                nodefromset = list(self.NodeFro[NextNode][0])
                random.shuffle(nodefromset)
                for nodefrom in nodefromset:

                    if nodefrom not in self.Base and len(self.NodeOut[nodefrom]) == currentOUTNUM and nodefrom not in self.XOR3NodeSet and nodefrom not in Target:

                        is_used = 0
                        NeedToReduced = copy.deepcopy(self.NodeOut[nodefrom])
                        for NodeNeedToReduced in NeedToReduced:
                            if NodeNeedToReduced in self.XOR3NodeSet:
                                is_used = 1
                        if is_used:
                            continue
                        Xor3Count += currentOUTNUM
                        Xor2Count -= (currentOUTNUM + 1)

                        self.Node.remove(nodefrom)


                        node1and2 = list(self.NodeFro[nodefrom][0])
                        node1 = node1and2[0]
                        node2 = node1and2[1]
                        del self.NodeFro[nodefrom]
                        del self.NodeOut[nodefrom]


                        for nodeout in NeedToReduced:
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
                        break
            if currentOUTNUM == 1:

                Xor2Count = 0
                Xor3Count = 0

                for node in self.NodeFro:
                    if len(self.NodeFro[node][0]) == 2:
                        Xor2Count += 1
                    elif len(self.NodeFro[node][0]) == 3:
                        Xor3Count += 1

                MinCost0 = Xor2Count * COST2 + Xor3Count * COST3
                depth0 = ExtendGraph.GetDepth(self.Base, self.NodeFro)

            currentOUTNUM += 1

        Xor2Count = 0
        Xor3Count = 0

        for node in self.NodeFro:
            if len(self.NodeFro[node][0]) == 2:
                Xor2Count += 1
            elif len(self.NodeFro[node][0]) == 3:
                Xor3Count += 1
        MinCost1 = Xor2Count * COST2 + Xor3Count * COST3
        depth1 = ExtendGraph.GetDepth(self.Base, self.NodeFro)

        if MinCost1 <= 1 and depth1 < 100:
            print("2:{}  3:{}  all:{}".format(Xor2Count, Xor3Count, Xor2Count+Xor3Count))
            for node in self.NodeFro.keys():
                nodes = []
                for onenode in self.NodeFro[node][0]:
                    nodes.append(onenode)
                print("{}:{}".format(node, nodes))

        return [MinCost1, depth1, MinCost0, depth0]

    def FromAllSingleToBestXOR3(self):
        self.MinCost0 = 100000
        self.MinDepth0 = []
        self.MinNum0 = []
        self.MinCost1 = 100000
        self.MinNum1 = []
        self.MinDepth1 = []

        OnlyPrintOnce = 0

        for i in range(len(self.AllSingleGraph)):
            if i == 12:
                print(1)

            self.Node = copy.deepcopy(self.AllSingleGraph[i].Node)
            self.NodeFro = copy.deepcopy(self.AllSingleGraph[i].NodeFro)
            self.NodeOut = copy.deepcopy(self.AllSingleGraph[i].NodeOut)
            self.TopologyList = copy.deepcopy(self.AllSingleGraph[i].TopologyList)

            # print("depth: {}".format(ExtendGraph.GetDepth(self.Base, self.NodeFro)))


            [ThisCost1, depth1, ThisCost0, depth0] = self.AlgorithmToReducedXOR3()
            # ThisCost = self.AlgorithmToReducedXOR3_random()
            if i == 0:
                self.MinCost0 = ThisCost0
                self.MinDepth0.append(depth0)


                # print("-------{}---------".format(self.MinCost0))
                # num_xor2 = 0
                # num_xor3 = 0
                # for node in self.NodeFro.keys():
                #     if len(self.NodeFro[node][0]) == 2:
                #         num_xor2 += 1
                #     if len(self.NodeFro[node][0]) == 3:
                #         num_xor3 += 1
                # print("XOR2:{}, XOR3:{}".format(num_xor2, num_xor3))
                # for node in self.NodeFro.keys():
                #     nodes = []
                #     for onenode in self.NodeFro[node][0]:
                #         nodes.append(onenode)
                #     print("{}:{}".format(node, nodes))


            if ThisCost1 <= 10000 and OnlyPrintOnce == 0:
                OnlyPrintOnce += 1
                print("-------{}---------".format(ThisCost1))
                num_xor2 = 0
                num_xor3 = 0
                for node in self.NodeFro.keys():
                    if len(self.NodeFro[node][0]) == 2:
                        num_xor2 += 1
                    if len(self.NodeFro[node][0]) == 3:
                        num_xor3 += 1
                print("XOR2:{}, XOR3:{}".format(num_xor2, num_xor3))
                for node in self.NodeFro.keys():
                    nodes = []
                    for onenode in self.NodeFro[node][0]:
                        nodes.append(onenode)
                    print("{}:{}".format(node, nodes))

            if ThisCost1 < self.MinCost1:
                self.MinCost1 = ThisCost1
                self.MinNum1 = [i]
                self.MinDepth1 = [depth1]
            elif ThisCost1 == self.MinCost1:
                self.MinNum1.append(i)
                self.MinDepth1.append(depth1)

        print("XOR3")
        # print(self.MinCost0)
        # print(self.MinDepth0)
        print(self.MinCost1)
        print(self.MinDepth1)
        print(self.MinNum1)


    def AlgorithmToReducedXOR3_for_XOR4(self, NewGraph_with_XOR3):
        Target = copy.deepcopy(self.TargetNode)
        self.XOR3NodeSet = []
        Xor2Count = 0
        Xor3Count = 0

        OUTNUM = 0
        for i in range(1, 10):
            if (i + 1) * COST2 > i * COST3:
                OUTNUM = i
            else:
                break


        currentOUTNUM = 1
        while currentOUTNUM <= OUTNUM:

            S = copy.deepcopy(self.Base)
            for node in self.XOR3NodeSet:
                S.append(node)
            U = []
            Edge = dict()
            for node in self.TopologyList:
                if node not in self.Base and node not in self.XOR3NodeSet and node in self.Node:
                    U.append(node)


            while len(U) > 0:
                NextNode = U[0]

                S.append(NextNode)
                U.remove(NextNode)

                for nodefrom in self.NodeFro[NextNode][0]:

                    if nodefrom not in self.Base and len(self.NodeOut[nodefrom]) == currentOUTNUM and nodefrom not in self.XOR3NodeSet and nodefrom not in Target:

                        is_used = 0
                        NeedToReduced = copy.deepcopy(self.NodeOut[nodefrom])
                        for NodeNeedToReduced in NeedToReduced:
                            if NodeNeedToReduced in self.XOR3NodeSet:
                                is_used = 1
                        if is_used:
                            continue
                        Xor3Count += currentOUTNUM
                        Xor2Count -= (currentOUTNUM + 1)

                        self.Node.remove(nodefrom)


                        node1and2 = list(self.NodeFro[nodefrom][0])
                        node1 = node1and2[0]
                        node2 = node1and2[1]
                        del self.NodeFro[nodefrom]
                        del self.NodeOut[nodefrom]


                        for nodeout in NeedToReduced:
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

                        break
            currentOUTNUM += 1


        NewGraph_with_XOR3.Node = copy.deepcopy(self.Node)
        NewGraph_with_XOR3.NodeFro = copy.deepcopy(self.NodeFro)
        NewGraph_with_XOR3.NodeOut = copy.deepcopy(self.NodeOut)

        for node in NewGraph_with_XOR3.NodeFro:
            if len(NewGraph_with_XOR3.NodeFro[node][0]) == 3:
                NewGraph_with_XOR3.XOR3NodeSet.append(node)

    def FromBestXOR3ToExtendGraph_with_XOR3(self):
        if len(self.AllSingleGraph) > 32:
            NewAllSingleGraph = []
            if len(self.MinNum1) <= 32:
                for i in self.MinNum1:
                    NewAllSingleGraph.append(self.AllSingleGraph[i])
            else:
                for i in range(32):
                    NewAllSingleGraph.append(self.AllSingleGraph[i])
            self.AllSingleGraph = copy.deepcopy(NewAllSingleGraph)

        for i in range(len(self.AllSingleGraph)):
            NewGraph_with_XOR3 = ExtendGraph_XOR4(self.Size)
            NewGraph_with_XOR3.Base = copy.deepcopy(self.Base)
            NewGraph_with_XOR3.TargetNode = copy.deepcopy(self.TargetNode)
            NewGraph_with_XOR3.Value = copy.deepcopy(self.Value)
            NewGraph_with_XOR3.HammingSet = copy.deepcopy(self.HammingSet)

            self.Node = copy.deepcopy(self.AllSingleGraph[i].Node)
            self.NodeFro = copy.deepcopy(self.AllSingleGraph[i].NodeFro)
            self.NodeOut = copy.deepcopy(self.AllSingleGraph[i].NodeOut)
            self.TopologyList = copy.deepcopy(self.AllSingleGraph[i].TopologyList)


            self.AlgorithmToReducedXOR3_for_XOR4(NewGraph_with_XOR3)


            NewGraph_with_XOR3.ComputeCanGetSet()


            NewGraph_with_XOR3.GenerateExtendGraph_with_XOR3()


            NewGraph_with_XOR3.GenerateSingleGraph_with_XOR3()


            NewGraph_with_XOR3.FromAllSingleToBestXOR4()
            ThisCost = NewGraph_with_XOR3.MinCost
            Thisdepth = NewGraph_with_XOR3.MinDepth

            if ThisCost < self.MinCost:
                self.MinCost = ThisCost
                self.MinNum = [i]
                self.MinDepth = [Thisdepth]
            elif ThisCost == self.MinCost:
                self.MinNum.append(i)
                self.MinDepth.append(Thisdepth)

        print("---------MIN:---------")
        print(self.MinCost)
        print(self.MinDepth)
        print(self.MinNum)


    def run_XOR3(self):
        self.ReadFromXiang()

        self.ReadFromSeq()
        self.ComputeCanGetSet()
        self.GenerateExtendGraph_with_XOR2()
        self.GenerateSingleGraph_with_XOR2()
        self.FromAllSingleToBestXOR3()

        print("output node:")
        for i in range(len(self.outputdict)):
            print("{}:{}, ".format(i, self.outputdict[i]), end='')
        print('')

    # def run_XOR4(self):
    #     self.FromBestXOR3ToExtendGraph_with_XOR3()

    def run_XOR3_XOR4(self):
        self.ReadFromXiang()

        self.ReadFromSeq()
        self.ComputeCanGetSet()
        self.GenerateExtendGraph_with_XOR2()
        self.GenerateSingleGraph_with_XOR2()
        self.FromAllSingleToBestXOR3()
        self.FromBestXOR3ToExtendGraph_with_XOR3()

        print("output node:")
        for i in range(len(self.outputdict)):
            print("{}:{}, ".format(i, self.outputdict[i]), end='')
        print('')

    # def run_XOR2(self):
    #     # self.ReadFromXiang()
    #     self.ReadFromSLP()
    #
    #     self.ReadFromSeq()
    #     self.ComputeCanGetSet()
    #     self.GenerateExtendGraph_with_XOR2()
    #     self.GenerateSingleGraph_with_XOR2()
    #     print(self.MinCost0)
    #     print(self.MinDepth0)



if __name__ == "__main__":

    NumberBase = 32
    graph = ExtendGraph(NumberBase)
    # graph.ReadFromXiang()
    # graph.ReadFromSeq()

    print(graph.outputdict)


