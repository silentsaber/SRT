from node import *
#实数
Real = ObjectNode("Real", "x", "True", toSympy="self['x']")
#点
Point=ObjectNode("Point","x y", "True",spec_attr={"coordinate":"'('+str($x)+','+str($y)+')'"})
GetPoint=OperationNode("GetPoint",[Real,Real],[Point],"self.output[0]['x'],self.output[0]['y']=self.input[0]['x'],self.input[1]['x]",E=["self.output[0]['x']-self.input[0]['x']","self.output[0]['y']-self.input[1]['x']"])

#求中点
GetMidpoint=OperationNode("GetMidpoint",[Point,Point],[Point],"self.output[0]['x'],self.output[0]['y']=(self.input[0]['x']+self.input[1]['x'])/2,(self.input[0]['y']+self.input[1]['y'])/2",E=["self.output[0]['x']-(self.input[0]['x']+self.input[1]['x'])/2","self.output[0]['y']-(self.input[0]['y']+self.input[1]['y'])/2"])

#计算距离
GetDistance=ConstraintNode("GetDistance",[Point,Point,Real],"self.input[2]['x']**2==simplify((self.input[0]['x']-self.input[1]['x'])**2+(self.input[0]['y']-self.input[1]['y'])**2) and self.input[2]['x']>0",E=["self.input[2]['x']*self.input[2]['x']-((self.input[0]['x']-self.input[1]['x'])*(self.input[0]['x']-self.input[1]['x'])+(self.input[0]['y']-self.input[1]['y'])*(self.input[0]['y']-self.input[1]['y']))"])

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
#点到直线的距离
GetDistancePointToLine = OperationNode("GetDistancePointToLine",[Point,Line],[Real],"self.output[0]['x']=abs(self.input[1]['a']*self.input[0]['x']+self.input[1]['b']*self.input[0]['y']+self.input[1]['c'])/sqrt(self.input[1]['a']**2+self.input[1]['b']**2)",E=["self.output[0]['x']-abs(self.input[1]['a']*self.input[0]['x']+self.input[1]['b']*self.input[0]['y']+self.input[1]['c'])/sqrt(self.input[1]['a']**2+self.input[1]['b']**2)"])
#平行直线到直线的距离

#椭圆（焦点在x轴）
Ellipsex=ObjectNode("Ellipsex","a b","(self['a']>self['b'])&(self['b']>0)",spec_attr={"expression":"'x**2/'+str($a*$a)+'+y**2/'+str($b*$b)+'=1'"})
#获取椭圆的a
GetEllipsexa=OperationNode("GetEllipsexa",[Ellipsex],[Real],"self.output[0]['x']=self.input[0]['a']",E=["self.output[0]['x']-self.input[0]['a']"])
#由a、b生成椭圆
GetEllipsex=OperationNode("GetEllipsex",[Real,Real],[Ellipsex],"self.output[0]['a'],self.output[0]['b']=self.input[0]['x'],self.input[1]['x']",E=["self.output[0]['a']-self.input[0]['x']","self.output[0]['b']-self.input[1]['x']"])
#得到半焦距
GetEllipsexC=ConstraintNode("GetEllipsexC",[Ellipsex,Real],"self.input[1]['x']**2==(self.input[0]['a']**2-self.input[0]['b']**2) and self.input[1]['x']>0",E=["self.input[1]['x']**2-(self.input[0]['a']**2-self.input[0]['b']**2)"])
#左焦点
GetEllipsexLeftC=ConstraintNode("GetEllipsexLeftC",[Ellipsex,Point],"self.input[1]['x']**2==(self.input[0]['a']**2-self.input[0]['b']**2) and self.input[1]['y']==0 and self.input[1]['x']<0",E=["self.input[1]['x']**2-(self.input[0]['a']**2-self.input[0]['b']**2)","self.input[1]['y']"])
#右焦点
GetEllipsexRightC=ConstraintNode("GetEllipsexRightC",[Ellipsex,Point],"self.input[1]['x']**2==simplify((self.input[0]['a']**2-self.input[0]['b']**2)) and self.input[1]['y']==0 and self.input[1]['x']>0",E=["self.input[1]['x']**2-(self.input[0]['a']**2-self.input[0]['b']**2)","self.input[1]['y']"])
#椭圆过点
PointOnEllipsex=ConstraintNode("PointOnEllipsex",[Point,Ellipsex],"simplify(self.input[0]['x']**2/self.input[1]['a']**2+self.input[0]['y']**2/self.input[1]['b']**2)==1",E=["self.input[0]['x']**2/self.input[1]['a']**2+self.input[0]['y']**2/self.input[1]['b']**2-1"])
#求直线与椭圆交点
LineIntersectEllipsex=ConstraintNode("LineIntersectEllipsex",[Point,Point,Line,Ellipsex],"simplify(self.input[0]['x']**2/self.input[3]['a']**2+self.input[0]['y']**2/self.input[3]['b']**2)==1 and simplify(self.input[1]['x']**2/self.input[3]['a']**2+self.input[1]['y']**2/self.input[3]['b']**2)==1 and self.input[2]['a']*self.input[0]['x']+self.input[2]['b']*self.input[0]['y']+self.input[2]['c']==0 and self.input[2]['a']*self.input[1]['x']+self.input[2]['b']*self.input[1]['y']+self.input[2]['c']==0 and  (self.input[0]['x']>self.input[1]['x'])|((self.input[0]['x']==self.input[1]['x'])&(self.input[0]['y']>self.input[1]['y']))",E=["self.input[0]['x']**2/self.input[3]['a']**2+self.input[0]['y']**2/self.input[3]['b']**2-1","self.input[1]['x']**2/self.input[3]['a']**2+self.input[1]['y']**2/self.input[3]['b']**2-1","self.input[2]['a']*self.input[0]['x']+self.input[2]['b']*self.input[0]['y']+self.input[2]['c']","self.input[2]['a']*self.input[1]['x']+self.input[2]['b']*self.input[1]['y']+self.input[2]['c']"])
#求离心率
GetEllipsexEccentricity=ConstraintNode("GetEllipsexEccentricity",[Ellipsex,Real],"self.input[1]['x']**2==(self.input[0]['a']**2-self.input[0]['b']**2)/(self.input[0]['a]**2) and self.input[1]['x']>0",E=["self.input[1]['x']**2-(self.input[0]['a']**2-self.input[0]['b']**2)/(self.input[0]['a']**2)"])
#求准线
#GetEllipsexDirectrix=ConstraintNode("GetEllipsexDirectrix",[Ellipsex,Line],"self.input")

