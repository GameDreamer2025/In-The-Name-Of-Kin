# Импорт модулей Panda3D для текстовой версии игры
from direct.showbase.ShowBase import ShowBase  # Базовый класс для запуска приложения
from direct.gui.OnscreenText import OnscreenText  # Класс для текста на экране
from direct.gui.DirectButton import DirectButton  # Класс для кнопок
from panda3d.core import TextNode  # Класс для выравнивания текста
from panda3d.core import loadPrcFileData  # Для настройки шрифтов

# Настраиваем кодировку UTF-8 для поддержки кириллицы
loadPrcFileData("", "text-encoding utf8")  # Устанавливаем UTF-8 для текста

class InTheNameOfKin(ShowBase):  # Определяем класс игры
    def __init__(self):  # Инициализация игры
        ShowBase.__init__(self)  # Запускаем базовый конструктор
        
        # Карма — моральный счётчик
        self.karma = 0  # Начальная карма
        
        # Главы и локации (на русском)
        self.chapters = {
            1: {"name": "Тени единства", "locations": ["Дом", "Лес", "Перевал", "Деревня"]},
            2: {"name": "Кровь чужаков", "locations": ["Мёртвые земли"]},
            3: {"name": "Пепел надежды", "locations": ["Кровавая пустошь", "Разлом теней", "Сердце рода"]}
        }
        self.locations = {
            "Дом": "Старый дом семьи у края мёртвых земель. Дым витает над могилой.",
            "Лес": "Тёмный лес с голыми деревьями. Вой волков эхом звучит в тумане.",
            "Перевал": "Узкий перевал среди обломков. Скалы шепчут о смерти.",
            "Деревня": "Разрушенная деревня. Уцелевшие дома хранят слабый свет надежды.",
            "Мёртвые земли": "Мёртвые земли — выжженная равнина, пепел витает в воздухе.",
            "Кровавая пустошь": "Кровавая пустошь — земля красна от крови, тени воют.",
            "Разлом теней": "Разлом теней — трещина в земле, ведущая к Сердцу рода.",
            "Сердце рода": "Сердце рода — пещера с пульсирующими стенами."
        }
        self.current_chapter = 1  # Начальная глава
        self.current_location = "Дом"  # Начальная локация
        self.location_index = 0  # Индекс локации
        
        # Семья с характеристиками (без моделей)
        self.family = {
            "Мать": {"hp": 80, "sanity": 100, "side": "light"},
            "Старший сын": {"hp": 100, "sanity": 100, "side": "light"},
            "Младшая дочь": {"hp": 60, "sanity": 100, "side": "light"},
            "Отец": {"hp": 120, "sanity": 100, "side": "dark"},
            "Старшая дочь": {"hp": 90, "sanity": 100, "side": "dark"},
            "Младший сын": {"hp": 70, "sanity": 100, "side": "dark"},
            "Посредник": {"hp": 90, "sanity": 100, "side": "neutral"}
        }
        
        # Интерфейс (без указания шрифта, используем встроенный с UTF-8)
        self.stats = OnscreenText(text=self.get_stats(), pos=(-1.2, 0.9), scale=0.07, fg=(1, 1, 1, 1), align=TextNode.ALeft)  # Статистика
        self.dialog = OnscreenText(text=f"Глава {self.current_chapter}: {self.chapters[self.current_chapter]['name']}\nЛокация: {self.current_location}\n{self.locations[self.current_location]}\nНачать путь?", pos=(0, 0), scale=0.07, fg=(1, 1, 1, 1))  # Диалог
        self.karma_text = OnscreenText(text=f"Карма: {self.karma}", pos=(0, -0.9), scale=0.07, fg=(1, 1, 1, 1))  # Карма
        
        # Кнопка выбора
        self.choice_button = DirectButton(text="Сделать выбор", scale=0.15, pos=(0, 0, -0.7), command=self.make_choice, text_scale=0.8, text_fg=(1, 1, 1, 1))  # Кнопка для продвижения сюжета
        
        self.stage = 0  # 0: Глава 1, 1: Глава 2, 2: Глава 3 (Мать), 3: Глава 3 (Старший сын), 4: Концовка
    
    def get_stats(self):  # Функция получения статистики семьи
        stats = ""
        for name, data in self.family.items():  # Проходим по каждому персонажу
            if data["hp"] > 0:  # Если персонаж жив
                stats += f"{name}: HP {data['hp']} Sanity {data['sanity']}\n"
        return stats
    
    def make_choice(self):  # Функция обработки выборов
        if self.current_chapter == 1:  # Глава 1
            if self.current_location == "Дом":  # Начало пути
                self.current_location = "Лес"
                self.location_index = 1
                self.dialog.setText(f"Глава 1: Тени единства\nЛокация: {self.current_location}\n{self.locations[self.current_location]}\nОленёнок в лапах волка. Спасить его?")
            elif self.current_location == "Лес":  # Спасение оленёнка
                self.karma += 10
                self.karma -= 20  # Ловушка
                self.family["Младшая дочь"]["sanity"] -= 10
                self.family["Отец"]["sanity"] += 5
                self.current_location = "Перевал"
                self.location_index = 2
                self.dialog.setText(f"Глава 1: Тени единства\nЛокация: {self.current_location}\n{self.locations[self.current_location]}\nМладенец плачет у тела матери. Спасить его?")
            elif self.current_location == "Перевал":  # Смерть Младшей дочери
                self.karma += 10
                self.family["Младшая дочь"]["hp"] = 0  # Младшая дочь умирает
                self.family["Мать"]["sanity"] -= 10
                self.family["Старший сын"]["sanity"] -= 10
                self.family["Отец"]["sanity"] += 5
                self.karma -= 10  # Ловушка
                self.current_location = "Деревня"
                self.location_index = 3
                self.dialog.setText(f"Глава 1: Тени единства\nЛокация: {self.current_location}\n{self.locations[self.current_location]}\nМладенец передан добрым людям. Продолжить?")
            elif self.current_location == "Деревня":  # Переход ко главе 2
                self.karma += 5
                self.current_chapter = 2
                self.current_location = "Мёртвые земли"
                self.location_index = 0
                self.stage = 1
                self.dialog.setText(f"Глава 2: Кровь чужаков\nЛокация: {self.current_location}\n{self.locations[self.current_location]}\nВыжившие просят оружие. Дать им?")
        
        elif self.current_chapter == 2:  # Глава 2: Смерть Младшего сына
            self.karma += 10
            self.family["Младший сын"]["hp"] = 0  # Младший сын умирает
            self.family["Мать"]["sanity"] -= 10
            self.family["Старший сын"]["sanity"] -= 10
            self.family["Отец"]["sanity"] += 5
            self.family["Старшая дочь"]["sanity"] += 5
            self.karma -= 10  # Ловушка
            self.current_chapter = 3
            self.current_location = "Кровавая пустошь"
            self.location_index = 0
            self.stage = 2
            self.dialog.setText(f"Глава 3: Пепел надежды\nЛокация: {self.current_location}\n{self.locations[self.current_location]}\nДевушка на алтаре культистов. Спасить её?")
        
        elif self.current_chapter == 3:  # Глава 3
            if self.current_location == "Кровавая пустошь" and self.stage == 2:  # Смерть Матери
                self.karma += 10
                self.family["Мать"]["hp"] = 0  # Мать умирает
                self.family["Старший сын"]["sanity"] -= 10
                self.family["Отец"]["sanity"] -= 5
                self.family["Посредник"]["sanity"] -= 5
                self.karma -= 5  # Ловушка
                self.current_location = "Разлом теней"
                self.location_index = 1
                self.stage = 3
                self.dialog.setText(f"Глава 3: Пепел надежды\nЛокация: {self.current_location}\n{self.locations[self.current_location]}\nУмирающий культист просит покоя. Дать ему?")
            elif self.current_location == "Разлом теней" and self.stage == 3:  # Смерть Старшего сына
                self.karma += 10
                self.family["Старший сын"]["hp"] = 0  # Старший сын умирает
                self.family["Отец"]["sanity"] += 5
                self.family["Посредник"]["sanity"] -= 10
                self.karma -= 5  # Ловушка
                self.current_location = "Сердце рода"
                self.location_index = 2
                self.stage = 4
                self.dialog.setText(f"Глава 3: Пепел надежды\nЛокация: {self.current_location}\n{self.locations[self.current_location]}\nОтец и Посредник у алтаря. Жертвовать Отцом?")
            elif self.current_location == "Сердце рода" and self.stage == 4:  # Концовка
                self.karma += 5
                self.family["Отец"]["hp"] = 0  # Отец жертвует собой
                self.family["Посредник"]["sanity"] -= 5
                self.dialog.setText(f"Глава 3: Пепел надежды\nЛокация: {self.current_location}\nХорошая концовка: Проклятие снято, семья воссоединилась в лучах солнца. Мёртвые земли исцеляются.")
                self.choice_button.hide()  # Скрываем кнопку выбора
        
        self.karma_text.setText(f"Карма: {self.karma}")  # Обновляем текст кармы
        self.stats.setText(self.get_stats())  # Обновляем статистику
        if all(data["hp"] <= 0 for data in self.family.values()):  # Если все мертвы
            self.dialog.setText(f"Локация: {self.current_location}\nСемья пала... Поражение!")
            self.choice_button.hide()

# Запуск игры
game = InTheNameOfKin()  # Создаём экземпляр игры
game.run()  # Запускаем игровой цикл
