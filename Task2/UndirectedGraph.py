from Task2 import AbstractConnectivity


class UndirectedGraph(AbstractConnectivity.GraphConnectivity):
    # полностью наследуем конструктор абстрактного графа
    def __init__(self, graph):
        super().__init__(graph)

    # связный ли граф
    def is_graph_connected(self):
        # вызываем метод абстрактного класса, работающий через BFS
        return self.is_connected(self._matrix)

    # подсчет и состав компонент связности графа
    def count_graph_connected_components(self):
        # вызываем метод абстрактного класса, работающий через BFS
        return self.count_connected_components(self._matrix)