import Chromosone
import random
import ClassObj

def generateClasses(classesNum,courses,timeslots,profs):


    classes=[]
    for j in range(classesNum):
        course_index = j
        time_index = random.randint(0, len(Chromosone.times) - 1)
        prof_index = random.randint(0, len(Chromosone.profs) - 1)


        classes.append(ClassObj(course=course_index,time=Chromosone.times[time_index],prof=Chromosone.profs[prof_index]))





courses = []
rooms = []
timeslots = []

with open("t1/courses.txt", "r") as file:
    next(file)

    for line in file:
        name, professor, students, duration = line.strip().split(",")
        courses.append({
            "name": name,
            "professor": professor,
            "students": int(students),  # Convert to integer
            "duration": int(duration)  # Convert to integer
        })

with open("t1/rooms.txt", "r") as file:
    next(file)

    for line in file:
        name, capacity = line.strip().split(",")
        rooms.append({
            "name": name,
            "capacity": int(capacity)
        })

with open("t1/timeslots.txt", "r") as file:
    next(file)

    for line in file:
        day, hour = line.strip().split(",")
        timeslots.append({
            "day": day,
            "hour": int(hour)
        })

Chromosone.classes = courses
Chromosone.rooms = rooms
Chromosone.times = timeslots
profs=[course['professor'] for course in courses]
Chromosone.profs =profs
classesNum= len(Chromosone.classes)
generateClasses(classesNum,courses,timeslots,profs)





