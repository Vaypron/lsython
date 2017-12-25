import os
import sys
from extension import Lsython_database

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

    def get_file_information(self, filename):
        file = os.stat(filename)
        print(file)

class Lsython:
    def __init__(self, descriptions, path, suggested_software):
        self._database = Lsython_database('extensions.json')
        self._file_utility = file_utility()
        self._descriptions = descriptions
        self._suggested_software = suggested_software
        self._path = path


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
        if self._descriptions or self._suggested_software:
            entry = self._database._db_extensions.search(self._database._query.extension == extension)
            if len(entry) != 1:
                return ""
        else:
            return ""

        tmp = []
        for i in range(50 - len(file)):
            tmp.append(" ")
        subfix = "".join(tmp)

        if self._descriptions:
            subfix += "----    "
            subfix += entry[0]['description']
            for i in range(40-len(entry[0]['description'])):
                subfix+=" "
        if self._suggested_software:
            subfix += "----    "
            subfix += entry[0]['suggested software']
        return subfix

    def generate_header(self):
        header = ""
        if self._descriptions:
            for i in range(59):
                header += " "
            header += "File Type:"
        if self._suggested_software:
            for i in range(38):
                header += " "
            header += "Suggested Software:"
        return header

    def output(self):
        print("")
        directory = self._file_utility.files(path=self._path)

        print(
            bcolors.BOLD + bcolors.HEADER + bcolors.UNDERLINE + "Files and directories you shouldn't be allowed to see:" + bcolors.ENDC)
        print("")

        print(self.generate_header())
        for invisible in directory["invisible"]["dirs"]:
            prefix =self.generate_prefix(path, invisible)
            print(bcolors.OKGREEN + prefix + invisible)

        for invisible in directory["invisible"]["files"]:
            prefix = self.generate_prefix(path, invisible)
            subfix = self.generate_subfix()
            print(bcolors.WARNING + prefix + invisible+subfix)

        print("")
        print(
            bcolors.BOLD + bcolors.HEADER + bcolors.UNDERLINE + "These are files you should be allowed to see:" + bcolors.ENDC)
        print("")
        print(self.generate_header())

        for visible in directory["visible"]["dirs"]:
            prefix = self.generate_prefix(path, visible)
            print(bcolors.OKGREEN + prefix + visible)

        for visible in directory["visible"]["files"]:
            prefix = self.generate_prefix(path, visible)
            subfix = self.generate_subfix(path, visible)
            print(bcolors.WARNING + prefix + visible + subfix)

        print(bcolors.ENDC)
        print("")
        print("")
        self.generate_legend()


if __name__ == "__main__":

    descriptions = False
    suggested_software = False
    path = '.'
    if len(sys.argv) == 1:
        path = '.'
    for index, arg in enumerate(sys.argv):
        if arg[0] == '-':
            if arg[1] == 'd':
                path = sys.argv[index + 1]
            elif arg[1] == 'm':
                descriptions = True
            elif arg[1] == 's':
                suggested_software = True

    active_class = Lsython(path=path, descriptions=descriptions, suggested_software=suggested_software )
    active_class.output()
