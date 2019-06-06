## 文件:
* solve.py (更改过其中的函数)
* conic_curve_graph.py(图谱)
* conic_question.txt(问题。  第一个能解，第二个不能解&卡死,第三个、第四个能解，第五个返回no valid subset)

## 问题：sqrt形式的方程、abs类的方程(a=sqrt(b**2+c**2))，sympy的solve解不了

解决:约束设置为 a**2==b**2+c**2


## 问题:solve([],["x","y"],dict=true)不会返回结果

解决:solve(["Zero*Zero"],["x","y","Zero"],set=true) 返回的结果中包含{[x,y,Zero],[x,y,0]}。第一个是变量，后一个是名称

更改之后的solve函数:
```
 #求解所有未知量
    results = solve(constraints, basic_symbols, set=True)
    # print(results)
    dresults = []
    if(len(results)>0):
        for re in results[1]:
            req = {}
            for index in range(len(results[0])):
                x=results[0][index]
                req[x] = re[index]
            dresults.append(req)
    # print(dresults)
    results=dresults
```

## 问题:抽象函数解不了，不等式组暂时不能处理