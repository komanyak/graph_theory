import copy


class FindMaxFlow:
    def __init__(self, graph):
        self.__graph = graph
        self.__matrix = graph.adjacency_matrix()
        self.__matrix_len = len(self.__matrix)
        self.__source = self.__find_source()
        self.__sink = self.__find_sink()
        self.flow_matrix, self.max_flow = self.__edmonds_karp()

    # геттер для источника
    def get_source(self):
        return self.__source

    # геттер для стока
    def get_sink(self):
        return self.__sink

    # алгоритм Эдмондса-Карпа
    def __edmonds_karp(self):
        result = copy.deepcopy(self.__matrix)
        ost = copy.deepcopy(self.__matrix)

        while True:
            # пока путь от истока до стока существует
            way = self.__BFS(ost)
            if way == -1:
                break

            # получаем пропускную способность дуги
            way.sort(key=lambda edge: edge[2])
            min_edge = way[0][2]

            # обновляем матрицу пропускных способностей
            for edge in way:
                ost[edge[0]][edge[1]] -= min_edge
                ost[edge[1]][edge[0]] += min_edge

        # результирующую матрицу получаем как разность изначальной матрицы и остаточных пропускных способностей
        # в изначальной матрице записаны пропускные способности ребер, а в ost - остаточные пропускные способности
        for i in range(self.__matrix_len):
            for j in range(self.__matrix_len):
                if result[i][j] != 1000000:
                    result[i][j] -= ost[i][j]

        # значение максимального потока это входной поток на сток
        max_flow = 0
        for i in range(self.__matrix_len):
            # print(result[i])
            if result[i][self.__sink] != 1000000:
                max_flow += result[i][self.__sink]

        return result, max_flow

    # BFS для нахождения дополняющей цепи
    def __BFS(self, matrix):
        queue = [self.__source]  # очередь, в которой изначально только источник
        is_sink = False  # флаг остановки, если дошли до стока

        visited = [False] * self.__matrix_len  # массив посещенных вершин
        visited[self.__source] = True

        parents = [-1] * self.__matrix_len  # массив родителей для каждой вершины
        parents[self.__source] = self.__source

        while len(queue):
            # берем вершину из очереди и смотрим ее соседей
            current_vertex = queue.pop(0)
            neighbours = self.__graph.adjacency_list(self.__matrix, current_vertex)

            for neighbour in neighbours:
                # если сосед еще не посещен и еще можно пропустить поток
                if matrix[current_vertex][neighbour] != 0 and not visited[neighbour]:
                    # помечаем соседа, его родителем будет текущая вершина, а самого соседа заносим в конец очереди
                    visited[neighbour] = True
                    parents[neighbour] = current_vertex
                    queue.append(neighbour)
                    # если сосед является стоком - выходим, цепь найдена
                    if neighbour == self.__sink:
                        is_sink = True
                        break
            if is_sink:
                break

        # критерий остановки - если все еще не дошли до стока
        if not is_sink:
            return -1

        # возвращаем дополняющую цепь
        return self.__get_route_for_BFS(parents, matrix)

        # получение дополнящей цепи минимального количества ребер

    def __get_route_for_BFS(self, parents, matrix):
        route = []
        vertex = self.__sink
        # идем по родителям от стока, пока не дойдем до источника
        while vertex != self.__source:
            route.append([parents[vertex], vertex, matrix[parents[vertex]][vertex]])
            vertex = parents[vertex]

        # реверсируем массив, тк родителей писали в обратном порядке
        route.reverse()

        return route

    # нахождение источника в сети (вершина, в которую ничего не входит)
    def __find_source(self):
        for i in range(self.__matrix_len):
            is_source = True
            for j in range(self.__matrix_len):
                if self.__matrix[j][i] != 1000000:
                    is_source = False
                    continue
            if is_source:
                return i
        return -1

    # нахождение стока в сети (вершина, из которой ничего не выходит)
    def __find_sink(self):
        for i in range(self.__matrix_len):
            is_sink = True
            for j in range(self.__matrix_len):
                if self.__matrix[i][j] != 1000000:
                    is_sink = False
                    continue
            if is_sink:
                return i
        return -1