from .gameplay import gameplay
import sys
from urllib.request import urlopen

if __name__ == '__main__':
    words_ref = sys.argv[1]
    words = ''
    try:
        with open(words_ref, 'r') as f:
            words = f.read().split()
    except:
        words = urlopen(words_ref).read().decode('utf-8').split()
    l = 0
    if len(sys.argv) == 3:
        l = int(sys.argv[2])
    else:
        l = 5
    print(gameplay(input, print, [word for word in words if len(word) == l]))
