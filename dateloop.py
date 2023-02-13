from typing import List, Tuple

def getMonthDayCount(month, year='2001'):
    # default no leap year
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31

    if month in [4, 6, 9, 11]:
        return 30
    
    if month == 2:
        if year % 100 == 0:
            # 100s year
            if year % 400 == 0:
                # e.g. 2000 is a leap year
                return 29
            else:
                # 1900 is not a leap year
                return 28
        else:
            if year % 4 == 0:
                # 2004 is a leap year
                return 29
            else:
                return 28

def getDateString(year, month, day):
    return f'{year}-{month}-{day}'

def getFirstDateString(year, month):
    return getDateString(year, month, 1)

def getLastDateString(year, month):
    last_day = getMonthDayCount(month, year)
    return getDateString(year, month, last_day)

def getThisMonthResult(year, month):
    return [getFirstDateString(year, month), getLastDateString(year, month)]

def getNextMonth(year, month):
    if month == 12:
        return (year+1, 1)
    else:
        return (year, month+1)

def getMonthRange(start_year: int, start_month: int, end_year: int, end_month: int) -> List[List[str]]:
    """Return a consistency months range for `filterBounds()` function in GEE.
    For example, when the input is (2003, 12, 2004, 3), the output will be:
    [
        ['2003-12-01', '2003-12-31'],
        ['2004-01-01', '2004-01-31'],
        ['2004-02-01', '2004-02-29'],
        ['2004-03-01', '2004-03-31']
    ]

    Parameters
    ----------
    start_year : int
        start year, e.g. 2001
    start_month : int
        start month, e.g. 10
    end_year : int
        end year, e.g. 2016
    end_month : int
        end month, e.g. 3

    Returns
    -------
    List[List[str]]
        The consistency months range list.
    """


    result = []
    this_year = start_year
    this_month = start_month
    while True:
        result.append(getThisMonthResult(this_year, this_month))

        if this_year == end_year and this_month == end_month:
            break
        else:
            this_year, this_month = getNextMonth(this_year, this_month)
    return result


