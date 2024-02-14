import sys
from MyParser import MyParser
from InputOutput import edges_list_to_matrix, adjacency_list_to_matrix, adjacency_matrix_to_matrix, print_results
from Graph import Graph
from collections import deque


class ShortestPath():
    def __init__(self, graph, begin_vertex):
        self.graph = graph
        self.matrix = self.graph.adjacency_matrix()
        self.begin_vertex = begin_vertex


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
        labels = [0] * n  # Массив для хранения количества меток вершин

        queue = deque([self.begin_vertex - 1])  # Очередь для обхода вершин

        while queue:
            v = queue.popleft()
            visited[v] = True
            for u in range(n):
                weight = self.matrix[v][u]
                if weight is not None:  # Проверяем смежные вершины
                    alt = dist[v] + weight  # Новая длина пути до вершины u через вершину v
                    if dist[u] is None or alt < dist[
                        u]:  # Если новый путь короче старого или у вершины u нет пути, то обновляем информацию о пути
                        dist[u] = alt
                        if not visited[u]:
                            queue.append(u)
                            labels[u] += 1
                            if labels[
                                u] >= n:  # Проверяем, если вершина имеет n или более меток, то есть отрицательный цикл
                                return None  # Возвращаем None для обозначения наличия отрицательного цикла

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



    def levit(self):
        n = len(self.matrix)  # Количество вершин в графе
        distance = [float('inf')] * n  # Массив для хранения длин путей
        distance[self.begin_vertex - 1] = 0  # Длина пути до начальной вершины равна 0
        m0 = deque([v for v in range(1, n + 1) if v != self.begin_vertex])  # необр. вершины
        m1 = deque([self.begin_vertex])  # расстояние вычисляется
        m2 = deque()  # обработанные вершины

        while m1:
            v_cur = m1.popleft()
            m2.append(v_cur)

            for v_next in self.graph.adjacency_list(v_cur):
                weight = self.matrix[v_cur - 1][v_next - 1]

                if v_next in m0:
                    distance[v_next - 1] = distance[v_cur - 1] + weight
                    m1.append(v_next)
                    m0.remove(v_next)
                elif v_next in m1:
                    new_distance = distance[v_cur - 1] + weight
                    if new_distance < distance[v_next - 1]:
                        distance[v_next - 1] = new_distance
                elif v_next in m2:
                    new_distance = distance[v_cur - 1] + weight
                    if new_distance < distance[v_next - 1]:
                        distance[v_next - 1] = new_distance
                        m1.append(v_next)
                        m2.remove(v_next)

        return distance



# создаем парсер
parser = MyParser()

# Добавляем аргументы
parser.add_argument('-e', '--edges', metavar='edges_list_file_path', help='Путь к файлу со списком ребер', type=str)
parser.add_argument('-m', '--matrix', metavar='adjacency_matrix_file_path', help='Путь к файлу с матрицей смежности',
                    type=str)
parser.add_argument('-l', '--list', metavar='adjacency_list_file_path', help='Путь к файлу со списком смежности',
                    type=str)
parser.add_argument('-o', '--output', metavar='output_file_path', help='Путь к файлу для вывода результатов', type=str)

parser.add_argument('-n', '--begin_vertex', metavar='begin_vertex_number', help='Номер начальной вершины', type=int,
                    required=True)
parser.add_argument('-d', '--dijkstra', help='Использовать алгоритм Дейкстры', action="store_true")
parser.add_argument('-b', '--bellman_ford', help='Использовать алгоритм Беллмана-Форда-Мура',
                    action="store_true")
parser.add_argument('-t', '--levit', help='Использовать алгоритм Левита', action="store_true")

# Получаем аргументы командной строки
args = parser.parse_args()

# проверка количества указанных ключей
if (sum([1 for item in [args.edges, args.matrix, args.list] if item is not None])) > 1:
    print(f"\n\t{sys.argv[0]} error:\tОдновременно может указываться только один из ключей ['-e', '-m', '-l']")
    exit(0)

if (sum([1 for item in [args.dijkstra, args.levit, args.bellman_ford] if item is not None])) == 0:
    print(f"\n\t{sys.argv[0]} error:\tУкажите алгоритм расчёта")
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
task6 = ShortestPath(graph, int(args.begin_vertex))

negative = task6.check_negative()



if negative[1]:
    result = "Graph contains a negative cycle."
else:

    if args.dijkstra:
        distance = task6.dijkstra()

    if args.bellman_ford:
        distance = task6.bellman_ford()

    if args.levit:
        distance = task6.levit()

    if negative[0]:
        result = "Graph contains edges with negative weight."
    else:
        result = "Graph does not contain edges with negative weight."
    result += "\nShortest paths lengths:\n"
    for i in range(1, len(distance) + 1):
        if i == args.begin_vertex:
            continue
        result += f"{args.begin_vertex} - {i}: {distance[i - 1]}\n"

if args.output:
    print_results(result, args.output)
else:
    print_results("\n" + result)
