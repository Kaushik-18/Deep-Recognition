class UniqueID:

    id = 0    

    @staticmethod
    def getUniqueID():
        UniqueID.id += 1
        return UniqueID.id