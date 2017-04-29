from database import Database

class UniqueID:

    id = Database.getUniqueID()    

    @staticmethod
    def getUniqueID():
        UniqueID.id += 1
        Database.storeUniqueID(UniqueID.id)
        return UniqueID.id