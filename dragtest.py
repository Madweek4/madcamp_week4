lst = [("글자", [(1,1),(5,1),(1,5),(5,5)]), ("한글", [(10,10),(50,10),(10,50),(50,50)])]
drag = [(0,0),(3,0),(0,3),(3,3)]
result_lst = []

for text, coordinate in lst:
    x1 = coordinate[0][0]
    x2 = coordinate[1][0]
    y1 = coordinate[0][1]
    y2 = coordinate[2][1]

    if (drag[0][0] <= x1 <= drag[1][0] or drag[0][0] <= x2 <= drag[1][0]):
        if (drag[0][1] <= y1 <= drag[2][1] or drag[0][1] <= y2 <= drag[2][1]):
            result_lst.append(text)

x = (1,2)
print(x[0])
