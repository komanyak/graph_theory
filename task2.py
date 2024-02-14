import argparse

from task0 import Graph, Output, Strategy
from Task2 import DirectedGraph, UndirectedGraph


# создание парсера, который будет считывать флаги исходного файла
# и также выходного, если потребуется
def create_parser():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-e', default=False)
    argument_parser.add_argument('-m', default=False)
    argument_parser.add_argument('-l', default=False)
    argument_parser.add_argument('-o', default=False)

    return argument_parser


# проверка на то, что введен только один флаг из трех (-e, -m, -l)
def check_num_args(arguments):
    # считаем все ненулевые флаги и вычитаем флаг о, если тот был указан
    count_flags = sum([1 for flag in vars(arguments).values() if flag is not False])
    count_flags -= arguments.o is not False

    # если был указан один флаг, то находим флаг и с каким файлом он был указан
    if count_flags == 1:
        path_to_file = ''
        correct_flag = 0
        for i in vars(arguments):
            # нашли ненулевой флаг - запомнили его и имя файла
            if vars(arguments)[i] is not False:
                path_to_file = vars(arguments)[i]
                correct_flag = i
                break
        return path_to_file, correct_flag

    # иначе возвращаем ошибку
    return False, False


# проверка на нужду выходного файла
def check_file_needed(arg_o):
    if arg_o:
        # если файл нужен - меняем поток вывода из консоли на файл
        output.switch_to_file_output(arg_o)
        # очищаем файл путем открытия его для записи перед основной работой
        with open(arg_o, "w") as file:
            file.write("")


if __name__ == '__main__':
    # словарь стратегий, где по ключу (флагу) получаем функцию считывания матрицы из файла
    strategies = {
        'm': lambda path: Strategy.matrix_strategy(path),
        'e': lambda path: Strategy.edges_strategy(path),
        'l': lambda path: Strategy.list_strategy(path)
    }

    output = Output.Output()  # создаем экземпляр класса Output из модуля Output
    parser = create_parser()  # создаем парсер
    args = parser.parse_args()  # получаем все флаги этого парсера

    path, flag = check_num_args(args)

    if (path, flag) != (False, False):

        graph = Graph.Graph(strategies[flag](path))
        check_file_needed(args.o)

        if graph.is_directed():
            task2_graph = DirectedGraph.DirectedGraph(graph)
            kosaraju = task2_graph.kosaraju()
            if kosaraju[0] == 1:
                output.write("\n\nGraph is strongly connected")
            elif task2_graph.is_graph_weak_connected():
                output.write("\n\nGraph is weakly connected")
            else:
                output.write("\n\nGraph is not connected")

            res1 = kosaraju[1]
            for i in range(len(res1)):
                for j in range(len(res1[i])):
                    res1[i][j] += 1

            res2 = task2_graph.count_weak_connected_components()[1]
            for i in range(len(res2)):
                for j in range(len(res2[i])):
                    res2[i][j] += 1
            output.write(f"{kosaraju[0]} Strongly connected components:\n{res1}")
            output.write(f"{task2_graph.count_weak_connected_components()[0]} Weakly connected components:\n\
{res2}")

        # если граф не ориентирован
        else:
            # выписываем связный он или нет и компоненты связности
            task2_graph = UndirectedGraph.UndirectedGraph(graph)
            if task2_graph.is_graph_connected():
                output.write("Graph is connected")
            else:

                output.write("Graph is not connected")
            res = task2_graph.count_graph_connected_components()[1]
            for i in range(len(res)):
                for j in range(len(res[i])):
                    res[i][j] += 1
            output.write(f"{task2_graph.count_graph_connected_components()[0]} Connected components:\n\
{res}")

    else:
        print("Было передано неверное количество ключей с параметрами")
