import json
from pathlib import Path
from functools import lru_cache

LANGUAGE = "en-US"

LOCATIONS = [Path(__file__).parent / "translations"]

@lru_cache
def get_translation_data(language):
    for location in LOCATIONS:
        location_file = location / f"{language}.json"
        if location_file.is_file():
            with location_file.open() as fp:
                return json.load(fp)
    raise AttributeError("Language not found")


def format_distance(key, count):
    translation_data = get_translation_data(LANGUAGE)
    translation_value = translation_data[key]
    if type(translation_value) == str:
        result = translation_value
    elif count == 1:
        result = translation_value['one']
    else:
        result = translation_value['other'].format(count=count)
    return result


if __name__ == '__main__':
    print(format_distance("xMonths", 4))
