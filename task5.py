import sys
from MyParser import MyParser
from InputOutput import edges_list_to_matrix, adjacency_list_to_matrix, adjacency_matrix_to_matrix, print_results
from Graph import Graph


class Algorithm_Dijkstra():
    def __init__(self, graph, begin_vertex, end_vertex):
        self.graph = graph
        self.matrix = self.graph.adjacency_matrix()
        self.begin_vertex = begin_vertex
        self.end_vertex = end_vertex

    # Алгоритм Дейкстры
    def dijkstra(self):
        n = len(self.matrix)  # Количество вершин в графе
        dist = [float('inf')] * n  # Массив для хранения длин путей
        dist[self.begin_vertex - 1] = 0  # Длина пути до начальной вершины равна 0
        p = [None] * n  # Массив для хранения предыдущих вершин на пути
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
                if self.matrix[v][u] is not None:
                    alt = dist[v] + self.matrix[v][u]  # Новая длина пути до вершины u через вершину v
                    if alt < dist[u]:  # Если новый путь короче старого, то обновляем информацию о пути
                        dist[u] = alt
                        p[u] = v
        path = []
        u = self.end_vertex - 1
        while p[u] is not None:  # Восстанавливаем путь от конечной вершины до начальной
            path.append((p[u] + 1, u + 1, self.graph.weight(p[u] + 1, u + 1)))
            u = p[u]
        path.reverse()  # Переворачиваем путь, чтобы он шел от начальной вершины до конечной
        return path, dist[self.end_vertex - 1]  # Возвращаем путь и длину кратчайшего пути


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
parser.add_argument('-d', '--end_vertex', metavar='end_vertex_number', help='Номер конечной вершины', type=int,
                    required=True)

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
task5 = Algorithm_Dijkstra(graph, int(args.begin_vertex), int(args.end_vertex))

dijkstra = task5.dijkstra()

if dijkstra[0]:
    result = f"Shortest path length between {args.begin_vertex} and {args.end_vertex} vertices: {dijkstra[1]}\nPath:\n" + str(
        dijkstra[0])
else:
    result = f"There is no path between the vertices {args.begin_vertex} and {args.end_vertex}."

if args.output:
    print_results(result, args.output)
else:
    print_results("\n" + result)
