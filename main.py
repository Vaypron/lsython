import sys
from lsython import Lsython


if __name__ == '__main__':
    active_class = Lsython(sys.argv)
    print(active_class.output)
