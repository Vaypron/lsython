import os
from extension import Lsython_database
from file_utility import file_utility


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
    def __init__(self, parameters):
        self._database = Lsython_database('extensions.json')
        self._file_utility = file_utility()
        self._parameters = parameters

    def generate_legend(self) -> str:
        return "+Executables  " + bcolors.WARNING + u"\u2588" + bcolors.ENDC + "File  " + bcolors.OKGREEN + u"\u2588" + bcolors.ENDC + "Directory"

    def generate_prefix(self, path, file) -> str:
        prefix = "    "
        if self._file_utility.is_exe(os.path.join(path, file)):
            tmp = list(prefix)
            tmp[0] = "+"
            prefix = "".join(tmp)
        return prefix

    def generate_subfix(self, path, file) -> str:
        extension = file.rsplit('.', 1)[-1]
        extension = '.' + extension
        if self._parameters['description'] or self._parameters['suggested software'] or self._parameters[
            'modified date']:
            entry = self._database.db_extensions.search(self._database.query.extension == extension)
            if len(entry) != 1:
                return ""
        else:
            return ""

        tmp = []
        for i in range(50 - len(file)):
            tmp.append(" ")
        subfix = "".join(tmp)

        for iterator in self._parameters['order']:
            subfix += self.generate_column(iterator=iterator, entry=entry, file=file)

        return subfix

    def generate_column(self, iterator, entry, file):
        subfix = "----    "
        whitespaces = 0
        if iterator == 'modified date':
            tmp = self._file_utility.get_modified_date(filename=file)
            whitespaces = 42 - len(tmp)
        else:
            tmp = entry[0][iterator]
            whitespaces = 42 - len(entry[0][iterator])
        subfix += tmp
        for i in range(whitespaces):
            subfix += " "
        return subfix

    def generate_header(self) -> str:
        topics = {'description': 'File Type:', 'suggested software': 'Recommended Software:',
                  'modified date': 'Modified Date:'}
        header = ""
        for i in range(54):
            header += " "
        for iterator in self._parameters['order']:
            header += topics[iterator]
            for i in range(50 - len(topics[iterator])):
                header += " "
        return header

    def file_list(self, visibility, directory):
        _list=""
        _file_list =  directory[visibility]['files']
        if self._parameters['sort']:
            _file_list = self.sort_file_list(visibility=visibility,directory=directory)
        for _file in directory[visibility]['dirs']:
            prefix = self.generate_prefix(self._parameters['path'], _file)
            subfix = self.generate_subfix(self._parameters['path'], _file)
            _list += bcolors.OKGREEN + prefix + _file + subfix+ '\n'

        for _file in _file_list:
            prefix = self.generate_prefix(self._parameters['path'], _file)
            subfix = self.generate_subfix(self._parameters['path'], _file)
            _list += bcolors.WARNING + prefix + _file + subfix + '\n'
        return _list

    def sort_file_list(self, visibility,directory):
        vis_order = []
        for index, file in enumerate(directory[visibility]['files']):
            extension = file.rsplit('.', 1)[-1]
            vis_order.append((index, extension))
        vis_order.sort(key=lambda tup: tup[1])
        vis_ordered = []
        for file in vis_order:
            vis_ordered.append(directory[visibility]['files'][file[0]])

        return vis_ordered

    def output(self) -> str:
        directory = self._file_utility.files(path=self._parameters['path'])
        output = ''
        output += '\n' + bcolors.BOLD + bcolors.HEADER + bcolors.UNDERLINE + 'Files and directories you shouldn\'t be ' \
                                                                             'allowed to see:' + bcolors.ENDC + '\n '
        output += self.generate_header() + '\n'
        output += self.file_list(visibility='invisible', directory=directory)
        output += '\n' + bcolors.BOLD + bcolors.HEADER + bcolors.UNDERLINE + 'These are files you should be allowed ' \
                                                                             'to see:' + bcolors.ENDC + '\n '
        output += self.generate_header() + '\n'
        output += self.file_list(visibility='visible', directory=directory) + bcolors.ENDC + '\n\n'
        output += self.generate_legend()
        return output


def generate_help() -> str:
    help_string = '\nlsython [-d|-g] [path|file] [-h|-f|-s|-m|-i|] \n'
    help_string += '  -d [path] List directory information \n'
    help_string += '  -g [file] List file information \n'
    help_string += '  -h        Show help page \n'
    help_string += '  -f        Show additional information : file type \n'
    help_string += '  -r        Show additional information : recommended software \n'
    help_string += '  -m        Show additional information : modified date \n'
    help_string += '  -s        sort by extension \n'
    return help_string
