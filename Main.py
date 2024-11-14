from Chromosone import Chromosone
import random
from Gene import Gene
import heapq

def generateChromosone(courses, timeslots, profs, rooms, population):
    classes=[]

    for j in range(len(courses)):
        course_index = j
        time_index = random.randint(0, len(timeslots) -1)
        prof_index = j
        students= courses[course_index]['students']
        room_index= random.randint(0, len(rooms) -1)
        course_name = courses[course_index]['name']
        duration = courses[course_index]['duration']


        classes.append(Gene(course=course_name,time=timeslots[time_index],prof=profs[prof_index],room=rooms[room_index], students=students , duration=duration))

    chromosone=Chromosone(classes)

    #for i in range(len(classes)):
        ##print(str(i+1)+" "+str(classes[i].course)+", "+str(classes[i].time)+", "+str(classes[i].prof)+", "+str(classes[i].room)+"\n")

    #print(chromosone.getFitness())

    return chromosone

def printChromosone(chromosone):

    for i, gene in enumerate(chromosone.getClassList()):
        print(f"{i + 1}: Course: {gene.course}, Time: {gene.time}, Prof: {gene.prof}, Room: {gene.room}")

def tournamentSelection(population):
    k=3

    tournament= random.sample(population,k)


    bestChromosone = max(tournament, key=lambda chrom: chrom.getFitness())


    #printChromosone(bestChromosone)

    return bestChromosone

'''
def crossover(parent1, parent2):
    mask=random.choice(0,2)
    for (int i=)
'''
#crossOvrRate=float(input("Enter your Crossover Rate: "))
#elitismRate=float(input("Enter your Elitism Rate: "))

crossoverRate=0;
elitismRate=0.2
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
            "students": int(students),
            "duration": int(duration)
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

population= 2*len(courses)
print(population)
Chromosone.classes = courses
Chromosone.rooms = rooms
Chromosone.times = timeslots
profs = [course['professor'] for course in courses]
students=[course['students'] for course in courses]
Chromosone.profs =profs
classesNum= len(Chromosone.classes)

chromPopulation= []


for i in range(population):
    tempChrom=generateChromosone(courses, timeslots, profs, rooms, population)
    chromPopulation.append( tempChrom)

chromPopulation = sorted(chromPopulation, key=lambda chrom: chrom.getFitness(), reverse=True)

for i in range(population):
    print(str(chromPopulation[i].getFitness()))
print("\n")

#Make initial random population
tournamentSelection(chromPopulation)

#Make new generation
newParents= []
elitism = int(population*elitismRate)



for i in range(elitism):
    newParents.append(chromPopulation[i])

for i in range(int(population-elitism)):
    tempWinner= tournamentSelection(chromPopulation)
    newParents.append( tempWinner)
    #print(str(tempWinner.getFitness()))

for i in range(len(newParents)):
    print(newParents[i].getFitness())

