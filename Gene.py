import random
class Gene:
    def __init__(self, course, time, prof, room, students, duration):
        self.course = course
        self.time = time
        self.students=students
        self.prof = prof
        self.room = room
        self.duration=duration

    def mutate(self, rooms, times):
        self.time= times[random.randint(0, len(times) - 1)]
        self.room= rooms[random.randint(0, len(rooms) - 1)]