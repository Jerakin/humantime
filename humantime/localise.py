import json
from pathlib import Path

LANGUAGE = "en-US"


def format_distance(key, count):
    with (Path(__file__).parent / "translations"/f"{LANGUAGE}.json").open() as fp:
        translation_data = json.load(fp)
    if not translation_data:
        raise AttributeError("Language not found")

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
