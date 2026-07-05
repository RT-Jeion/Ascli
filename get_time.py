from datetime import datetime


def get_time(now=datetime.now()):
    return str(now.strftime("%I:%M:%S %p"))


def get_day(now=datetime.now()):
    return str(now.strftime("%B %d, %A"))


def get_year(now=datetime.now()):
    return str(now.strftime("%Y"))


if __name__ == "__main__":
    print(get_time())
    print(get_day())
    print(get_year())