#圆
Circle=ObjectNode("Circle","a b r","self['r']>0",toSympy="",spec_attr={"expression":"'(x-'+str($a)+')**2+(y-'+str($b)+')**2='+str($r**2)"})
#生成一个圆
GenerateCircle=OperationNode("GenerateCircle",[Real,Real,Real],[Circle],"self.output[0]['a'],self.output[0]['b'],self.output[0]['r']=self.input[0]['x'],self.input[1]['x'],self.input[2]['x']",E=["self.output[0]['a']-self.input[0]['x']","self.output[0]['b']-self.input[1]['x']","self.output[0]['r']-self.input[2]['x']"])
#获取圆的半径
GetCircleR=OperationNode("GetCircleR",[Circle],[Real],"self.output[0]['x']=self.input[0]['r']",E=["self.output[0]['x']-self.input[0]['r']"])
#获取圆的圆心
GetCircleCenter=OperationNode("GetCircleCenter",[Circle],[Point],"self.output[0]['x'],self.output[0]['y']=self.input[0]['a'],self.input[0]['b']",E=["self.output[0]['x']-self.input[0]['a']","self.output[0]['y']-self.input[0]['b']"])
#点在圆上
PointOnCircle = ConstraintNode("PointOnCircle", [Circle,Point], "(self.input[0]['a']-self.input[1]['x'])**2+(self.input[0]['b']-self.input[1]['y'])**2==self.input[0]['r']**2",E=["(self.input[0]['a']-self.input[1]['x'])**2+(self.input[0]['b']-self.input[1]['y'])**2-self.input[0]['r']**2"])
#点在圆内
PointInCircle = ConstraintNode("PointInCircle", [Circle,Point], "(self.input[0]['a']-self.input[1]['x'])**2+(self.input[0]['b']-self.input[1]['y'])**2 < self.input[0]['r']**2")
#点在圆外
PointOutCircle = ConstraintNode("PointOutCircle", [Circle,Point], "(self.input[0]['a']-self.input[1]['x'])**2+(self.input[0]['b']-self.input[1]['y'])**2 > self.input[0]['r']**2")
#直线和圆相交
LineIntersectCircle = ConstraintNode("LineIntersectCircle",[Line,Circle,Point,Point],"self.input[0]['a']*self.input[2]['x']+self.input[0]['b']*self.input[2]['y']+self.input[0]['c']==0 and self.input[0]['a']*self.input[3]['x']+self.input[0]['b']*self.input[3]['y']+self.input[0]['c']==0 and (self.input[1]['a']-self.input[2]['x'])**2+(self.input[1]['b']-self.input[2]['y'])**2==self.input[1]['r']**2 and (self.input[1]['a']-self.input[3]['x'])**2+(self.input[1]['b']-self.input[3]['y'])**2==self.input[1]['r']**2 and (self.input[2]['x']<self.input[3]['x'] or (self.input[2]['x']==self.input[3]['x'] and self.input[2]['y']<self.input[3]['y']))",E=["self.input[0]['a']*self.input[2]['x']+self.input[0]['b']*self.input[2]['y']+self.input[0]['c']","self.input[0]['a']*self.input[3]['x']+self.input[0]['b']*self.input[3]['y']+self.input[0]['c']","(self.input[1]['a']-self.input[2]['x'])**2+(self.input[1]['b']-self.input[2]['y'])**2-self.input[1]['r']**2","(self.input[1]['a']-self.input[3]['x'])**2+(self.input[1]['b']-self.input[3]['y'])**2-self.input[1]['r']**2"])
#直线到圆的距离   (圆上的点到直线的最短距离)
GetDistanceLineToCircle = OperationNode("GetDistanceLineToCircle",[Line,Circle],[Real],"self.output[0]['x']=(abs(self.input[0]['a']*self.input[1]['a']+self.input[0]['b']*self.input[1]['b']+self.input[0]['c'])/sqrt(self.input[0]['a']**2+self.input[0]['b']**2)-self.input[1]['r'])",E=["self.output[0]['x']-(abs(self.input[0]['a']*self.input[1]['a']+self.input[0]['b']*self.input[1]['b']+self.input[0]['c'])/sqrt(self.input[0]['a']**2+self.input[0]['b']**2)-self.input[1]['r'])"])


node_names = ["Real", "Point","GetPoint","GetMidpoint","GetDistance",'Line', "GetLineb","PointOnLine", "GetLinea", "GetLinec","GetLine","Parallel","Vertical","Ellipsex","GetEllipsexa","GetEllipsex","GetEllipsexC","GetEllipsexLeftC","PointOnEllipsex","GetEllipsexEccentricity","Circle","GenerateCircle","GetCircleR","GetCircleCenter","PointOnCircle","PointInCircle","PointOutCircle","LineIntersectEllipsex","LineIntersectCircle","GetDistanceLineToCircle"]

nodes = {}
for name in node_names:
    exec("nodes['%s'] = %s" % (name, name))