from abc import ABC


# абстрактный класс, предок орграфа и обычного графа
class GraphConnectivity(ABC):
    # конструктор, инициализирующий матрицу смежности и ее длину
    def __init__(self, graph):
        self._matrix = graph.adjacency_matrix()
        self._matrix_len = len(self._matrix)

    # обычный BFS
    def BFS(self, vertex, matrix):
        queue = [vertex]
        marked_vertices = [vertex]

        # пока очередь не пустая
        while len(queue):
            current_vertex = queue.pop(0)
            neighbours = self.adjacency_list(matrix, current_vertex)
            # берем вершину и всех ее соседей, которых еще не брали
            for neighbour in neighbours:
                if neighbour not in marked_vertices:
                    queue.append(neighbour)
                    marked_vertices.append(neighbour)

        marked_vertices.sort()
        return marked_vertices

    # связный граф или нет
    def is_connected(self, matrix):
        # если через BFS дошли не до всех вершин - несвязный
        if len(self.BFS(0, matrix)) != self._matrix_len:
            return False
        return True

    # подсчет количества и состав компонент связности
    def count_connected_components(self, matrix):
        vertices = [int(i) for i in range(len(matrix))]
        counter = 0
        components = []

        # идем по всем вершинам и запускаем от каждой BFS
        for current_vertex in vertices:
            component = self.BFS(current_vertex, matrix)

            # убираем все вершины, найденные предыдущим BFS,
            # ведь это отдельная компонента связности
            for vertex in component:
                vertices.pop(vertices.index(vertex))

            # обновляем счетчик и компоненты связности
            counter += 1
            components.append(component)

        return counter, components

    # DFS с номерами порядка выхода из каждой вершины
    def DFS(self, vertex, counter, counters, matrix):
        vertices = [vertex]
        stack = [vertex]

        # пока стэк не пустой - берем вершину
        while len(stack):
            current_vertex = stack.pop()

            # увеличиваем счетчик (t_out) и приписываем текущей вершине
            counter[0] += 1
            counters[current_vertex] = counter[0]  # массив t_out'ов для каждой вершины

            # создаем массив непосещенных соседей для вершины
            unmarked_neighbours = []
            neighbours = self.adjacency_list(matrix, current_vertex)
            for vertex in neighbours:
                if counters[vertex] == 0:
                    unmarked_neighbours.append(vertex)

            # маркируем первого соседа и добавляем его и вершину в стэк
            for vertex in unmarked_neighbours:
                stack.append(current_vertex)
                stack.append(vertex)
                vertices.append(vertex)
                break

        return vertices

    @staticmethod
    # получение списка смежных вершин к vert
    def adjacency_list(matrix, vert):
        vertices = []
        for i in range(len(matrix)):
            if matrix[vert][i] != 1000000 and vert != i:
                vertices.append(i)
        return vertices