from Gene import Gene


class Chromosone:

    def __init__(self, classList):
        self.classList = classList
        self.size = len(classList)
        self.fitness = self.calcFitness()



    def calcFitness(self):
        conflicts = 0
        roomUsage = {}
        profSchedule = {}

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

                current_slot = timeSlot['hour'] + hour
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

