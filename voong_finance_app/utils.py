import datetime

def date_range(start, end):
    return [start + datetime.timedelta(days=i) for i in range((end - start).days)]

def convert_date_string(date_string):
    return datetime.datetime.strptime(date_string, '%Y-%m-%d').date()

def get_month_dates(date):
    start = datetime.date(date.year, date.month, 1)
    end = start + datetime.timedelta(days=32)
    end = end - datetime.timedelta(days=end.day - 1)
    return date_range(start, end)
