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
        prefix = ''
        if self._file_utility.is_exe(os.path.join(path, file)):
            prefix+='+'
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
        tmp.append('\t')

        subfix= "".join(tmp)

        for iterator in self._parameters['order']:
            subfix += self.generate_column(iterator=iterator, entry=entry, file=file)

        return subfix

    def generate_column(self, iterator, entry, file):
        subfix = "----\t"
        whitespaces = 0
        if iterator == 'modified date':
            tmp = self._file_utility.get_modified_date(path=self._parameters['path'], filename=file)
            whitespaces = 40 - len(tmp)
        else:
            tmp = entry[0][iterator]
            whitespaces = 40 - len(entry[0][iterator])
        subfix += tmp
        for i in range(round((whitespaces/8)+0.49)):
            subfix += '\t'
        return subfix

    def generate_header(self) -> str:
        topics = {'description': 'File Type:', 'suggested software': 'Recommended Software:',
                  'modified date': 'Modified Date:'}
        header = "\t\t\t\t\t"

        for iterator in self._parameters['order']:
            header += topics[iterator]
            header += self.calc_tabs(string=topics[iterator], tab_count=6)
        return header

    def file_list(self, visibility, directory):
        _file_list = []
        _list=""

        if self._parameters['sort'] in ['m','e']:
            _file_list = self.sort_file_list(visibility=visibility,directory=directory, sort=self._parameters['sort'])
        elif self._parameters['sort'] == 'a':
            _file_list = directory[visibility]['files']

        _list += self.generate_file_list(directory[visibility]['dirs'],bcolors.OKGREEN)
        _list += self.generate_file_list(_file_list, bcolors.WARNING)
        return _list

    def generate_file_list(self,directory,color):
        _list = ''
        for _file in directory:

            if len(_file) > 24 and self._parameters['no cut'] == False:
                extension = _file.rsplit('.', 1)[-1]
                ending = "[...]"+'.'+extension
                formatted_file=_file[:24-len(ending)]
                formatted_file+=ending
            else:
                formatted_file=_file
            prefix = self.generate_prefix(self._parameters['path'], _file)
            subfix = self.generate_subfix(self._parameters['path'], _file)
            tabs = self.calc_tabs(string=_file, tab_count=3)
            _list += color + prefix + '\t' + formatted_file + tabs + subfix + '\n'
        return _list

    def calc_tabs(self, string, tab_count):
        tabs_count = round(((tab_count*8 - len(string)) / 8) + 0.49)
        tabs = ''
        for i in range(tabs_count):
            tabs += '\t'
        return tabs

    def sort_file_list(self, visibility,directory, sort):
        if sort == 'a':
            tmp = list(directory[visibility]['files'])
            return tmp.sort()

        vis_order = []
        for index, file in enumerate(directory[visibility]['files']):
            if sort == 'e':
                extension = file.rsplit('.', 1)[-1]
                vis_order.append((index, extension))
            elif sort == 'm':
                vis_order.append((index, self._file_utility.get_modified_date(path=self._parameters['path'], filename=file)))

        vis_order.sort(key=lambda tup: tup[1])
        vis_ordered =[]
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
    help_string = 'Usage:\n'
    help_string +='\tlsython [-d|-g] [path|file] [-h|-f|-s|-m|-i|] \n'
    help_string += '\t\t-d [path]\tList directory information \n'
    help_string += '\t\t-g [file]\tList file information \n'
    help_string += '\t\t-s [a|m|e]\tSort (a)lphabetically[default] | by (m)odified date | by (e)xtension \n'
    help_string += '\t\t-c\t\tCut off long filenames to keep format. No cut if set \n'
    help_string += '\t\t-h\t\tShow help page \n'
    help_string += '\t\t-f\t\tShow additional information : file type \n'
    help_string += '\t\t-r\t\tShow additional information : recommended software \n'
    help_string += '\t\t-m\t\tShow additional information : modified date \n'

    return help_string
