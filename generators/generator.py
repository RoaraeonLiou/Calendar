from ics import Calendar
from datetime import datetime
from lunarcalendar import Converter, Lunar
from abc import ABC, abstractmethod, ABCMeta


class GeneratorMeta(ABCMeta):
    # Meta Class
    # 负责将子类注册到子类字典
    registry = {}

    def __init__(cls, name, bases, attrs):
        super(GeneratorMeta, cls).__init__(name, bases, attrs)
        if name != "Generator":
            GeneratorMeta.registry[name] = cls


class Generator(ABC, metaclass=GeneratorMeta):
    # 抽象类，提供核心方法接口
    def __init__(self, generator_name):
        self.calendar = Calendar()
        self.event_list = list()
        self.generator_name = generator_name

    @staticmethod
    def lunar_to_solar(month, day, year):
        lunar = Lunar(year, month, day)
        solar = Converter.Lunar2Solar(lunar)
        return datetime(solar.year, solar.month, solar.day)

    @abstractmethod
    def parse(self, path):
        pass

    def generate(self, path):
        for event in self.event_list:
            self.calendar.events.add(event)
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(self.calendar)
        print(self.generator_name + " ics file generate success!")

