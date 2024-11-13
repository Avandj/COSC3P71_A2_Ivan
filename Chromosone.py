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

# Comparison methods based on the fitness for max-heap
    def __lt__(self, other):
        # For max-heap, compares by negative fitness this makes sure that we get a max heap and not a min heap if the negative wasnt incliuded
        return -self.fitness < -other.fitness

    def __le__(self, other):

        return -self.getFitness() <= other.getFitness()

    def __gt__(self, other):

        return -self.getFitness() > other.getFitness()

    def __ge__(self, other):
        return -self.getFitness() >= other.getFitness()
