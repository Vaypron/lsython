import sys
from lsython import generate_help, Lsython


if __name__ == '__main__':
    parameters = {'path': '.', 'description': False, 'suggested software': False, 'modified date': False,'sort' : False,  'order': []}

    if len(sys.argv) > 1:
        for index, arg in enumerate(sys.argv):
            if arg == '-h':
                print(generate_help())
                exit()
            if arg[0] == '-' and 2 <= len(arg):
                for char in arg:
                    if char == 'd':
                        parameters['path'] = sys.argv[index + 1]
                    elif char == 'f':
                        parameters['description'] = True
                        parameters['order'].append('description')
                    elif char == 'r':
                        parameters['suggested software'] = True
                        parameters['order'].append('suggested software')
                    elif char == 'm':
                        parameters['modified date'] = True
                        parameters['order'].append('modified date')
                    elif char == 's':
                        parameters['sort'] = True

    active_class = Lsython(parameters=parameters)
    print(active_class.output())
