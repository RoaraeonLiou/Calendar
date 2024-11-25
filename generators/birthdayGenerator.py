import json
from .generator import Generator
from ics import Event
from datetime import datetime, timedelta


class BirthdayGenerator(Generator):
    def __init__(self):
        super().__init__("birthday")

    def parse(self, path):
        # 从配置文件解析生日信息
        today = datetime.now()
        next_year = today.year + 1

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for entry in data["birthdays"]:
            name = entry["name"]
            reminder_days = entry.get("reminder_days", 7)
            birthday_type = entry["type"]
            birth_year, month, day = map(int, entry["date"].split('-'))

            for year in [today.year, next_year]:
                try:
                    if birthday_type == "solar":
                        birthday_date = datetime(year, month, day)
                    elif birthday_type == "lunar":
                        birthday_date = Generator.lunar_to_solar(month, day, year)
                    else:
                        continue

                    if today <= birthday_date <= datetime(next_year, today.month, today.day):
                        event = Event()
                        if birth_year <= 0 or birth_year > today.year:
                            event.name = f"{name}的生日"
                        else:
                            event.name = f"{name}的{birthday_date.year - birth_year}岁生日"
                        if birthday_type == "solar":
                            event.name = event.name + "(阳历)"
                        else :
                            event.name = event.name + "(阴历)"
                        event.begin = birthday_date
                        event.end = birthday_date
                        event.make_all_day()

                        reminder_date = birthday_date - timedelta(days=reminder_days)
                        event.alarms.append(reminder_date)
                        self.event_list.append(event)
                except ValueError:
                    continue

    def generate(self, path):
        super(BirthdayGenerator, self).generate(path)
