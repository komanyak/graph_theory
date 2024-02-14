import copy


class Graph():
    # конструктор класса
    def __init__(self, matrix):
        self.matrix = matrix
        self._matrix_len = len(matrix)

    # весовая функция, принимает номеравершин,
    # возвращает вес ребра, связывающего их
    def weight(self, VertexI, VertexJ):
        return self.matrix[VertexI - 1][VertexJ - 1]

    # true, если между вершинами есть ребро, иначе - false
    def is_edge(self, VertexI, VertexJ):
        if self.matrix[VertexI - 1][VertexJ - 1] is not None:
            return True
        return False

    # функция, возвращающая матрицу смежности графа / орграфа;
    def adjacency_matrix(self):
        return copy.deepcopy(self.matrix)

    # функция, возвращающая список вершин смежных вершине v;
    def adjacency_list(self, v):
        adj_list = []
        for i in range(len(self.matrix)):
            if self.is_edge(v, i + 1):
                adj_list.append(i + 1)
        return adj_list

    # список рёбер
    def list_of_edges(self, v=None):
        edges = set()
        if v is not None:
            # Проверяем все исходящие рёбра из вершины v
            for i in range(len(self.matrix)):
                if self.matrix[v - 1][i] is not None:
                    edges.add((v, i + 1, self.matrix[v - 1][i]))
        else:
            # Возвращаем список всех ребер графа
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix)):
                    if self.matrix[i][j] is not None:
                        # Если граф неориентированный, добавляем ребро только если i < j,
                        # чтобы избежать дублирования ребер
                        if not self.is_directed():
                            if i < j and self.matrix[j][i] is not None:
                                edges.add((i + 1, j + 1, self.matrix[i][j]))
                        else:
                            edges.add((i + 1, j + 1, self.matrix[i][j]))

        return sorted(list(edges))

    # true, если граф ориентированный,
    # false, если граф простой
    def is_directed(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] != self.matrix[j][i]:
                    return True
        return False

    # получение матрицы смежности ассоциативного графа
    def associated_matrix(self):
        associated_matrix = self.adjacency_matrix()

        for i in range(self._matrix_len):
            for j in range(self._matrix_len):
                if self.is_edge(i, j):
                    associated_matrix[j][i] = associated_matrix[i][j]

        return associated_matrix
