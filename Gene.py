import random
class Gene:


    def __init__(self, course, time, day, room):

        self.course = course
        self.day= day
        self.time = int(time)
        self.room = room

    def mutate(self, courses, rooms, times):
        #Selects a random day from the available days in the timeslots
        unique_days = list(set(slot['day'] for slot in times))  # Get unique days from timeslots
        self.day = random.choice(unique_days)  # Randomly choose a day

        #Select a random timeslot for the selected day
        available_slots = [i for i, slot in enumerate(times) if
                           slot["day"] == self.day]  # Filter slots by the chosen day
        self.time = random.choice(available_slots)  # Choose a random available timeslot

        suitable_rooms = [room for room in rooms if room["capacity"] >= courses[self.course]["students"]]
        if not suitable_rooms:
            raise ValueError(f"No suitable room found for course {courses[self.course]['name']} with {courses[self.course]['students']} students.")

        self.room = rooms.index(random.choice(suitable_rooms))