from Gene import Gene


class Chromosone:

    def __init__(self, classList=None):

        if(classList != None):
            self.classList = classList
            self.size = len(classList)
            self.fitness = self.calcFitness()
        else:
            self.fitness = None
            self.classList = []


    def addGene(self,gene):
        self.classList.append(gene)

    def updateFitness(self):
        self.fitness = self.calcFitness();


    def calcFitness(self):
        conflicts = 0
        roomUsage = {}
        profSchedule = {}
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] #days in the week to make it easier to compare times

        # A dict that keeps track of the time slots for each day
        slotsPDay = {}
        for slot in Chromosone.times:
            day = slot['day']
            if day not in slotsPDay:
                slotsPDay[day] = 0
            slotsPDay[day] += 1

        for classO in self.classList:



            course = classO.course
            room = classO.room
            timeSlot = classO.time
            students =classO.students
            proffessor = classO.prof
            duration = classO.duration

            if (students > room['capacity']):
                conflicts += 2

            for hour in range(duration):

                day_index = days.index(timeSlot['day'])  # Maps the day for the class to a index from 0-4 represenrting monday to friday
                current_slot = day_index * slotsPDay[timeSlot['day']] + timeSlot['hour'] + hour

                if (room['name'], current_slot) not in roomUsage:
                    roomUsage[(room['name'], current_slot)] = 0
                roomUsage[(room['name'], current_slot)] += 1

                #checks for conflics for the rooms
                if roomUsage[(room['name'], current_slot)] > 1:
                    conflicts += 3

                if (proffessor, current_slot) not in profSchedule:
                    profSchedule[(proffessor, current_slot)] = 0
                profSchedule[(proffessor, current_slot)] += 1

                # Checks for professor conflicts
                if profSchedule[(proffessor, current_slot)] > 1:
                    conflicts += 1

        # Calculate fitness score: higher score for fewer conflicts
        return 1 / (1 + conflicts)



    def getFitness(self):
        return self.fitness

    def getClassList(self):
        return self.classList
