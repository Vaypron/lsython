import os
import sys
from extension import Lsython_database
from datetime import datetime


class bcolors:
    HEADER = '\033[91m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class file_utility:
    def is_exe(self, fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    def files(self, path):
        items = {"visible": {"dirs": [], "files": []}, "invisible": {"dirs": [], "files": []}}

        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                if file[0] == '.':
                    items["invisible"]["files"].append(file)
                else:
                    items["visible"]["files"].append(file)

            elif os.path.isdir(os.path.join(path, file)):
                if file[0] == ".":
                    items["invisible"]["dirs"].append(file)
                else:
                    items["visible"]["dirs"].append(file)

        return items

    def get_modified_date(self, filename):
        file = os.stat(filename)
        dt = datetime.fromtimestamp(file.st_mtime)

        return dt.strftime('%Y-%m-%d %H:%M:%S')


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
        if self._parameters['description'] or self._parameters['suggested software'] or self._parameters['modified date']:
            entry = self._database._db_extensions.search(self._database._query.extension == extension)
            if len(entry) != 1:
                return ""
        else:
            return ""

        tmp = []
        for i in range(50 - len(file)):
            tmp.append(" ")
        subfix = "".join(tmp)

        for iterator in self._parameters['order']:
            subfix += self.generate_column(iterator=iterator,entry=entry,file=file)

        return subfix

    def generate_column(self,iterator,entry,file):
        subfix = "----    "
        whitespaces = 0
        if iterator == 'modified date':
            tmp = self._file_utility.get_modified_date(filename=file)
            whitespaces = 42 - len(tmp)

        else:
            tmp = entry[0][iterator]
            whitespaces = 42 - len(entry[0][iterator])

        subfix+=tmp
        for i in range(whitespaces):
            subfix += " "

        return subfix

    def generate_header(self) -> str:
        topics = {'description' : 'File Type:', 'suggested software': 'Recommended Software:', 'modified date' : 'Modified Date:'}
        header = ""
        for i in range(59):
            header += " "
        for iterator in self._parameters['order']:
            header += topics[iterator]
            for i in range(50-len(topics[iterator])):
                header += " "
        return header

    def output(self):
        print("")
        directory = self._file_utility.files(path=self._parameters['path'])

        print(
            bcolors.BOLD + bcolors.HEADER + bcolors.UNDERLINE + "Files and directories you shouldn't be allowed to see:" + bcolors.ENDC)
        print("")

        print(self.generate_header())
        for invisible in directory["invisible"]["dirs"]:
            prefix = self.generate_prefix(self._parameters['path'], invisible)
            print(bcolors.OKGREEN + prefix + invisible)

        for invisible in directory["invisible"]["files"]:
            prefix = self.generate_prefix(self._parameters['path'], invisible)
            subfix = self.generate_subfix(self._parameters['path'], invisible)
            print(bcolors.WARNING + prefix + invisible + subfix)

        print("")
        print(
            bcolors.BOLD + bcolors.HEADER + bcolors.UNDERLINE + "These are files you should be allowed to see:" + bcolors.ENDC)
        print("")
        print(self.generate_header())

        for visible in directory["visible"]["dirs"]:
            prefix = self.generate_prefix(self._parameters['path'], visible)
            print(bcolors.OKGREEN + prefix + visible)

        for visible in directory["visible"]["files"]:
            prefix = self.generate_prefix(self._parameters['path'], visible)
            subfix = self.generate_subfix(self._parameters['path'], visible)
            print(bcolors.WARNING + prefix + visible + subfix)

        print(bcolors.ENDC)
        print("")
        print("")
        print(self.generate_legend())


if __name__ == "__main__":
    parameters = {'path': '.', 'description': False, 'suggested software': False, 'modified date': False, 'order': []}
    descriptions = False
    suggested_software = False

    if len(sys.argv) > 1:
        for index, arg in enumerate(sys.argv):
            if arg[0] == '-':
                if arg[1] == 'd':
                    parameters['path'] = sys.argv[index + 1]
                elif arg[1] == 'f':
                    parameters['description'] = True
                    parameters['order'].append('description')
                elif arg[1] == 's':
                    parameters['suggested software'] = True
                    parameters['order'].append('suggested software')
                elif arg[1] == 'm':
                    parameters['modified date'] = True
                    parameters['order'].append('modified date')

    active_class = Lsython(parameters=parameters)
    active_class.output()
