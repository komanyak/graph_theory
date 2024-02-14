import sys
import copy
import math
from MyParser import MyParser
from InputOutput import edges_list_to_matrix, adjacency_list_to_matrix, adjacency_matrix_to_matrix, print_results
from Graph import Graph


class AlgJohnson:
    # принимается на вход модифицированный класс графа, где добавляются методы
    # добавления и удаления вершины в графе
    def __init__(self, graph):
        self.graph = graph
        self.matrix = self.graph.adjacency_matrix()
        self.begin_vertex = len(self.matrix)

    def check_negative(self):
        edges = self.graph.list_of_edges()
        negative_weight = False
        negative_cycle = False

        # Проверка на наличие отрицательных весов ребер
        for u, v, weight in edges:
            if weight is not None and weight < 0:
                negative_weight = True
                break

        if self.bellman_ford() == -1:
            negative_cycle = True

        return negative_weight, negative_cycle

    def dijkstra(self):
        n = len(self.matrix)  # Количество вершин в графе
        dist = [float('inf')] * n  # Массив для хранения длин путей
        dist[self.begin_vertex - 1] = 0  # Длина пути до начальной вершины равна 0
        visited = [False] * n  # Массив для хранения информации о пройденных вершинах
        for i in range(n):
            v = -1
            for j in range(n):
                # Находим непройденную вершину с минимальным значением dist
                if not visited[j] and (v == -1 or dist[j] < dist[v]):
                    v = j
            if dist[v] == float('inf'):  # Если путь до вершины v не найден, алгоритм заканчивает работу
                break
            visited[v] = True  # Помечаем вершину v как пройденную
            for u in range(n):
                weight = self.matrix[v][u]
                if weight is not None:  # Проверяем смежные вершины
                    alt = dist[v] + weight  # Новая длина пути до вершины u через вершину v
                    if dist[u] is None or alt < dist[
                        u]:  # Если новый путь короче старого или у вершины u нет пути, то обновляем информацию о пути
                        dist[u] = alt

        return dist

    def bellman_ford(self):

        n = len(self.matrix)  # Количество вершин в графе
        dist = [None] * n  # Массив для хранения длин путей
        dist[self.begin_vertex - 1] = 0  # Длина пути до начальной вершины равна 0
        edges = self.graph.list_of_edges()

        # Обновление расстояний до всех вершин
        for _ in range(len(self.matrix) - 1):
            for u, v, weight in edges:
                if dist[u - 1] is not None and weight is not None and (
                        dist[v - 1] is None or dist[v - 1] > dist[u - 1] + weight):
                    dist[v - 1] = dist[u - 1] + weight

        # Проверка на наличие отрицательных циклов
        for _ in range(len(self.matrix) - 1):
            for u, v, weight in edges:
                if dist[u - 1] is not None and weight is not None and (
                        dist[v - 1] is None or dist[v - 1] > dist[u - 1] + weight):
                    return -1

        return dist

    # алгортим Джонсона
    def johnson(self):
        n = len(self.matrix)  # Количество вершин в графе

        matr = self.matrix

        # Добавление вершины q и соединение с остальными вершинами с нулевыми весами
        modified_matrix = copy.deepcopy(self.matrix)
        modified_matrix.append([None] * (n + 1))
        for i in range(n):
            modified_matrix[i].append(0)

        self.graph = Graph(modified_matrix)
        self.matrix = modified_matrix
        self.begin_vertex = len(self.matrix)

        # Запуск алгоритма Беллмана-Форда для расчета h(v)
        h = self.bellman_ford()

        self.graph = Graph(matr)
        self.matrix = matr
        self.begin_vertex = len(self.matrix)

        if h == -1:
            return -1  # Присутствует отрицательный цикл, завершаем работу

        # Пересчет весов ребер оригинального графа
        for u in range(n):
            for v in range(n):
                weight = self.matrix[u][v]
                if weight is not None and h[u] is not None and h[v] is not None:
                    self.matrix[u][v] = weight + h[u] - h[v]

        # Запуск алгоритма Дейкстры для каждой вершины
        shortest_paths = []
        for i in range(1, n + 1):
            self.begin_vertex = i
            shortest_path = self.dijkstra()
            shortest_paths.append(shortest_path)

        # Пересчет кратчайших путей обратно
        for u in range(n):
            for v in range(n):
                if shortest_paths[u][v] is not math.inf and h[u] is not None and h[v] is not None:
                    shortest_paths[u][v] = shortest_paths[u][v] + h[v] - h[u]

        return shortest_paths
        # # добавляется новая вершина q и ребра нулевого веса от этой вершины ко всем остальным
        # for i in range(len(self.matrix)):
        #     self.matrix[i].append(1000000)
        # self.matrix.append([None] * (len(self.matrix) + 1))
        # self.graph = Graph(self.matrix)
        #
        # # используется алгоритм Беллмана-Форда для расчета растояний от q до всех остальных вершин
        # sp = ShortestPath(self.graph, len(self.matrix) - 1)
        # h = sp.bellman_ford()
        #
        # # вершина удаляется, далее работа будет с изначальным графом и его матрицей смежности
        # for i in range(len(self.matrix) - 1):
        #     self.matrix[i].pop(len(self.matrix) - 1)
        # self.matrix.pop(len(self.matrix) - 1)
        # self.graph = Graph(self.matrix)
        #
        # # если Б.Ф. нашел цикл отрицательного веса, то работа алгоритма завершается
        # if h == -1:
        #     return -1, True
        #
        # # флаг для проверки на отрицательное ребро
        # negative_edge = False
        # for dist in h:
        #     if dist < 0:
        #         negative_edge = True
        #
        # # делаем копию матрицы, чтобы затем после пересчитываний весов все вернуть как было
        # matrix_copy = self.graph.adjacency_matrix()
        #
        # # пересчитываются веса ребер
        # for i in range(len(self.matrix)):
        #     for j in range(len(self.matrix)):
        #         self.matrix[i][j] = self.matrix[i][j] + h[i] - h[j] \
        #             if self.matrix[i][j] is not None else None
        #
        # # из каждой вершины запускаем алгоритм Дейкстры
        # d = [0] * len(self.matrix)
        # for i in range(len(self.matrix)):
        #     d[i] = ShortestPath.dijkstra(self.graph, i)
        #
        # # для найденных расстояний вычисляем исходное значение
        # for i in range(len(self.__graph._matrix)):
        #     for j in range(len(self.__graph._matrix)):
        #         d[i][j] = d[i][j] + h[j] - h[i] if d[i][j] != 1000000 else 1000000
        #
        # # возвращаем матрицу в исходное состояние
        # self.__graph._matrix = matrix_copy
        #
        # return d, negative_edge


