from task0 import Graph as GraphModule


# модифицированный класс графа, расширяющий функционал обычного
class ModifiedGraph(GraphModule.Graph):
    def __init__(self, matrix):
        super().__init__(matrix)

    # добавить вершину в конец, соединив ее со всеми остальными нулевыми ребрами
    def add_vertex(self):
        for i in range(self._matrix_len):
            self._matrix[i].append(1000000)
        self._matrix.append([0] * (self._matrix_len + 1))
        self._matrix_len += 1
        return self._matrix

    # удалить указанную вершину
    def del_vertex(self, vertex):
        for i in range(self._matrix_len):
            self._matrix[i].pop(vertex)
        self._matrix.pop(vertex)
        self._matrix_len -= 1
        return self._matrix