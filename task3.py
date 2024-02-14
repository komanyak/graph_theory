import sys
from MyParser import MyParser
from InputOutput import edges_list_to_matrix, adjacency_list_to_matrix, adjacency_matrix_to_matrix, print_results
from Graph import Graph


class Bridges_And_Cutpoints():
    def __init__(self, graph):
        self.graph = graph
        self.matrix = self.graph.adjacency_matrix()
        self.tin = [0] * len(self.matrix)
        self.tup = [0] * len(self.matrix)
        self.timer = 0
        self.bridges = []
        self.cutpoints = []
        # для орграфа создаем матрицу соотнесенного графа
        if self.graph.is_directed():
            # Инвертируем направление ребер исходного графа
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix)):
                    if self.graph.adjacency_matrix()[i][j] is not None:
                        self.matrix[j][i] = self.graph.adjacency_matrix()[i][j]
            self.graph = Graph(self.matrix)

    def find_bridges_and_cutpoints(self):
        marked = [False] * len(self.matrix)
        self.DFS(marked, 1, -1)
        return sorted(self.bridges), sorted(self.cutpoints)

    def DFS(self, marked, v, p):
        marked[v - 1] = True
        self.tin[v - 1] = self.timer
        self.timer += 1
        self.tup[v - 1] = self.tin[v - 1]
        children = 0
        is_cutpoint = False

        for to in self.graph.adjacency_list(v):
            if to == p:
                continue

            if marked[to - 1]: # обратное ребро
                self.tup[v - 1] = min(self.tup[v - 1], self.tin[to - 1])
            else:
                self.DFS(marked, to, v)

                self.tup[v - 1] = min(self.tup[v - 1], self.tup[to - 1])      # возврат в вершину
                children += 1

                if self.tup[to - 1] > self.tin[v - 1]:
                    self.bridges.append((min(v, to), max(v, to)))

                if self.tup[to - 1] >= self.tin[v - 1] and p != -1:
                    is_cutpoint = True

        if children > 1 and p == -1:
            is_cutpoint = True
        if is_cutpoint:
            self.cutpoints.append(v)


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
task3 = Bridges_And_Cutpoints(graph)

bridges_and_cutpoints = task3.find_bridges_and_cutpoints()
result = "Bridges:\n" + str(bridges_and_cutpoints[0]) + "\nCut vertices:\n" + str(bridges_and_cutpoints[1])

if args.output:
    print_results(result, args.output)
else:
    print_results("\n\n" + result)
