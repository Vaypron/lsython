import sys
from lsython import generate_help, Lsython


if __name__ == '__main__':
    parameters = {'path': '.', 'description': False, 'suggested software': False, 'modified date': False,'sort' : 'a',  'order': []}
    try:
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
                            if 'description' not in parameters['order']:
                                parameters['description'] = True
                                parameters['order'].append('description')
                            else:
                                raise Exception('You can only use a flag once... What purpose would it have to use a flag multiple times?')
                        elif char == 'r':
                            if 'suggested software' not in parameters['order']:
                                parameters['suggested software'] = True
                                parameters['order'].append('suggested software')
                            else:
                                raise Exception('You can only use a flag once... What purpose would it have to use a flag multiple times?')
                        elif char == 'm':
                            if 'modified date' not in parameters['order']:
                                parameters['modified date'] = True
                                parameters['order'].append('modified date')
                            else:
                                raise Exception('You can only use a flag once... What purpose would it have to use a flag multiple times?')
                        elif char == 's':
                            if len(sys.argv) > index+1 and len(sys.argv[index+1]) == 1:
                                if sys.argv[index+1] in ['a','m','e']:
                                    parameters['sort'] = sys.argv[index+1]
                                else:
                                    raise Exception("I'm not able to sort by this parameter... Read the help page...")

                            else:
                                raise Exception("You need to tell me a parameter by which I should sort the list. Jeez. Read the help page...")
                        else:
                            if char != '-':
                                raise Exception("Unknown flag... Can't you just read the help page???")
                else:

                    if sys.argv[index-1] not in ['-s', '-d'] and index != 0:
                        raise Exception("Parameter needs to be a flag... Just reaad the help page...")
    except Exception as error:
        print('Error occurred! ' + error.args[0] + '\n')
        print(generate_help())
        exit()

    active_class = Lsython(parameters=parameters)
    print(active_class.output())
