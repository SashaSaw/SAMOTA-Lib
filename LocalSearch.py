from Search import Search

class LocalSearch(Search):

    def __init__(self, percentage_local, min_per_cluster):
        self.percentage_local = percentage_local
        self.min_per_cluster = min_per_cluster

    def generateClusters(self):
        return


    def trainLocal(self, x, y) -> (int, int):
        """Short description of the method

        :param x:
        :param y:
        :return:
        """
        return 0, 0

    def calcFitnessLS(self):
        self.trainLocal(1, 1)
    def updateBestPredicted(self):

    def localSearch(self):