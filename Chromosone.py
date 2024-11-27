from Gene import Gene
import random


class Chromosone:

    # Static class variables
    courses = None
    rooms = None
    timeslots = None

    def __init__(self, classList=None):
        self.classList = classList if classList is not None else []
        self.fitness = self.calcFitness()

    @classmethod
    def get_courses(cls):
        return cls.courses

    @classmethod
    def get_rooms(cls):
        return cls.rooms

    @classmethod
    def get_timeslots(cls):
        return cls.timeslots

    def addGene(self, gene):
        self.classList.append(gene)

    def updateFitness(self):
        self.fitness = self.calcFitness()

    def calcFitness(self):
        classN = len(self.classList)
        roomConflictsM = [[0] * classN for _ in range(classN)]
        profConflictsM = [[0] * classN for _ in range(classN)]

        courses = Chromosone.get_courses()
        rooms = Chromosone.get_rooms()

        for i, classO1 in enumerate(self.classList):
            course1 = classO1.course
            room1 = classO1.room
            day1 = classO1.day
            time1 = classO1.time

            students1 = courses[course1]['students']

            if students1 > rooms[room1]["capacity"]:
                roomConflictsM[i][i] += 2  #

            for j in range(i + 1, classN):
                classO2 = self.classList[j]
                course2 = classO2.course
                room2 = classO2.room
                day2 = classO2.day
                time2 = classO2.time

                if room1 == room2 and day1 == day2 and time1 == time2:
                    roomConflictsM[i][j] += 3
                    roomConflictsM[j][i] += 3

                if courses[course1]['prof'] == courses[course2]['prof'] and day1 == day2 and time1 == time2:
                    profConflictsM[i][j] += 1
                    profConflictsM[j][i] += 1

        totalConflicts = sum(sum(row) for row in roomConflictsM) + sum(sum(row) for row in profConflictsM)

        return 1 / (1 + totalConflicts) if totalConflicts > 0 else 1

    def mutateClassL(self, mutationRate):
        for i in range(len(self.classList)):
            if random.random() < mutationRate:
                self.classList[i].mutate(Chromosone.get_courses(), Chromosone.get_rooms(), Chromosone.get_timeslots())
        self.updateFitness()

    def getFitness(self):
        return self.fitness

    def getClassList(self):
        return self.classList
