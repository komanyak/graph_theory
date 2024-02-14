class Output:
    __is_file_needed = False
    __path = ""

    # если нужно начать запись в файл
    def switch_to_file_output(self, path):
        self.__is_file_needed = True
        self.__path = path

    # запись в файл / консоль
    def write(self, *values, sep=' ', end='\n'):
        if self.__is_file_needed:
            # аргумент а обозначает, что файл откроется для записи,
            # или же создастся, если файла с таким именем нет
            with open(self.__path, "a", encoding="utf-8-sig") as file:
                print(*values, file=file, sep=sep, end=end)
        else:
            print(*values, sep=sep, end=end)