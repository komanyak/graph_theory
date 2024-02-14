import argparse


"""Класс MyParser создается для изменения  вывода справки при введенном -h
с помощью переопредеоления метода format_help() класса ArgumentParser"""
class MyParser(argparse.ArgumentParser):
    def format_help(self):
        # Выводим информацию об авторе и группе
        author_info = '\nАвтор работы: Команяк Александр\nГруппа: М3О-210Б-21\n\n'

        # Выводим информацию о каждом аргументе
        argument_info = 'Список ключей:\n'
        for action in self._actions:
            if isinstance(action, argparse._HelpAction):
                continue
            if action.help is argparse.SUPPRESS:
                continue
            argument_info += f'  {", ".join(action.option_strings)}\t{action.help}\n'

        return author_info + argument_info
