# входные данные - матрица смежности
def adjacency_matrix_to_matrix(path):
    with open(path, "r") as file:
        matrix = []

        # прочитали матрицу смежности
        for line in file:
            matrix.append([int(s) for s in line.split()])

        # если в файле были нули (то есть отсутствие пути) - заменяем их на бесконечности
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                matrix[i][j] = matrix[i][j] if matrix[i][j] != 0 else 1000000

    return matrix


# входные данные - список ребер
def edges_list_to_matrix(path):
    with open(path, "r") as file:
        lines = file.readlines()

    # находим в списке ребер максимальное число из вершин
    # общее количество вершин будет этим числом - инициализируем матрицу
    maxim = 0
    for line in lines:
        maxim = max(maxim, max([int(s) for s in line.split()[:2]]))
    matrix = [[1000000] * maxim for j in range(maxim)]

    for line in lines:
        temp = [int(s) for s in line.split()]  # парсим строку ребра
        if len(temp) == 3:
            matrix[temp[0] - 1][temp[1] - 1] = temp[2]  # (i-1;j-1) ребро с весом temp[2]
        elif len(temp) == 2:
            matrix[temp[0] - 1][temp[1] - 1] = 1
    return matrix


# входные данные - список смежности
def adjacency_list_to_matrix(path):
    with open(path, "r") as file:
        lines = file.readlines()

    # выделили место под матрицу
    maxim = len(lines)
    matrix = [[1000000] * maxim for j in range(maxim)]
    current_row = 0

    for line in lines:
        temp = [int(s) for s in line.split()]  # парсим список смежности
        for elem in temp:
            matrix[current_row][elem - 1] = 1  # ( i-1;j-1) ребро с весом 1
        current_row += 1
    return matrix
