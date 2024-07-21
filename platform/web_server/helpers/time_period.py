from typing import Optional

from django.utils.dateparse import parse_datetime
from django.utils.timezone import datetime


DAWN_OF_TIME_STR = '1974-09-12T00:00:00Z'
DAWN_OF_TIME_DATETIME = parse_datetime(DAWN_OF_TIME_STR)


class TimePeriod:
    def __init__(
            self,
            start: Optional[datetime]=None,
            end: Optional[datetime]=None,
    ):
        self.start = start
        self.end = end

    def before(self, date_time: datetime) -> bool:
        return (date_time < self.start) if self.start else False

    def after(self, date_time: datetime) -> bool:
        return (date_time > self.end) if self.end else False

    def within(self, date_time:datetime) -> bool:
        return not self.before(date_time) and not self.after(date_time)

    def __str__(self):
        if not self.start and not self.end:
            return "period covering all of time"
        if not self.start:
            return f"period from the dawn of time until {self.end}"
        if not self.end:
            return f"period starting {self.start} until the end of time"
        return f"period starting {self.start} and ending {self.end}"
