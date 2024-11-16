from Chromosone import Chromosone
import random
from Gene import Gene




def generateChromosone(courses, timeslots, profs, rooms):
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
        print(f" {i + 1}:{gene.course},{gene.time},{gene.room}")

def tournamentSelection(population):
    k=3

    tournament= random.sample(population,k)


    bestChromosone = max(tournament, key=lambda chrom: chrom.getFitness())


    #printChromosone(bestChromosone)

    return bestChromosone


def crossover(parent1, parent2):

    mask=None

    child1=Chromosone()
    child2=Chromosone()

    mask=""
    for i in range(len(parent1.getClassList())):
        mask+=str(random.choice([0,1]))

    #print(mask)
    #print("Parent 1")
    #printChromosone(parent1)
    #print("\n")
    #print("Parent 2")
    #printChromosone(parent2)
    #print("\n")

    for i in range(len(mask)):
        if(mask[i]=='1'):
            child1.addGene(parent1.getClassList()[i])
            child2.addGene(parent2.getClassList()[i])
        else:
            child1.addGene(parent2.getClassList()[i])
            child2.addGene(parent1.getClassList()[i])

        child1.updateFitness()
        child2.updateFitness()
    return child1, child2


def genParents(chromPopulation, population, elitismRate):

    # Make new generation
    newParents = []
    parentNum = population / 2
    elitism = int(population * elitismRate)




    for i in range(int(population-elitism)):
        tempWinner = tournamentSelection(chromPopulation)
        newParents.append(tempWinner)
        # print(str(tempWinner.getFitness()))

    #for i in range(len(newParents)):
        #print(newParents[i].getFitness())
    return newParents


#crossOvrRate=float(input("Enter your Crossover Rate: "))
#elitismRate=float(input("Enter your Elitism Rate: "))

crossoverRate = 0.7
elitismRate = 0.1
mutationRate = 0.2
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

population= 10*len(courses)
#print(population)
Chromosone.classes = courses
Chromosone.rooms = rooms
Chromosone.times = timeslots
profs = [course['professor'] for course in courses]
students=[course['students'] for course in courses]
Chromosone.profs =profs
classesNum= len(Chromosone.classes)

chromPopulation= []


for i in range(population):
    tempChrom=generateChromosone(courses, timeslots, profs, rooms)
    chromPopulation.append( tempChrom)

chromPopulation = sorted(chromPopulation, key=lambda chrom: chrom.getFitness(), reverse=True)

#for i in range(population):
    #print(str(chromPopulation[i].getFitness()))
#print("\n")

#Make initial random population
tournamentSelection(chromPopulation)






print("Calculating...")
gen=0
maxfitness=None

while (chromPopulation[0].getFitness()!=1):
    gen+=1

    chromPopulation = sorted(chromPopulation, key=lambda chrom: chrom.getFitness(), reverse=True)
    bestChromosones = []

    for i in range(int(population* elitismRate)):
        bestChromosones.append(chromPopulation[i])

    maxfitness=bestChromosones[0].getFitness()
    newParents=genParents(chromPopulation, population, elitismRate)
    chromPopulation=[]

    for i in range(len(bestChromosones)):
        chromPopulation.append(bestChromosones[i])

    #Loop for crossovers for parents
    while (len(newParents)> 0):

        if len(newParents) >= 2:
            # Perform crossover on pairs of parents
            child1, child2 = crossover(newParents[0], newParents[1])
            newParents.pop(0)
            newParents.pop(0)
        else:
            child1, child2 = crossover(newParents[0], chromPopulation[0])
            newParents.pop(0)


        if random.random() < mutationRate:
            child1.mutateClassL(rooms, timeslots)

        if random.random() < mutationRate:
            child2.mutateClassL(rooms, timeslots)

        chromPopulation.append(child1)
        chromPopulation.append(child2)
    if(len(chromPopulation)!=population):
        print("Idiot")
    chromPopulation = sorted(chromPopulation, key=lambda chrom: chrom.getFitness(), reverse=True)
    if(chromPopulation[0].getFitness()!=maxfitness):
        print(str(gen)+": "+str(chromPopulation[0].getFitness()))

    maxfitness=chromPopulation[0].getFitness()




