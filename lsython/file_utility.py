import os, stat
from datetime import datetime



class file:
    name = ''
    path = ''
    type = False
    executable = False
    invisible = False
    permissions = []
    link = ''
    size = None
    modified = ''


class file_utility:

    def _sort_in(self, store_in, filename, type):
        if filename[0] == '.':
            store_in['invisible'][type].append(filename)
        else:
            store_in['visible'][type].append(filename)

    def files(self, path):
        file_list = []

        if os.path.isdir(path):
            for filename in os.listdir(path):
                file_list.append(self.get_file_data(path=path, filename=filename))
        else:
            pass
        return file_list

    def get_file_data(self,path, filename):
        tmp = file()
        tmp.name = filename
        tmp.path = path

        _file = os.path.join(path, filename)
        info = os.lstat(_file)

        if filename[0] == '.':
            tmp.invisible = True

        if stat.S_ISDIR(info.st_mode):
            tmp.type = 'dir'
        elif stat.S_ISLNK(info .st_mode):
            tmp.type = 'link'
            tmp.link = os.readlink(_file)
        elif stat.S_ISREG(info.st_mode):
            tmp.type = 'file'
            if os.path.isfile(_file) and os.access(_file, os.X_OK):
                tmp.executable = True

        tmp.modified = datetime.fromtimestamp(info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

        for who in "USR", "GRP", "OTH":
            for what in "R", "W", "X":
                if stat.S_IMODE(info.st_mode) & getattr(stat, "S_I" + what + who):
                    tmp.permissions.append(what.lower())

        tmp.size = info.st_size

        return tmp