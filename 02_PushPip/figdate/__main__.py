import sys
from .date import date

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(date())
    elif len(sys.argv) == 2:
        print(date(sys.argv[1]))
    else:
        print(date(sys.argv[1], sys.argv[2]))
