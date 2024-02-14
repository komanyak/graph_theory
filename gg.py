edges = set()
s = input()
while s != "123":


    s = s.split()
    s.sort()
    edges.add((s[0], s[1]))
    s = input()


for i in edges:
    print(i[0] + " -- " + i[-1])
