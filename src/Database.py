from TestCase import TestCase


class Database:

    def __init__(self, database):
        self.database = database

    def createDatabase(self):
        database = []

    def getDatabase(self) -> set[TestCase]:
        """returns the database
        :return: database
        """
        return self.database

    def updateDatabase(self, database, test_cases) -> set[TestCase]:
        """updates the database to include the given test cases
        :param database:
        :param test_cases:
        :return: database
        """
        self.database = database + test_cases
        return self.database

    def loadDatabase(self):
        """reads a text file that stores a representation of the database and sets the database in the Database object
        to that stored database
        :return: nothing
        """
    def exportDatabase(self):
        """formats the database and saves a textfile with the formatted database
        :return: nothing
        """
