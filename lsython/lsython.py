import os

from lsython.extension import Lsython_database
from .file_utility import file_utility


class bcolors:
    HEADER = '\033[91m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Lsython:
    def __init__(self, argv):
        self._database = Lsython_database('extensions.json')
        self._file_utility = file_utility()
        self._parameters = self._args(argv)

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        self._parameters = value

    def _generate_legend(self) -> str:
        return "+Executables\t" + bcolors.WARNING + u"\u2588" + bcolors.ENDC + "File\t\t" + bcolors.OKGREEN + u"\u2588" \
               + bcolors.ENDC + "Directory\t" + bcolors.FAIL + u"\u2588" + bcolors.ENDC + "Symlink"

    def _generate_prefix(self,file) -> str:
        prefix = ''
        if file.executable == True:
            prefix += '+'
        return prefix

    def _generate_subfix(self, file) -> str:
        extension = file.name.rsplit('.', 1)[-1]
        extension = '.' + extension
        if self._parameters['description'] or self._parameters['suggested software'] or self._parameters[
            'modified date']:
            entry = self._database.db_extensions.search(self._database.query.extension == extension)
            if len(entry) != 1:
                return ""
        else:
            return ""

        tmp = ['\t']

        subfix = "".join(tmp)

        for iterator in self._parameters['order']:
            subfix += self._generate_column(iterator=iterator, entry=entry, file=file)
        return subfix

    def _generate_column(self, iterator, entry, file):
        subfix = "----\t"
        if iterator == 'modified date':
            tmp = file.modified
            whitespaces = 40 - len(tmp)
        else:
            tmp = entry[0][iterator]
            whitespaces = 40 - len(entry[0][iterator])
        subfix += tmp
        for i in range(round((whitespaces / 8) + 0.49)):
            subfix += '\t'

        return subfix

    def _generate_header(self) -> str:
        topics = {'description': 'File Type:', 'suggested software': 'Recommended Software:',
                  'modified date': 'Modified Date:'}
        header = "\t\t\t\t\t"

        for iterator in self._parameters['order']:
            header += topics[iterator]
            header += self._calc_tabs(string=topics[iterator], tab_count=6)
        return header

    def _file_list(self, directory):
        file_list = []
        _list = ""

        file_list = self._sort_file_list(directory=[file for file in directory if file.type == 'file'], sort=self._parameters['sort'])
        link_list = self._sort_file_list(directory=[file for file in directory if file.type == 'link'], sort=self._parameters['sort'])
        dir_list = self._sort_file_list(directory=[file for file in directory if file.type == 'dir'], sort=self._parameters['sort'])
        _list += self._generate_file_list(dir_list, bcolors.OKGREEN)
        _list += self._generate_file_list(link_list, bcolors.FAIL)
        _list += self._generate_file_list(file_list, bcolors.WARNING)
        return _list

    def _generate_file_list(self, directory, color):
        _list = ''
        for _file in directory:

            if len(_file.name) > 24 and not self._parameters['no cut']:
                extension = _file.name.rsplit('.', 1)[-1]
                ending = "[...]" + '.' + extension
                formatted_file = _file.name[:24 - len(ending)]
                formatted_file += ending
            else:
                formatted_file = _file.name
            prefix = self._generate_prefix(_file)
            subfix = self._generate_subfix(_file)
            tabs = self._calc_tabs(string=_file.name, tab_count=3)
            _list += color + prefix + '\t' + formatted_file + tabs + subfix + '\n'
        return _list

    def _calc_tabs(self, string, tab_count):
        tabs_count = round(((tab_count * 8 - len(string)) / 8) + 0.49)
        tabs = ''
        for i in range(tabs_count):
            tabs += '\t'
        return tabs

    def _sort_file_list(self, directory, sort):
        if sort == 'a':
            return sorted(directory, key=lambda s: s.name.lower())

        vis_order = []
        for index, file in enumerate(directory):
            if sort == 'e':
                extension = file.name.rsplit('.', 1)[-1]
                vis_order.append((index, extension))
            elif sort == 'm':
                vis_order.append((index, file.modified))

        vis_order.sort(key=lambda tup: tup[1])
        vis_ordered = []
        for file in vis_order:
            vis_ordered.append(directory[file[0]])
        return vis_ordered


    @property
    def output(self):
        return self._generate_output()

    def _generate_output(self) -> str:
        directory = self._file_utility.files(path=self._parameters['path'])


        output = ''
        if len([file for file in directory if file.invisible == True]) != 0:
            output += '\n' + bcolors.BOLD + bcolors.HEADER + bcolors.UNDERLINE + 'Files and directories you shouldn\'t be ' \
                                                                             'allowed to see:' + bcolors.ENDC + '\n '
            output += self._generate_header() + '\n'
            output += self._file_list([file for file in directory if file.invisible == True])

        if len([file for file in directory if file.invisible == False]) != 0:
            output += '\n' + bcolors.BOLD + bcolors.HEADER + bcolors.UNDERLINE + 'These are files you should be allowed ' \
                                                                             'to see:' + bcolors.ENDC + '\n '
            output += self._generate_header() + '\n'
            output += self._file_list([file for file in directory if file.invisible == False]) + bcolors.ENDC + '\n\n'
        output += self._generate_legend()
        return output

    @property
    def help(self):
        return self._generate_help()

    def _generate_help(self) -> str:
        help_string = 'Usage:\n'
        help_string += '\tlsython [-d|-g] [path|file] [-h|-f|-s|-m|-i|] \n'
        help_string += '\t\t-d [path]\tList directory information \n'
        help_string += '\t\t-g [file]\tList file information \n'
        help_string += '\t\t-s [a|m|e]\tSort (a)lphabetically[default] | by (m)odified date | by (e)xtension \n'
        help_string += '\t\t-c\t\tCut off long filenames to keep format. No cut if set \n'
        help_string += '\t\t-h\t\tShow help page \n'
        help_string += '\t\t-f\t\tShow additional information : file type \n'
        help_string += '\t\t-r\t\tShow additional information : recommended software \n'
        help_string += '\t\t-m\t\tShow additional information : modified date \n'

        return help_string

    def _args(self, argv):
        parameters = {'path': '.', 'description': False, 'suggested software': False, 'modified date': False,
                      'sort': 'a', 'no cut': False, 'order': []}
        try:
            if len(argv) > 1:
                for index, arg in enumerate(argv):
                    if arg == '-h':
                        raise Exception('help')
                    if arg[0] == '-' and 2 <= len(arg):
                        for char in arg:
                            if char == 'd':
                                parameters['path'] = argv[index + 1]
                            elif char == 'f':
                                if 'description' not in parameters['order']:
                                    parameters['description'] = True
                                    parameters['order'].append('description')
                                else:
                                    raise Exception(
                                        'You can only use a flag once... What purpose would it have to use a flag '
                                        'multiple times?')
                            elif char == 'r':
                                if 'suggested software' not in parameters['order']:
                                    parameters['suggested software'] = True
                                    parameters['order'].append('suggested software')
                                else:
                                    raise Exception(
                                        'You can only use a flag once... What purpose would it have to use a flag '
                                        'multiple times?')
                            elif char == 'm':
                                if 'modified date' not in parameters['order']:
                                    parameters['modified date'] = True
                                    parameters['order'].append('modified date')
                                else:
                                    raise Exception(
                                        'You can only use a flag once... What purpose would it have to use a flag '
                                        'multiple times?')
                            elif char == 's':
                                if len(argv) > index + 1 and len(argv[index + 1]) == 1:
                                    if argv[index + 1] in ['a', 'm', 'e']:
                                        parameters['sort'] = argv[index + 1]
                                    else:
                                        raise Exception(
                                            "I'm not able to sort by this parameter... Read the help page...")

                                else:
                                    raise Exception(
                                        "You need to tell me a parameter by which I should sort the list. Jeez. Read "
                                        "the help page...")

                            elif char == 'c':
                                parameters['no cut'] = True
                            else:
                                if char != '-':
                                    raise Exception("Unknown flag... Can't you just read the help page???")
                    else:

                        if argv[index - 1] not in ['-s', '-d'] and index != 0:
                            raise Exception("Parameter needs to be a flag... Just reaad the help page...")
        except Exception as error:
            if error.args[0] == 'help':
                print(self._generate_help())
            print('Error occurred! ' + error.args[0] + '\n' + self._generate_help())
            exit()
        return parameters
