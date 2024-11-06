import ClassObj
class Chromosone:

    classes=[];
    times=[];
    rooms=[];
    profs=[];



    def __init__(self,classList):
        self.classList=classList

    def __int__(self, classes, times, rooms, profs):
        Chromosone.classes=classes
        Chromosone.times=times
        Chromosone.rooms=rooms
        Chromosone.profs=profs

    def checkConflicts(self):
        print()
