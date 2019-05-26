from sympy import *
from graphviz import Digraph

class Node:
    '''
    pure node
    '''
    pass

class Instance:
    '''
    pure instance
    '''
    pass

class ObjectNode(Node):
    def __init__(self, name, P, C):
        '''
        :param name: a string "Triangle"
        :param P: a string "a b c"
        :param C: a string"self['a']+self['b']>self['c']&&self['a']+self['c']>self['b']&&self['b']+self['c']>self['a']"
        '''
        self.name = name
        self.P = P.split(" ")
        if self.P.count("") > 0:
            self.P.remove("")
        self.C = C
        self.instances = {}
        self.toSave = "ObjectNode\n" + name + "\n" + P + "\n" + C

class ObjectInstance(Instance):
    '''
    a certain or uncertain instance
    like triangle(a, b, c)
    '''
    def __init__(self, objNode, name, PV):
        '''
        :param objNode: an ObjectNode like ObjectNode("triangle", ..., ...)
        :param name: a string like "x"
        :param PV: a dict, properties->value {"a": 3, "b": 4, "c": 5}
        '''
        self.objNode = objNode
        self.PV = PV
        self.name = name
        objNode.instances[name] = self

    def isCertain(self):
        certain = True
        for p in self.PV:
            if isinstance(self.PV[p], ObjectInstance):
                certain = certain and self.PV[p].isCertain()
            elif hasattr(self.PV[p], "is_number"):
                '''when the value is a sympy object, use is_number to judge'''
                certain = certain and self.PV[p].is_number
            if certain == False:
                break
        return certain

    def isLegal(self):
        '''
        indicating whether the instance satisfies all the constraints
        for example: when a triangle has a=1, b=2 and c=3, then this function returns False
        :return: True/False
        '''
        if self.isCertain() == False:
            '''cannot judge when not certain'''
            return True
        legal = eval(self.objNode.C)
        return legal

    def __getitem__(self, item):
        '''for Instance["xxx"]'''
        return self.PV[item]

    def __setitem__(self, key, value):
        '''for Instance["xxx"] = xxx'''
        self.PV[key] = value

    def __repr__(self):
        '''for print(self)'''
        return "ObjectNode " + self.objNode.name + ": " + self.name + "\n" + str(self.PV)


class OperationNode(Node):
    def __init__(self, name, input, output, f):
        '''
        :param input: a list [objNode1, objNode2, objNode3, ..., objNodeN]
        :param output: a list [objNode1, objNode2, objNode3, ..., objNodeN]
        :param f: a string: input->output such as "self.output['x']= self.input[0]['a'] + self.input[0]['b'] + self.input[0]['c']"
        '''
        self.name = name
        self.input = input
        self.output = output
        self.f = f
        self.instances = []
        self.toSave = "OperationNode\n" + name + "\n"
        cnt = 0
        for objNode in input:
            if cnt != 0:
                self.toSave += " "
            cnt += 1
            self.toSave += objNode.name
        cnt = 0
        self.toSave += "\n"
        for objNode in output:
            if cnt != 0:
                self.toSave += " "
            cnt += 1
            self.toSave += objNode.name
        self.toSave += "\n" + f

class OperationInstance(Instance):
    def __init__(self, opNode, input, output):
        '''
        :param opNode: an OperationNode, like get real part of a complex number
        :param input: a list including serveral ObjectInstances [objIns1, objIns2, ..., objInsN]
        :param output: a list including serveral ObjectInstances [objIns1, objIns2, ..., objInsN]
        '''
        self.opNode = opNode
        '''examine whether the input satisfies the opNode's type'''
        '''
        judge = True
        for index in range(0, len(input)):
            judge = judge and isinstance(input[index], opNode.input[index])
            if judge == False:
                break
        '''
        self.input = input
        self.output = output
        self.opNode.instances.append(self)

    def calculate(self):
        '''let output = f(input)'''
        exec(self.opNode.f)


