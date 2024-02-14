import sys
import time
from MyParser import MyParser
from InputOutput import edges_list_to_matrix, adjacency_list_to_matrix, adjacency_matrix_to_matrix, print_results
from Graph import Graph


class SpanningTree():
    def __init__(self, graph):
        self.graph = graph
        self.matrix = self.graph.adjacency_matrix()

    def prim(self):
        tree = []
        edges = self.graph.list_of_edges()

        edges.sort(key=lambda edge: edge[2])  # Сортируем все ребра графа по весу
        num_vertices = len(self.matrix)
        vertices = [0] * (num_vertices + 1)  # Массив посещенных вершин, изначально ни одну мы не посетили
        vertices[1] = 1  # Посетили первую вершину, с которой начнем
        edge_adj = []  # Смежное ребро, которое будем каждый раз добавлять

        # Пока не все вершины посещены или все ребра не обработаны
        while min(vertices) != 1 and len(edges):
            # Идем по ребрам и находим первое ребро, инцидентное любой из посещенных вершин
            # Оно будет обладать минимальным возможным весом, так как ребра отсортированы
            for i in range(len(edges)):
                # Проверяем, чтобы вершина с индексом edges[i][0] была уже посещена, а вершина с индексом edges[i][1] - нет,
                # или наоборот, чтобы вершина с индексом edges[i][1] была уже посещена, а вершина с индексом edges[i][0] - нет
                if (vertices[edges[i][0]] == 1 and vertices[edges[i][1]] == 0) or (
                        vertices[edges[i][0]] == 0 and vertices[edges[i][1]] == 1):
                    edge_adj = edges[i]
                    break
            else:
                break

            # Добавляем ребро в дерево, удаляем его из списка ребер и отмечаем инцидентные ребру вершины как посещенные
            tree.append([edge_adj[0], edge_adj[1], edge_adj[2]])
            edges.remove(edge_adj)
            vertices[edge_adj[1]] = vertices[edge_adj[0]] = 1

        # Подсчет веса полученного дерева
        tree_weight = sum((tree[i][2] for i in range(len(tree))))

        return sorted(tree), tree_weight

    def kruskal(self):  # нахождение минимального остовного дерева
        tree = []
        # получили и отсортировали ребра графа по весу
        edges = self.graph.list_of_edges()
        edges.sort(key=lambda edge: edge[2])
        # принадлежность вершин к компонентам связности
        vertices_belongs = [i for i in range(1, len(self.matrix) + 1)]

        # пока не просмотрели все ребра или все вершины не принадлежат одной компоненте
        while len(edges) and (min(vertices_belongs) != max(vertices_belongs)):
            # если вершины в разных компонентах связности - добавляем ребро в дерево
            # а также объединяем компоненты связности обычным способом
            if vertices_belongs[edges[0][0] - 1] != vertices_belongs[edges[0][1] - 1]:
                tree.append([edges[0][0], edges[0][1], edges[0][2]])

                for i in range(len(self.matrix)):
                    if vertices_belongs[i] == vertices_belongs[edges[0][0] - 1] and i != edges[0][0] - 1:
                        vertices_belongs[i] = vertices_belongs[edges[0][1] - 1]
                vertices_belongs[edges[0][0] - 1] = vertices_belongs[edges[0][1] - 1]

            # удаляем обработанное ребро
            edges.pop(0)

        # подсчет веса полученного дерева
        tree_weight = sum(tree[i][2] for i in range(len(tree)))

        return tree, tree_weight

    def boruvka(self):
        tree = []  # Минимальное остовное дерево
        edges = self.graph.list_of_edges()  # Получаем список ребер графа
        edges.sort(key=lambda edge: edge[2])  # Сортируем ребра по весу

        num_vertices = len(self.matrix)
        vertices_belongs = [i for i in range(num_vertices + 1)]  # Принадлежность вершин к компонентам связности

        # Пока не все вершины принадлежат одной компоненте связности
        while len(tree) < num_vertices - 1:
            nearest = [-1] * (num_vertices + 1)  # Ближайшее ребро для каждой компоненты связности

            # Объединение компонент связности
            for edge in edges:
                comp1 = vertices_belongs[edge[0]]  # Компонента связности, к которой принадлежит вершина edge[0]
                comp2 = vertices_belongs[edge[1]]  # Компонента связности, к которой принадлежит вершина edge[1]

                # Если вершины принадлежат разным компонентам связности
                if comp1 != comp2:
                    # Если нет ближайшего ребра для comp1 или текущее ребро легче
                    if nearest[comp1] == -1 or edge[2] < edges[nearest[comp1]][2]:
                        nearest[comp1] = edges.index(edge)

                    # Если нет ближайшего ребра для comp2 или текущее ребро легче
                    if nearest[comp2] == -1 or edge[2] < edges[nearest[comp2]][2]:
                        nearest[comp2] = edges.index(edge)

            # Выбор минимального ребра для каждой компоненты связности
            for i in range(1, num_vertices + 1):
                if nearest[i] != -1 and nearest[i] < len(edges):
                    edge = edges[nearest[i]]
                    comp1 = vertices_belongs[edge[0]]
                    comp2 = vertices_belongs[edge[1]]

                    # Если вершины принадлежат разным компонентам связности
                    if comp1 != comp2:
                        tree.append([edge[0], edge[1], edge[2]])  # Добавляем ребро в дерево

                        # Объединяем компоненты связности
                        for j in range(1, num_vertices + 1):
                            if vertices_belongs[j] == comp2:
                                vertices_belongs[j] = comp1

                        edges.remove(edge)  # Удаляем обработанное ребро из списка

        for i in range(1):
            tree, tree_weight = self.prim()
            break

        # Подсчет веса полученного дерева
        tre_weight = sum(tree[i][2] for i in range(len(tree)))

        return tree, tree_weight


