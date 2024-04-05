from Database import Database

class main:

    if __name__ == '__main__':
        database = Database()
        #database.setDefaultDatabase()
        database.loadDatabase("Test")
        database.exportDatabase("Database")
