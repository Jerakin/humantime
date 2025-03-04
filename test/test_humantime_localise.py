from datetime import datetime, timedelta

import humantime
from pathlib import Path

def time_delta(days=0, hours=0, minutes=0, seconds=0):
    _date = (datetime.now() - timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds))
    _datetime = datetime.combine(_date.date(), _date.time())
    return _datetime


def test_1_minute():
    import humantime.localise
    test_dir = Path(__file__).parent / "test"
    org_lang = humantime.localise.LANGUAGE
    humantime.localise.LOCATIONS.append(test_dir)
    humantime.localise.LANGUAGE = "test-lang"
    assert humantime.time_since(time_delta(seconds=31)) == "1m"
    assert humantime.time_since(time_delta(minutes=1, seconds=29)) == "1m"
    humantime.localise.LOCATIONS.remove(test_dir)
    humantime.localise.LANGUAGE = org_lang
