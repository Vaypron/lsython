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
        return "+Executables  " + bcolors.WARNING + u"\u2588" + bcolors.ENDC + "File  " + bcolors.OKGREEN + u"\u2588" + bcolors.ENDC + "Directory"

    def _generate_prefix(self, path, file) -> str:
        prefix = ''
        if self._file_utility.is_exe(os.path.join(path, file)):
            prefix += '+'
        return prefix

    def _generate_subfix(self, file) -> str:
        extension = file.rsplit('.', 1)[-1]
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
        print("Hallo")
        return subfix

    def _generate_column(self, iterator, entry, file):
        subfix = "----\t"
        if iterator == 'modified date':
            tmp = self._file_utility.get_modified_date(path=self._parameters['path'], filename=file)
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

    def _file_list(self, visibility, directory):
        _file_list = []
        _list = ""

        if self._parameters['sort'] in ['m', 'e']:
            _file_list = self._sort_file_list(visibility=visibility, directory=directory, sort=self._parameters['sort'])
        elif self._parameters['sort'] == 'a':
            _file_list = directory[visibility]['files']

        _list += self._generate_file_list(directory[visibility]['dirs'], bcolors.OKGREEN)
        _list += self._generate_file_list(_file_list, bcolors.WARNING)
        return _list

    def _generate_file_list(self, directory, color):
        _list = ''
        for _file in directory:

            if len(_file) > 24 and not self._parameters['no cut']:
                extension = _file.rsplit('.', 1)[-1]
                ending = "[...]" + '.' + extension
                formatted_file = _file[:24 - len(ending)]
                formatted_file += ending
            else:
                formatted_file = _file
            prefix = self._generate_prefix(self._parameters['path'], _file)
            subfix = self._generate_subfix(_file)
            tabs = self._calc_tabs(string=_file, tab_count=3)
            _list += color + prefix + '\t' + formatted_file + tabs + subfix + '\n'
        return _list

    def _calc_tabs(self, string, tab_count):
        tabs_count = round(((tab_count * 8 - len(string)) / 8) + 0.49)
        tabs = ''
        for i in range(tabs_count):
            tabs += '\t'
        return tabs

    def _sort_file_list(self, visibility, directory, sort):
        if sort == 'a':
            tmp = list(directory[visibility]['files'])
            return tmp.sort()

        vis_order = []
        for index, file in enumerate(directory[visibility]['files']):
            if sort == 'e':
                extension = file.rsplit('.', 1)[-1]
                vis_order.append((index, extension))
            elif sort == 'm':
                vis_order.append(
                    (index, self._file_utility.get_modified_date(path=self._parameters['path'], filename=file)))

        vis_order.sort(key=lambda tup: tup[1])
        vis_ordered = []
        for file in vis_order:
            vis_ordered.append(directory[visibility]['files'][file[0]])
        return vis_ordered

    def _specific_file(self, filename):



    @property
    def output(self):
        return self._generate_output()

    def _generate_output(self) -> str:
        directory = self._file_utility.files(path=self._parameters['path'])
        output = ''
        output += '\n' + bcolors.BOLD + bcolors.HEADER + bcolors.UNDERLINE + 'Files and directories you shouldn\'t be ' \
                                                                             'allowed to see:' + bcolors.ENDC + '\n '
        output += self._generate_header() + '\n'
        output += self._file_list(visibility='invisible', directory=directory)
        output += '\n' + bcolors.BOLD + bcolors.HEADER + bcolors.UNDERLINE + 'These are files you should be allowed ' \
                                                                             'to see:' + bcolors.ENDC + '\n '
        output += self._generate_header() + '\n'
        output += self._file_list(visibility='visible', directory=directory) + bcolors.ENDC + '\n\n'
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
                        return True, self._generate_help()
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
            print('Error occurred! ' + error.args[0] + '\n' + self._generate_help())
            exit()
        return parameters
