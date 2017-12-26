from tinydb import TinyDB, Query

class Lsython_database:
    def __init__(self, db_file):
        self._db = TinyDB(db_file)
        self._db_extensions = self._db.table('extensions')
        self._query = Query()

    @property
    def db_extensions(self):
        return self._db_extensions

    @property
    def query(self):
        return self._query


#extensions.insert({'extension': '.h', 'description': 'C++ header file', 'suggested software' : 'Microsoft Visual Code'})

