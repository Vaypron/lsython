import os
from datetime import datetime


class file_utility:
    def is_exe(self, fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    def files(self, path):
        items = {'visible': {'dirs': [], 'files': []}, 'invisible': {'dirs': [], 'files': []}}

        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                if file[0] == '.':
                    items['invisible']['files'].append(file)
                else:
                    items['visible']['files'].append(file)

            elif os.path.isdir(os.path.join(path, file)):
                if file[0] == '.':
                    items['invisible']['dirs'].append(file)
                else:
                    items['visible']['dirs'].append(file)

        return items

    def get_modified_date(self, filename):
        file = os.stat(filename)
        dt = datetime.fromtimestamp(file.st_mtime)

        return dt.strftime('%Y-%m-%d %H:%M:%S')

