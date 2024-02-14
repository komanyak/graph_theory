# список рёбер -> матрица
def edges_list_to_matrix(file):
    with open(file, "r") as f:
        lines = [s.split() for s in f.readlines()]

        NumVert = 0
        for line in lines:
            NumVert = max(NumVert, max([int(x) for x in line[:-1]]))

        matrix = [[None] * NumVert for j in range(NumVert)]

        for line in lines:
            line = [int(x) for x in line]
            if len(line) == 2:
                matrix[line[0] - 1][line[1] - 1] = 1
            if len(line) == 3:
                matrix[line[0] - 1][line[1] - 1] = line[-1]

    return matrix


# список смежности -> матрица смежности
def adjacency_list_to_matrix(file):
    lines = []
    NumVert = 0
    with open(file, 'r') as f:
        for s in f.readlines():
            line = [int(x) for x in s.split()]
            NumVert = max(NumVert, max(line))
            lines.append(line)

    matrix = [[None] * NumVert for j in range(NumVert)]

    for i in range(len(lines)):
        for x in lines[i]:
            matrix[i][x - 1] = 1

    return matrix


# матрица смежности
def adjacency_matrix_to_matrix(file):
    matrix = []
    with open(file, "r") as f:
        lines = f.readlines()
        for line in lines:
            matrix.append([int(x) for x in line.split()])

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 0:
                matrix[i][j] = None

    return matrix


# функция для вывода результатов работы программы
def print_results(results, output_file_path=None):
    if output_file_path:
        # записываем результаты в файл
        with open(output_file_path, "w") as f:
            f.write(results)
    else:
        # выводим результаты на экран
        print(results)
