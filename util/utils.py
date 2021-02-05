import numpy
from datetime import datetime


def format_number(number):
    return numpy.format_float_positional(float(number), 3, trim="-")


def timestamp():
    dt = datetime.now()
    hour, minute, second, day, month = _format_date_time(dt.hour, dt.minute, dt.second, dt.day, dt.month)
    return f"{hour}:{minute}:{second} {day}.{month}.{dt.year}"


def _format_date_time(*data):
    fdata = list()
    for d in data:
        if d <= 9:
            d = str(d)
            fdata.append(d.replace(d, f"0{d}"))  # if value is below 9, insert 0 for proper formatting.
        else:
            fdata.append(str(d))
    return tuple(fdata)