# создаем парсер
parser = MyParser()

# Добавляем аргументы
parser.add_argument('-e', '--edges', metavar='edges_list_file_path', help='Путь к файлу со списком ребер', type=str)
parser.add_argument('-m', '--matrix', metavar='adjacency_matrix_file_path', help='Путь к файлу с матрицей смежности',
                    type=str)
parser.add_argument('-l', '--list', metavar='adjacency_list_file_path', help='Путь к файлу со списком смежности',
                    type=str)
parser.add_argument('-o', '--output', metavar='output_file_path', help='Путь к файлу для вывода результатов', type=str)

# Получаем аргументы командной строки
args = parser.parse_args()

# проверка количества указанных ключей
if (sum([1 for item in [args.edges, args.matrix, args.list] if item is not None])) > 1:
    print(f"\n\t{sys.argv[0]} error:\tОдновременно может указываться только один из ключей ['-e', '-m', '-l']")
    exit(0)

matrix = []
# граф задан списком ребер
if (args.edges):
    matrix = edges_list_to_matrix(args.edges)

# граф задан матрицей смежности
if (args.matrix):
    matrix = adjacency_matrix_to_matrix(args.matrix)

# граф задан списком смежности
if (args.list):
    matrix = adjacency_list_to_matrix(args.list)

graph = Graph(matrix)
task7 = AlgJohnson(graph)

lengths = task7.johnson()
result = ""

negative = task7.check_negative()

if negative[1]:
    result = "Graph contains a negative cycle."
else:
    if negative[0]:

        result = "Graph contains edges with negative weight."


    else:
        result = "Graph does not contain edges with negative weight."
    result += "\nShortest paths lengths:\n"
    for i in range(len(lengths)):
        for j in range(len(lengths)):
            if i != j and lengths[i][j] != float("inf"):
                result += f"{i + 1} - {j + 1}: {lengths[i][j]}\n"

if args.output:
    print_results(result, args.output)
else:
    print_results("\n" + result)
