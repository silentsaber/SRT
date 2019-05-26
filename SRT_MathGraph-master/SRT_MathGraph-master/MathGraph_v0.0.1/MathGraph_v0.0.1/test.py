from node2 import *
from sympy import *

#声明一个数学图谱-复数
graph = MathGraph()
#添加实体类-实数
graph.addObjectNode("Real", "x", "im(self['x']) == 0")
#添加实体类-复数
graph.addObjectNode("Complex", "a b", "")
#添加操作类型-获取实部
graph.addOperationNode("GetRealPart", [graph.objNodes["Complex"]], [graph.objNodes["Real"]], "self.output[0]['x'] = re(self.input[0]['a'])")
#添加操作类型-获取虚部
graph.addOperationNode("GetImaginaryPart", [graph.objNodes["Complex"]], [graph.objNodes["Real"]], "self.output[0]['x'] = im(self.input[0]['b'])")
#添加操作类型-计算模长
graph.addOperationNode("CalcMod", [graph.objNodes["Complex"]], [graph.objNodes["Real"]], "self.output[0]['x'] = sqrt(self.input[0]['a']**2 + self.input[0]['b']**2)")
#添加操作类型-复数加法
graph.addOperationNode("ComplexAdd", [graph.objNodes["Complex"], graph.objNodes["Complex"]], [graph.objNodes["Complex"]], "self.output[0]['a'], self.output[0]['b'] = self.input[0]['a']+self.input[1]['a'], self.input[0]['b']+self.input[1]['b']")
#添加操作类型-计算共轭复数
graph.addOperationNode("GetConjugate", [graph.objNodes["Complex"]], [graph.objNodes["Complex"]], "self.output[0]['a'], self.output[0]['b'] = self.input[0]['a'], -self.input[0]['b']")
#添加约束-相等
graph.addConstraintNode("ComplexEqual", [graph.objNodes["Complex"], graph.objNodes["Complex"]], "self.input[0]['a']==self.input[1]['a'] && self.input[0]['b']== self.input[1]['b']")
#添加约束-共轭
graph.addConstraintNode("ComplexConjugate", [graph.objNodes["Complex"], graph.objNodes["Complex"]], "self.input[0]['a']==self.input[1]['a'] && self.input[0]['b']== -self.input[1]['b']")

'''
#读取现有的数学图谱-复数
graph = loadFile("SimpleComplex.txt")
'''
#声明一个复数实体
compl = ObjectInstance(graph.objNodes["Complex"], "compl", {"a": 3, "b": 4})
#声明一个实数实体
real = ObjectInstance(graph.objNodes["Real"], "real", {"x": 0})
#声明一个操作符将上面两个实体联系起来：计算复数的模长
link = OperationInstance(graph.opNodes["CalcMod"], [compl], [real])
#查看激活运算符前实数值
print(real)
#激活运算符
link.calculate()
#查看激活运算符后实数值
print(real)
#将图谱表示为图像存储在SimpleComplex.pdf中
graph.view("SimpleComplex")
#可以将图谱进行存储
#graph.saveFile("SimpleComplex.txt")










