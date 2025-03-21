import json, os

# Вспомогательная функция, выводящая значение с отступами для визуального отображения вложенности.
def print_with_indent(value, indent=0):
    indention = "\t" * indent
    print(indention + str(value))

# Класс Entry представляет запись (например, категорию или элемент списка)
class Entry:
    # Конструктор записи
    # title – название записи
    # entries – список вложенных записей (по умолчанию пустой)
    # parent – родительская запись (по умолчанию None)
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            self.entries = list()
        self.title = title
        self.parent = parent

    # Строковое представление объекта Entry, возвращает его название
    def __str__(self):
        return self.title

    # Добавляет новую вложенную запись и устанавливает текущий объект как её родителя
    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    # Рекурсивно выводит текущую запись и все вложенные записи с отступами
    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    # Преобразует запись в формат словаря, подходящий для JSON-сериализации
    def json(self):
        res = {
            'title': self.title,
            'entries': [x.json() for x in self.entries]
        }
        return res

    # Создаёт объект Entry из JSON-словаря
    @classmethod
    def from_json(cls, value):
        new_entry = Entry(value['title'])
        for item in value.get('entries', []):
            new_entry.add_entry(cls.from_json(item))
        return new_entry

    # Сохраняет запись в JSON-файл по указанному пути
    def save(self, path):
        name = self.json()['title']
        with open(f'{path}/{name}.json', 'w') as f:
            json.dump(self.json(), f)

    # Загружает запись из JSON-файла
    @classmethod
    def load(cls, filename):
        with open(f'{filename}', 'r') as f:
            new_dict = json.load(f)
        return cls.from_json(new_dict)

# Класс EntryManager отвечает за управление коллекцией записей
class EntryManager:
    # Конструктор менеджера записей с указанием пути для хранения данных
    def __init__(self, data_path):
        self.data_path = data_path
        self.entries = list()

    # Сохраняет все записи менеджера в указанную директорию
    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    # Загружает записи из JSON-файлов из указанной директории
    def load(self):
        for entry in os.listdir(self.data_path):
            path_to_file = os.path.join(self.data_path, entry)
            if entry.endswith(".json"):
                some_entry = Entry.load(path_to_file)
                self.entries.append(some_entry)

    # Добавляет новую запись в менеджер по названию
    def add_entry(self, title: str):
        new_entry = Entry(title)
        self.entries.append(new_entry)

# Пример структуры данных (например, список покупок)
grocery_list = {
    "title": "Продукты",
    "entries": [
        {
            "title": "Молочные",
            "entries": [
                {"title": "Йогурт", "entries": []},
                {"title": "Сыр", "entries": []}
            ]
        }
    ]
}

# Пример использования кода
if __name__ == '__main__':
    # Создание записи из JSON-структуры
    new_entry = Entry.from_json(grocery_list)

    # Создание новой категории и добавление элементов
    category = Entry('Еда')
    category.add_entry(Entry('Морковь'))
    category.add_entry(Entry('Капуста'))

    # Печать структуры записей
    category.print_entries()

    # Получение словаря для сохранения в JSON
    to_save = category.json()