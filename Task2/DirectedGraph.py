from Task2 import AbstractConnectivity


class DirectedGraph(AbstractConnectivity.GraphConnectivity):
    def __init__(self, graph):
        super().__init__(graph)  # инициализируем матрицу смежности
        self.__graph = graph  # получаем граф

    # проверка на слабую связность графа через BFS из абстрактного класса
    def is_graph_weak_connected(self):
        return self.is_connected(self.__graph.associated_matrix())

    # подсчет и состав слабых компонент связности графа через BFS из абстрактного класса
    def count_weak_connected_components(self):

        return self.count_connected_components(self.__graph.associated_matrix())

    # алгоритм Косараджу (Косарайю)
    def kosaraju(self):
        # инициализация компонент, кол-ва компонент и транспонированной матрицы (инвертированного графа)
        components = []
        count_components = 0
        transpose_matrix = self.transpose_matrix(self._matrix)

        counters = [0] * self._matrix_len  # порядки выхода из вершин t_out для DFS
        vertices = [i for i in range(self._matrix_len)]  # массив вершин
        counter = [0]  # счетчик, который считает общий порядок выхода для всех вершин

        # запускаем DFS и удаляем вершины, принадлежащие дереву DFS, повторяем, пока вершины есть
        while len(vertices):
            dfs_result = self.DFS(vertices[0], counter, counters, self._matrix)
            for vertex in dfs_result:
                vertices.pop(vertices.index(vertex))

        counters_copy = [0] * self._matrix_len  # копия порядков выхода из вершин, чтобы не перезаписать нужные
        vertices = [i for i in range(self._matrix_len)]
        counter = [0]

        # запускаем DFS от вершины, имеющей наиболдьший порядок выхода
        while len(vertices):
            component = self.DFS(counters.index(max(counters)), counter, counters_copy, transpose_matrix)

            # запомнили компоненту и обновили счетчик компонент
            count_components += 1
            components.append(component)

            # удаляем вершины из этой компоненты и обнуляем их порядки, чтобы взять другую вершину для DFS
            for vertex in component:
                vertices.pop(vertices.index(vertex))
                counters[vertex] = 0

        # for i in range(len(components)):
        #     for j in range(len(components[i])):
        #         components[i][j] += 1

        return count_components, components

    @staticmethod
    # транспонирование матрицы
    def transpose_matrix(matrix):
        new_matrix = [[0] * len(matrix) for i in range(len(matrix))]
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                new_matrix[j][i] = matrix[i][j]
        return new_matrix
