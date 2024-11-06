from Gene import Gene
class Chromosone:

    classes=[];
    times=[];
    rooms=[];
    profs=[];



    def __init__(self,classList):
        self.classList=classList
        fitness=self.getFitness(self.classList);


    ##Method for storing the full list of classes, profs, room, and times
    @classmethod
    def setStaticAttributes(cls, classes, times, rooms, profs):
        """Set the static attributes for the class."""
        cls.classes = classes
        cls.times = times
        cls.rooms = rooms
        cls.profs = profs

    def getFitness(self, classList):
        conflicts=0
        roomUsage={}
        profSchedule={}

        for classO in classList:

            course= classO.course
            room=classO.room
            timeSlot=classO.time
            proffessor=classO.prof

    def checkConflicts(self):
        print()
