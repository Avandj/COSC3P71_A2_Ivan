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
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']  # Days of the week

        # Dictionary to track time slots for each day
        slotsPDay = {day: 0 for day in days}

        for slot in Chromosone.times:
            day = slot['day']
            slotsPDay[day] += 1

        for classO in self.classList:
            course = classO.course
            room = classO.room
            timeSlot = classO.time
            students = classO.students
            professor = classO.prof
            duration = classO.duration

            # Check for room capacity conflict
            if students > room['capacity']:
                conflicts += 2

            for hour in range(duration):
                # Map the day to an index from 0 to 4 (Monday to Friday)
                day_index = days.index(timeSlot['day'])
                current_slot = day_index * slotsPDay[timeSlot['day']] + timeSlot['hour'] + hour

                # Room usage conflicts
                if (room['name'], current_slot) not in roomUsage:
                    roomUsage[(room['name'], current_slot)] = 0
                roomUsage[(room['name'], current_slot)] += 1
                if roomUsage[(room['name'], current_slot)] > 1:
                    conflicts += 3

                # Professor schedule conflicts
                if (professor, current_slot) not in profSchedule:
                    profSchedule[(professor, current_slot)] = 0
                profSchedule[(professor, current_slot)] += 1
                if profSchedule[(professor, current_slot)] > 1:
                    conflicts += 1

        # Fitness score: Higher score for fewer conflicts
        return 1 / (1 + conflicts)

    def mutateClassL(self, times,rooms):
        for gene in self.classList:
            gene.mutate(times, rooms)
        self.updateFitness()



    def getFitness(self):
        return self.fitness

    def getClassList(self):
        return self.classList
