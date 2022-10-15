from datetime import datetime, timedelta

import humantime


def time_delta(days=0, hours=0, minutes=0, seconds=0):
    _date = (datetime.now() - timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds))
    _datetime = datetime.combine(_date.date(), _date.time())
    return _datetime


def test_time_between():
    assert humantime.time_between(datetime(year=2014, month=7, day=2), datetime(year=2015, month=1, day=1)) == "6 months"
    assert humantime.time_between(datetime(year=2015, month=1, day=1), datetime(year=2015, month=1, day=1, second=15)) == "less than a minute"


def test_less_than_a_minute():
    # | 0 ... 30 secs                                                     | less than a minute  |
    assert humantime.time_since(time_delta(seconds=1)) == "less than a minute"
    assert humantime.time_since(time_delta(seconds=30)) == "less than a minute"


def test_1_minute():
    # | 30 secs ... 1 min 30 secs                                         | 1 minute            |
    assert humantime.time_since(time_delta(seconds=31)) == "1 minute"
    assert humantime.time_since(time_delta(minutes=1, seconds=29)) == "1 minute"


def test_multiple_minutes():
    # | 1 min 30 secs ... 44 mins 30 secs                                 | [2..44] minutes     |
    assert humantime.time_since(time_delta(minutes=1, seconds=30)) == "2 minutes"
    assert humantime.time_since(time_delta(minutes=44, seconds=29)) == "44 minutes"


def test_1_hour():
    # | 44 mins ... 30 secs ... 89 mins 30 secs                           | about 1 hour        |
    assert humantime.time_since(time_delta(minutes=44, seconds=31)) == "about 1 hour"
    assert humantime.time_since(time_delta(minutes=89, seconds=29)) == "about 1 hour"


def test_multiple_hours():
    # | 89 mins 30 secs ... 23 hrs 59 mins 30 secs                        | about [2..24] hours |
    assert humantime.time_since(time_delta(minutes=89, seconds=30)) == "about 2 hours"
    assert humantime.time_since(time_delta(hours=23, minutes=59, seconds=29)) == "about 24 hours"


def test_1_day():
    # | 23 hrs 59 mins 30 secs ... 41 hrs 59 mins 30 secs                 | 1 day               |
    assert humantime.time_since(time_delta(hours=23, minutes=59, seconds=30)) == "1 day"
    assert humantime.time_since(time_delta(hours=41, minutes=59, seconds=29)) == "1 day"


def test_multiple_days():
    # | 41 hrs 59 mins 30 secs ... 29 days 23 hrs 59 mins 30 secs         | [2..30] days        |
    assert humantime.time_since(time_delta(hours=41, minutes=59, seconds=30)) == "2 days"
    assert humantime.time_since(time_delta(days=29, hours=23, minutes=59, seconds=29)) == "30 days"


def test_about_1_month():
    # | 29 days 23 hrs 59 mins 30 secs ... 44 days 23 hrs 59 mins 30 secs | about 1 month       |
    assert humantime.time_since(time_delta(days=29, hours=23, minutes=59, seconds=30)) == "about 1 month"
    assert humantime.time_since(time_delta(days=44, hours=23, minutes=59, seconds=29)) == "about 1 month"


def test_about_2_month():
    # | 44 days 23 hrs 59 mins 30 secs ... 59 days 23 hrs 59 mins 30 secs | about 2 months      |
    assert humantime.time_since(time_delta(days=44, hours=23, minutes=59, seconds=30)) == "about 2 months"
    assert humantime.time_since(time_delta(days=59, hours=23, minutes=59, seconds=29)) == "about 2 months"


def test_multiple_months():
    # | 59 days 23 hrs 59 mins 30 secs ... 1 yr                           | [2..12] months      |
    assert humantime.time_since(time_delta(days=59, hours=23, minutes=59, seconds=30)) == "2 months"
    assert humantime.time_since(time_delta(days=365-6)) == "12 months"


def test_about_a_year():
    # | 1 yr ... 1 yr 3 months                                            | about 1 year        |
    assert humantime.time_since(time_delta(days=365)) == "about 1 year"
    assert humantime.time_since(time_delta(days=365 + 30 * 3 - 1)) == "about 1 year"


def test_over_a_year():
    # | 1 yr 3 months ... 1 yr 9 month s                                  | over 1 year         |
    assert humantime.time_since(time_delta(days=365 + 30 * 3)) == "over 1 year"
    assert humantime.time_since(time_delta(days=365 + 30 * 9-1)) == "over 1 year"


def test_almost_2_years():
    # | 1 yr 9 months ... 2 yrs                                           | almost 2 years      |
    assert humantime.time_since(time_delta(days=365 + 30 * 9)) == "almost 2 years"
    assert humantime.time_since(time_delta(days=365 + 30 * 11 + 29)) == "almost 2 years"


def test_about_n_years():
    # | N yrs ... N yrs 3 months                                          | about N years       |
    n = 5
    assert humantime.time_since(time_delta(days=365 * n)) == f"about {n} years"
    assert humantime.time_since(time_delta(days=365 * n + 3 * 30-1)) == f"about {n} years"


def test_over_n_years():
    # | N yrs 3 months ... N yrs 9 months                                 | over N years        |
    n = 5
    assert humantime.time_since(time_delta(days=366 * n + 3 * 30)) == f"over {n} years"
    assert humantime.time_since(time_delta(days=365 * n + 9 * 30 - 1)) == f"over {n} years"


def test_almost_n_years():
    # | N yrs 9 months ... N+1 yrs                                        | almost N+1 years    |
    n = 5
    assert humantime.time_since(time_delta(days=365 * n + 9 * 30)) == f"almost {n+1} years"