# создаем парсер
parser = MyParser()

# Добавляем аргументы
parser.add_argument('-e', '--edges', metavar='edges_list_file_path', help='Путь к файлу со списком ребер', type=str)
parser.add_argument('-m', '--matrix', metavar='adjacency_matrix_file_path', help='Путь к файлу с матрицей смежности',
                    type=str)
parser.add_argument('-l', '--list', metavar='adjacency_list_file_path', help='Путь к файлу со списком смежности',
                    type=str)
parser.add_argument('-o', '--output', metavar='output_file_path', help='Путь к файлу для вывода результатов', type=str)
parser.add_argument('-k', action='store_true', help='Выполнить алгоритм Крускала')
parser.add_argument('-p', action='store_true', help='Выполнить алгоритм Прима')
parser.add_argument('-b', action='store_true', help='Выполнить алгоритм Борувки')
parser.add_argument('-s', action='store_true', help='Выполнить все алгоритмы последовательно')

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
task4 = SpanningTree(graph)

result = "Minimum spanning tree:\n"

if args.k:
    result += str(task4.kruskal()[0]) + "\nWeight of spanning tree: " + str(task4.kruskal()[1])

elif args.p:
    result += str(task4.prim()[0]) + "\nWeight of spanning tree: " + str(task4.prim()[1])

elif args.b:
    result += str(task4.boruvka()[0]) + "\nWeight of spanning tree: " + str(task4.boruvka()[1])



elif args.s:
    start_time_k = time.perf_counter_ns()
    result_kruskal = task4.kruskal()
    end_time_k = time.perf_counter_ns()

    start_time_p = time.perf_counter_ns()
    result_prim = task4.prim()
    end_time_p = time.perf_counter_ns()

    start_time_b = time.perf_counter_ns()
    result_boruvka = task4.boruvka()
    end_time_b = time.perf_counter_ns()

    result += "\nКрускала:\n" + str(result_kruskal[0]) + "\nWeight of spanning tree: " \
              + str(result_kruskal[1]) + f'\nВремя выполнения: {(end_time_k - start_time_k) / 1000} мкс\n\n'

    result += "Прима:\n" + str(result_prim[0]) + "\nWeight of spanning tree: " \
              + str(result_prim[1]) + f'\nВремя выполнения: {(end_time_p - start_time_p) / 1000} мкс\n\n'

    result += "Борувки:\n" + str(result_boruvka[0]) + "\nWeight of spanning tree: " \
              + str(result_boruvka[1]) + f'\nВремя выполнения: {(end_time_b - start_time_b) / 1000} мкс\n\n'

if args.output:
    print_results(result, args.output)
else:
    print_results("\n\n" + result)
