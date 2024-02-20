
class SAMOTA:

    def __init__(self, objectives, populationSize, errorThreshold, globalMaxIter, localMaxIter, percentageLocal,
                 minPerCluster, database):
        self.objectives = objectives
        self.populationSize = populationSize
        self.errorThreshold = errorThreshold
        self.globalMaxIter = globalMaxIter
        self.localMaxIter = localMaxIter
        self.percentageLocal = percentageLocal
        self.minPerCluster = minPerCluster
        self.database = database

    def updateArchive(self):

    def samota(self):
