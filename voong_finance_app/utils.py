import datetime

def date_range(start, end):
    return [start + datetime.timedelta(days=i) for i in range((end - start).days)]
