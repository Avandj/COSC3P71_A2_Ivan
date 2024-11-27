from Gene import Gene
import random


class Chromosone:

    # Static class variables
    courses = None
    rooms = None
    timeslots = None

    def __init__(self, classList=None):
        if classList is None:
            self.classList = []
            self.fitness=0
        else:
            self.classList = classList
            self.fitness=self.calcFitness()



    @classmethod
    def get_courses(cls):
        return cls.courses

    @classmethod
    def get_rooms(cls):
        return cls.rooms

    @classmethod
    def get_timeslots(cls):
        return cls.timeslots


    def addGene(self,gene):
        self.classList.append(gene)

    def updateFitness(self):
        self.fitness = self.calcFitness()

    def calcFitness(self):
        check=self.classList
        classN = len(self.classList)  # Number of classes in a Chromosone

        # Conflict matrices to track room and professor conflicts between pairs of classes
        roomConflictsM = [[0] * classN for _ in range(classN)]
        profConflictsM = [[0] * classN for _ in range(classN)]

        # Get courses, rooms, and timeslots from the Chromosone class (static)
        courses = Chromosone.get_courses()
        rooms = Chromosone.get_rooms()
        timeslots = Chromosone.get_timeslots()

        for i, classO1 in enumerate(self.classList):
            # Retrieve course, room, and scheduling details for the first class
            course1 = classO1.course  # Index of the course
            room1 = classO1.room  # Room index
            day1 = classO1.day  # Day index
            time1 = classO1.time  # Starting time index

            course_details1 = courses[course1]
            students1 = course_details1['students']
            professor1 = course_details1['prof']
            duration1 = course_details1['dur']

            # Check room capacity conflict
            try:
                if students1 > rooms[room1]["capacity"]:
                    roomConflictsM[i][i] += 2  # Self conflict for this class
            except Exception as e:
                print(f"Error checking room capacity for class {i}: {e}")

            # Check conflicts with other classes
            for j in range(i + 1, classN):  # Compare with classes after the current one
                classO2 = self.classList[j]

                # Retrieve course, room, and scheduling details for the second class
                course2 = classO2.course
                room2 = classO2.room
                day2 = classO2.day
                time2 = classO2.time  # Starting time index

                course_details2 = courses[course2]
                professor2 = course_details2['prof']
                duration2 = course_details2['dur']

                # Check room conflict (same room, same day, overlapping times)
                if room1 == room2 and day1 == day2:
                    if isinstance(time1, int) and isinstance(time2, int):  # Ensure times are integers
                        if time1 < time2 + duration2 and time2 < time1 + duration1:
                            if roomConflictsM[i][j] == 0:  # Only update once for this pair
                                roomConflictsM[i][j] += 3
                                roomConflictsM[j][i] += 3  # Symmetric update

                # Check professor conflict (same professor, same day, overlapping times)
                if professor1 == professor2 and day1 == day2:
                    if isinstance(time1, int) and isinstance(time2, int):  # Ensure times are integers
                        if time1 < time2 + duration2 and time2 < time1 + duration1:
                            if profConflictsM[i][j] == 0:  # Only update once for this pair
                                profConflictsM[i][j] += 1
                                profConflictsM[j][i] += 1  # Symmetric update

        # Debugging: Print the conflict matrices (optional)
        # print("Room Conflicts Matrix:", roomConflictsM)
        # print("Professor Conflicts Matrix:", profConflictsM)

        # Combine the conflict matrices (room and professor) to get the total number of conflicts
        totalConflicts = sum(sum(row) for row in roomConflictsM) + sum(sum(row) for row in profConflictsM)

        status=False
        if totalConflicts ==0:
            return 1

        # Fitness score: Higher score for fewer conflicts
        fitness = 1 / (1 + totalConflicts)
        return  fitness

    def mutateClassL(self, mutationRate):


        i=random.randint(0, len(self.classList)-1)

        if(random.random() < mutationRate):
            self.classList[i].mutate( Chromosone.get_courses(), Chromosone.get_rooms(), Chromosone.get_timeslots())

        self.updateFitness()



    def getFitness(self):
        return self.fitness

    def getClassList(self):
        return self.classList
