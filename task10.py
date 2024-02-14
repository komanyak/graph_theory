import sys
from MyParser import MyParser
from InputOutput import print_results
from inp import edges_list_to_matrix, adjacency_list_to_matrix, adjacency_matrix_to_matrix

from Task10.graphh import Graph
from Task10 import Flow

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

result = ""
task10_graph = Flow.FindMaxFlow(graph)

source = task10_graph.get_source()
sink = task10_graph.get_sink()
result += f"{task10_graph.max_flow} - maximum flow from {source + 1} to {sink + 1}.\n"

for i in range(len(graph.adjacency_matrix())):
    for j in range(len(graph.adjacency_matrix())):
        if task10_graph.flow_matrix[i][j] != 1000000:
            result += f"{i + 1} {j + 1} {task10_graph.flow_matrix[i][j]}/{graph.adjacency_matrix()[i][j]}\n"

if args.output:
    print_results(result, args.output)
else:
    print_results("\n\n" + result)
