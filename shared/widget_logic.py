# ©2025 Alex Hooper Projects

from calendar import day_abbr
from datetime import date
from dateutil.relativedelta import relativedelta
from data_processing import CountdownWidgetData


class CountdownWidget:
    def __init__(self):
        self.identifier = ""
        self.label = ""
        self.time_until = ""

    def update(self, end_date):
        today = date.today()
        if abs((end_date - today).days) < 0:
            end_date = end_date + relativedelta(years=1)
        self.time_until = abs((end_date - today).days)
        return self.time_until

    def fetch(self):
        return [self.label, self.time_until]

    def create_new(self, end_date="12/31", label="Last day of Year"):
        end_date_formatted = date.fromisoformat(end_date)
        self.update(end_date_formatted)
        self.identifier = CountdownWidgetData().new(label, end_date)
        return self.fetch()

    def remove(self):
        CountdownWidgetData().remove(self.identifier)


class WeatherWidget:
    def add_item(self):
        print()

    def remove_item(self):
        print()

    def update(self):
        print()


class DateWidget:
    def format_date(self):
        print()

    def update_date(self):
        print()
