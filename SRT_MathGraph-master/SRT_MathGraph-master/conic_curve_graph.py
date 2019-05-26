from node import *
#实数
Real = ObjectNode("Real", "x", "True", toSympy="self['x']")
#点
Point=ObjectNode("Point","x y", "True",spec_attr={"coordinate":"'('+str($x)+','+str($y)+')'"})
GetPoint=OperationNode("GetPoint",[Real,Real],[Point],"self.output[0]['x'],self.output[0]['y']=self.input[0]['x'],self.input[1]['x]",E=["self.output[0]['x']-self.input[0]['x']","self.output[0]['y']-self.input[1]['x']"])
#计算距离
GetDistance=OperationNode("GetDistance",[Point,Point],[Real],"self.output[0]['x']=sqrt((self.input[0]['x']-self.input[1]['x'])**2+(self.input[0]['y']-self.input[1]['y'])**2)",E=["self.output[0]['x']-sqrt((self.input[0]['x']-self.input[1]['x'])**2+(self.input[0]['y']-self.input[1]['y'])**2)"])
#直线,形式为ax+by+c=0
Line=ObjectNode("Line","a b c","self['a']*self['a']+self['b']*self['b']>0",E=["(self['c']-1)*self['c']","(self['c']-1)*(self['b']-1)*self['b']","(self['c']-1)*(self['b']-1)*(self['a']-1)"],spec_attr={"expression":"'('+str($a)+')*x+('+str($b)+')*y+('+str($c)+')=0'"})
#点在线上
PointOnLine=ConstraintNode("PointOnNode",[Point,Line],"self.input[1]['a']*self.input[0]['x']+self.input[1]['b']*self.input[0]['y']+self.input[1]['c']==0",E=["self.input[1]['a']*self.input[0]['x']+self.input[1]['b']*self.input[0]['y']+self.input[1]['c']"])
GetLinea=OperationNode("GetLinea",[Line],[Real],"self.output[0]['x']=self.input[0]['a']", E=["self.output[0]['x']-self.input[0]['a']"])
GetLineb=OperationNode("GetLineb",[Line],[Real], "self.output[0]['x']=self.input[0]['b']", E=["self.output[0]['x']-self.input[0]['b']"])
GetLinec=OperationNode("GetLinec",[Line],[Real], "self.output[0]['x']=self.input[0]['c']", E=["self.output[0]['x']-self.input[0]['c']"])
GetLine=ConstraintNode("GetLine",[Real,Real,Real,Line],"self.input[0]['x']*self.input[3]['b']==self.input[1]['x']*self.input[3]['a'] and self.input[0]['x']*self.input[3]['c']==self.input[2]['x']*self.input[3]['a'] and self.input[1]['x']*self.input[3]['c']==self.input[2]['x']*self.input[3]['b']",E=["self.input[0]['x']*self.input[3]['b']-self.input[1]['x']*self .input[3]['a']","self.input[0]['x']*self.input[3]['c']-self.input[2]['x']*self.input[3]['a']","self.input[1]['x']*self.input[3]['c']-self.input[2]['x']*self.input[3]['b']"])
#两直线平行
Parallel=ConstraintNode("Parallel",[Line,Line],"self.input[0]['a']*self.input[1]['b']==self.input[0]['b']*self.input[1]['a'] and !(self.input[0]['b']==self.input[1][b] and self.input[0]['c']==self.input[1]['c'] and self.input[0]['a']==self.input[1]['a']",E=["self.input[0]['a']*self.input[1]['b']-self.input[0]['b']*self.input[1]['a']"])
#两直线垂直
Vertical=ConstraintNode("Vertical",[Line,Line],"self.input[0]['a']*self.input[1]['a']+self.input[0]['b']*self.input[1]['b']==0",E=["self.input[0]['a']*self.input[1]['a']+self.input[0]['b']*self.input[1]['b']"])
#椭圆（焦点在x轴）
Ellipsex=ObjectNode("Ellipsex","a b","(self['a']>self['b'])&(self['b']>0)",spec_attr={"expression":"'x**2/'+str(a*a)+'y**2/'+str(b*b)+'=1'"})
#由a、b生成椭圆
GetEllipsex=OperationNode("GetEllipsex",[Real,Real],[Ellipsex],"self.output[0]['a'],self.output[0]['b']=self.input[0]['x'],self.input[1]['x']",E=["self.output[0]['a']-self.input[0]['x']","self.output[0]['b']-self.input[1]['x']"])
#得到半焦距
GetEllipsexC=OperationNode("GetEllipsexC",[Ellipsex],[Real],"self.output[0]['x']=sqrt(self.input[0]['a']**2-self.output[0]['b']**2)",E=["self.output[0]['x']-sqrt(self.input[0]['a']**2-self.output[0]['b']**2)"])
#左焦点
GetEllipsexLeftC=OperationNode("GetEllipsexLeftC",[Ellipsex],[Point],"self.output[0]['x'],self.output[0]['y']=-sqrt(self.input[0]['a']**2-self.output[0]['b']**2),0",E=["self.output[0]['x']+sqrt(self.input[0]['a']**2-self.output[0]['b']**2)","self.output[0]['y']"])
#右焦点
GetEllipsexRightC=OperationNode("GetEllipsexRightC",[Ellipsex],[Point],"self.output[0]['x'],self.output[0]['y']=sqrt(self.input[0]['a']**2-self.output[0]['b']**2),0",E=["self.output[0]['x']-sqrt(self.input[0]['a']**2-self.output[0]['b']**2)","self.output[0]['y']"])
#椭圆过点
PointOnEllipsex=ConstraintNode("PointOnEllipsex",[Point,Ellipsex],"self.input[0]['x']**2/self.input[1]['a']**2+self.input[0]['y']**2/self.input[1]['b']**2==1",E=["self.input[0]['x']**2/self.input[1]['a']**2+self.input[0]['y']**2/self.input[1]['b']**2-1"])

node_names = ["Real", "Point","GetPoint","GetDistance",'Line', "GetLineb","PointOnLine", "GetLinea", "GetLinec","GetLine","Parallel","Vertical","Ellipsex","GetEllipsex","GetEllipsexC","GetEllipsexLeftC","PointOnEllipsex"]
nodes = {}
for name in node_names:
    exec("nodes['%s'] = %s" % (name, name))