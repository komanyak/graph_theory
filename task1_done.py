import sys
from MyParser import MyParser
from InputOutput import edges_list_to_matrix, adjacency_list_to_matrix, adjacency_matrix_to_matrix, print_results
from Graph import Graph


class Graph_Characteristics():
    def __init__(self, graph):
        self.graph = graph
        self.dist_matr = self.floyd_warshall()

    def degree_vec(self):
        vec = []
        matr = self.graph.adjacency_matrix()

        # орграф
        if graph.is_directed():
            vec_plus = []
            vec_minus = []
            for i in range(len(matr)):
                count_plus = 0
                count_minus = 0
                for j in range(len(matr)):
                    if matr[i][j] is not None:
                        count_minus += 1
                    if matr[j][i] is not None:
                        count_plus += 1
                vec_plus.append(count_plus)
                vec_minus.append(count_minus)
            return [vec_plus, vec_minus]

        # простой граф
        else:
            for i in range(len(matr)):
                count = 0
                for j in range(len(matr)):
                    if matr[i][j] is not None:
                        count += 1
                vec.append(count)
            return [vec]

    def floyd_warshall(self):
        dist = self.graph.adjacency_matrix()
        for i in range(len(dist)):
            for j in range(len(dist)):
                if i == j:
                    dist[i][j] = 0
                if dist[i][j] is None:
                    dist[i][j] = float('inf')
        # Проходим по всем парам вершин i и j
        for k in range(len(dist)):
            for i in range(len(dist)):
                for j in range(len(dist)):
                    # Если путь от i к j через k короче, чем прямой путь от i к j,
                    # то обновляем дистанцию
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

        return dist

    def diameter(self):
        return max(self.eccentricity())

    def radius(self):
        return min(self.eccentricity())

    def eccentricity(self):
        return [max(x) for x in self.dist_matr]

    def center(self):
        c_list = []
        ec = self.eccentricity()
        for i in range(len(ec)):
            if ec[i] == min(ec):
                c_list.append(i + 1)
        return c_list

    def periphery(self):
        p_list = []
        ec = self.eccentricity()
        for i in range(len(ec)):
            if ec[i] == max(ec):
                p_list.append(i + 1)
        return p_list


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

# for i in matrix:
#     print(i)
# exit(1)

graph = Graph(matrix)
task1 = Graph_Characteristics(graph)

result = ""

# вектор степеней вершин
if len(task1.degree_vec()) == 1:
    result += "deg = " + str(task1.degree_vec()[0])
else:
    result += "deg+ = " + str(task1.degree_vec()[0])
    result += "\ndeg- = " + str(task1.degree_vec()[1])

# матрица расстояний
result += "\nDistancies:\n"
for i in (task1.floyd_warshall()):
    result += str(i) + "\n"

# вектор эксцентриситетов
result += "Eccentricity:\n" + str(task1.eccentricity())

# Диаметр
result += "\nD = " + str(task1.diameter())

# Радиус
result += "\nR = " + str(task1.radius())

# центральные вершины
result += "\nZ = " + str(task1.center())

# Периферийные вершины
result += "\nP = " + str(task1.periphery())

if args.output:
    print_results(result, args.output)
else:
    print_results(result)
