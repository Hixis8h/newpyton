matrix = [
    [1,2,3],
    [4,5,6],
    [7,8,9]
]
students = [['Joe','Kim'],['Sam','Sue'],['Kenlly','Chris']]
scores = [
    [0,0,0],
    [0,0,0],
    [0,0,0]
]

matrix[0][1] = 10
print(matrix)
for row in matrix :
    for element in row : 
        print(element,end='')
        print()


    