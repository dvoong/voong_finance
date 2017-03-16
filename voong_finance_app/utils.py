import datetime

def date_range(start, end):
    return [start + datetime.timedelta(days=i) for i in range((end - start).days)]

def convert_date_string(date_string):
    return datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
