from datetime import datetime

def get_time(now=datetime.now()):
    return now.strftime("%I:%M:%S %p")

def get_day(now=datetime.now()):
    return now.strftime("%B %d, %A")

def get_year(now=datetime.now()):
    return now.strftime("%Y")