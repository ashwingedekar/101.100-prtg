List = []
print(List)

List.append(1)
List.append(33)
List.append('pikachu')
print(List)

for i in range(1,9):
    List.append(i)
    print(List)

List.append((5,6))
print(List)

List2 = ['tiger','raja']
List.append(List2)
print(List)
print(List[-1])