from tinydb import TinyDB, Query

class Lsython_database:
    def __init__(self, db_file):
        self._db = TinyDB(db_file)
        self._db_extensions = self._db.table('extensions')
        self._query = Query()




#extensions.insert({'extension': '.h', 'description': 'C++ header file', 'suggested software' : 'Microsoft Visual Code'})

