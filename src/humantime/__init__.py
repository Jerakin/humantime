from datetime import datetime

from . import localise

# | Distance between dates                                            | Result              |
# |-------------------------------------------------------------------|---------------------|
# | 0 ... 30 secs                                                     | less than a minute  |
# | 30 secs ... 1 min 30 secs                                         | 1 minute            |
# | 1 min 30 secs ... 44 mins 30 secs                                 | [2..44] minutes     |
# | 44 mins ... 30 secs ... 89 mins 30 secs                           | about 1 hour        |
# | 89 mins 30 secs ... 23 hrs 59 mins 30 secs                        | about [2..24] hours |
# | 23 hrs 59 mins 30 secs ... 41 hrs 59 mins 30 secs                 | 1 day               |
# | 41 hrs 59 mins 30 secs ... 29 days 23 hrs 59 mins 30 secs         | [2..30] days        |
# | 29 days 23 hrs 59 mins 30 secs ... 44 days 23 hrs 59 mins 30 secs | about 1 month       |
# | 44 days 23 hrs 59 mins 30 secs ... 59 days 23 hrs 59 mins 30 secs | about 2 months      |
# | 59 days 23 hrs 59 mins 30 secs ... 1 yr                           | [2..12] months      |
# | 1 yr ... 1 yr 3 months                                            | about 1 year        |
# | 1 yr 3 months ... 1 yr 9 month s                                  | over 1 year         |
# | 1 yr 9 months ... 2 yrs                                           | almost 2 years      |
# | N yrs ... N yrs 3 months                                          | about N years       |
# | N yrs 3 months ... N yrs 9 months                                 | over N years        |
# | N yrs 9 months ... N+1 yrs                                        | almost N+1 years    |

__all__ = ["time_between", "time_since"]

minutes_in_amost_two_days = 2520
minutes_in_day = 60 * 24
minutes_in_month = 60 * 24 * 30


def _q_n_r(a, b):
    """Return quotient and remaining"""
    return a // b, a % b


class TimeDelta:
    def __init__(self, dt, now=None):
        now = datetime.now(dt.tzinfo) if now is None else now
        self.delta = now - dt
        self.day = abs(self.delta.days)
        self.second = abs(self.delta.seconds)

        self.year, self.day = _q_n_r(self.day, 365)
        self.month, self.day = _q_n_r(self.day, 30)
        self.hour, self.second = _q_n_r(self.second, 3600)
        self.minute, self.second = _q_n_r(self.second, 60)

    def __repr__(self):
        return f"{self.year}-{self.month}-{self.day}:{self.hour}:{self.minute}:{self.second}"

    @property
    def total_seconds(self):
        return self.delta.total_seconds()

    @property
    def total_months(self):
        return self.year * 12 + self.month


def time_since(date: datetime):
    return _time_string(TimeDelta(date))


def time_between(time_left: datetime, time_right: datetime):
    return _time_string(TimeDelta(time_left, time_right))


def get_delta(date: datetime):
    return TimeDelta(date)


def _time_string(delta: TimeDelta):
    seconds = round(delta.total_seconds)
    minutes = round(seconds / 60)

    # 0s to 30s
    if seconds <= 30:
        return localise.format_distance('lessThanXMinutes', 1)

    # 30s up to 0.75 hrs
    elif minutes < 45:
        return localise.format_distance('xMinutes', minutes)

    # 0.75 hrs up to 1.5 hrs
    elif minutes < 90:
        return localise.format_distance('aboutXHours', 1)

    # 1.5 hrs up to 24 hrs
    elif minutes < minutes_in_day:
        hours = round(minutes / 60)
        return localise.format_distance('aboutXHours', hours)

    # 1 day up to 1.75 days
    elif minutes < minutes_in_amost_two_days:
        return localise.format_distance('xDays', 1)

    # 1.75 days up to 30 days
    elif minutes < minutes_in_month:
        days = round(minutes / minutes_in_day)
        return localise.format_distance('xDays', days)

    # 1 month up to 2 months
    elif minutes < minutes_in_month * 2:
        months = round(minutes / minutes_in_month)
        return localise.format_distance('aboutXMonths', months)

    months = delta.total_months
    # 2 months up to 12 months
    if months < 12:
        nearest_month = round(minutes / minutes_in_month)
        return localise.format_distance('xMonths', nearest_month)

    # 1 year up to max Date
    else:
        months_since_start_of_year = months % 12
        years = delta.year
        # N years up to 1 years 3 months
        if months_since_start_of_year < 3:
            return localise.format_distance('aboutXYears', years)

        # N years 3 months up to N years 9 months
        elif months_since_start_of_year < 9:
            return localise.format_distance('overXYears', years)

        # N years 9 months up to N year 12 months
        else:
            return localise.format_distance('almostXYears', years + 1)
