import copy


class Graph:
    # конструктор класса, принимающий матрицу из списка стратегий
    def __init__(self, matrix):
        self._matrix = matrix
        self._matrix_len = len(matrix)

    # возвращает вес ребра, соединяющее вершины i и j
    def weight(self, vertI, vertJ):
        return self._matrix[vertI][vertJ]

    # возвращает true, если ребро между вершинами i и j существует, иначе false
    def is_edge(self, vertI, vertJ):
        return self._matrix[vertI][vertJ] != 1000000

    # возвращает матрицу смежности графа (копию, чтобы избежать ее изменения в классе графа)
    def adjacency_matrix(self):
        return copy.deepcopy(self._matrix)

    @staticmethod
    # получение списка смежных вершин к vert
    def adjacency_list(matrix, vert):
        vertices = []
        for i in range(len(matrix)):
            if matrix[vert][i] != 1000000 and vert != i:
                vertices.append(i)
        return vertices

    # возвращает список ребер графа / список ребер графа, инцидентных или исходящих из вершины vert
    def list_of_edges(self, vert=None):
        edges = []
        if vert is None:  # ребра для графа
            for i in range(self._matrix_len):
                for j in range(self._matrix_len):
                    if self.is_edge(i, j) and i != j:
                        edges.append([i, j, self._matrix[i][j]])
        else:  # ребра для вершины
            for j in range(self._matrix_len):
                if self.is_edge(vert, j) and vert != j:
                    edges.append([vert, j, self._matrix[vert][j]])
                if self.is_edge(j, vert) and vert != j:
                    edges.append([j, vert, self._matrix[j][vert]])
        return edges

    # возвращает true, если граф ориентированный, иначе false
    def is_directed(self):
        for i in range(self._matrix_len):
            for j in range(i, self._matrix_len):
                if self._matrix[i][j] != self._matrix[j][i]:
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
