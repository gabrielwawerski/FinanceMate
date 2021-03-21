import numpy
from datetime import datetime


def fnum(number: int) -> str:
    """Converts argument to float and formats it's decimal precision to 2

    :return: float with dec. precision = 2
    """
    return numpy.format_float_positional(float(number), 2, trim="-")


def timestamp() -> str:
    from datetime import datetime
    dt = datetime.now()
    hour, minute, second, day, month = _format_date_time(dt.hour, dt.minute, dt.second, dt.day, dt.month)
    return f"{hour}:{minute}:{second} {day}.{month}.{dt.year}"


def _format_date_time(*data: int) -> tuple:
    fdata = list()
    for d in data:
        if d <= 9:
            d = str(d)
            fdata.append(d.replace(d, f"0{d}"))  # if value is below 9, insert 0 for proper formatting.
        else:
            fdata.append(str(d))
    return tuple(fdata)


def get_month_name(month: int = datetime.now().month) -> str:
    """Returns a string representation of the current month. Assumes 1 as the first month of the year.

    :param month: 1 - 12
    :return: string representation of the month
    """

    if month == 1:
        return "January"
    elif month == 2:
        return "February"
    elif month == 3:
        return "March"
    elif month == 4:
        return "April"
    elif month == 5:
        return "May"
    elif month == 6:
        return "June"
    elif month == 7:
        return "July"
    elif month == 8:
        return "August"
    elif month == 9:
        return "September"
    elif month == 10:
        return "October"
    elif month == 11:
        return "November"
    elif month == 12:
        return "December"