class ConstraintNode(Node):
    def __init__(self, name, input, C):
        '''
        :param name: a string like "ComplexConjugate"
        :param input: a list [objNode1, objNode1, ..., objNodeN]
        :param C: a string "self.input[0].a==self.input[1].a&&self.input[0].b==self.input[1].b"
        '''
        self.name = name
        self.input = input
        self.C = C
        self.instances = []
        self.toSave = "ConstraintNode\n" + name + "\n"
        cnt = 0
        for objNode in input:
            if cnt != 0:
                self.toSave += " "
            cnt += 1
            self.toSave += objNode.name
        self.toSave += "\n" + self.C

class ConstraintInstance(Instance):
    def __init__(self, conNode, input):
        '''
        :param conNode: a ConstraintNode
        :param input: a list [objIns1, objIns2, ..., objInsN]
        '''
        self.conNode = conNode
        self.input = input
        self.conNode.instances.append(self)

    def isLegal(self):
        '''
        :return: whether the input satisfies all the constraints of the ConstraintNode
        '''
        return eval(self.conNode.C)


class MathGraph:
    def __init__(self):
        self.objNodes = {}
        self.opNodes = {}
        self.conNodes = {}
        self.toSave = ""

    def addObjectNode(self, name, P, C):
        self.objNodes[name] = ObjectNode(name, P, C)
        if self.toSave != "":
            self.toSave += "\n"
        self.toSave += self.objNodes[name].toSave

    def addOperationNode(self, name, input, output, f):
        self.opNodes[name] = OperationNode(name, input, output, f)
        if self.toSave != "":
            self.toSave += "\n"
        self.toSave += self.opNodes[name].toSave

    def addConstraintNode(self, name, input, C):
        self.conNodes[name] = ConstraintNode(name, input, C)
        if self.toSave != "":
            self.toSave += "\n"
        self.toSave += self.conNodes[name].toSave

    def saveFile(self, filename):
        '''save the graph as a file'''
        #print(self.toSave)
        file = open(filename, 'w')
        file.write(self.toSave)

    def view(self, filename):
        '''view the graph'''
        g = Digraph(filename)
        for objNode in self.objNodes:
            g.node(objNode)
        for opNode in self.opNodes:
            g.node(opNode, shape="box")
            for i in self.opNodes[opNode].input:
                g.edge(i.name, opNode)
            for i in self.opNodes[opNode].output:
                g.edge(opNode, i.name)
        for conNode in self.conNodes:
            g.node(conNode, shape="parrallelogram")
            for i in self.conNodes[conNode].input:
                g.edge(i.name, conNode)
        g.view(filename)

def loadFile(filename):
    '''
    load new graph from certain file
    :return : return a MathGraph object
    '''
    file = open(filename, 'r')
    graph = MathGraph()
    while True:
        s = file.readline()
        if s == "":
            '''when the file is finished'''
            break
        s = s.strip()
        if s == "ObjectNode":
            '''load ObjectNode(name, P, C)'''
            name = file.readline().strip()
            P = file.readline().strip()
            C = file.readline().strip()
            graph.addObjectNode(name, P, C)
        elif s == "OperationNode":
            '''load OperationNode(name, input, output, f)'''
            name = file.readline().strip()
            inputstr = file.readline().strip().split(" ")
            outputstr = file.readline().strip().split(" ")
            f = file.readline().strip()
            input = []
            output = []
            for i in inputstr:
                if i != "":
                    input.append(graph.objNodes[i])
            for o in outputstr:
                if o != "":
                    output.append(graph.objNodes[o])
            graph.addOperationNode(name, input, output, f)
        elif s == "ConstraintNode(name, input, C)":
            '''load ConstraintNode'''
            name = file.readline().strip()
            inputstr = file.readline().strip().split(" ")
            C = file.readline().strip()
            input = []
            for i in inputstr:
                input.append(graph.objNodes[i])
            graph.addConstraintNode(name, input, C)
    return graph
























