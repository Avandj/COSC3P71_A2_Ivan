from Gene import Gene
class Chromosone:

    classes=[];
    times=[];
    rooms=[];
    profs=[];



    def __init__(self,classList):
        self.classList=classList
        fitness=getFitness(self.classList);

    def __int__(self, classes, times, rooms, profs):
        Chromosone.classes=classes
        Chromosone.times=times
        Chromosone.rooms=rooms
        Chromosone.profs=profs

    def getFitness(self, classList):
        conflicts=0

    def checkConflicts(self):
        print()
