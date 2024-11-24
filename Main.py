from Chromosone import Chromosone
import random
from Gene import Gene


def generateChromosone(courses, timeslots, profs, rooms):
    classes = []

    for j in range(len(courses)):
        course_index = j
        time_index = random.randint(0, len(timeslots) - 1)
        prof_index = j
        students = courses[course_index]['students']
        room_index = random.randint(0, len(rooms) - 1)
        course_name = courses[course_index]['name']
        duration = courses[course_index]['duration']

        classes.append(
            Gene(course=course_name, time=timeslots[time_index], prof=profs[prof_index], room=rooms[room_index],
                 students=students, duration=duration))

    chromosone = Chromosone(classes)

    # for i in range(len(classes)):
    ##print(str(i+1)+" "+str(classes[i].course)+", "+str(classes[i].time)+", "+str(classes[i].prof)+", "+str(classes[i].room)+"\n")

    # print(chromosone.getFitness())

    return chromosone


def printChromosone(chromosone):
    for i, gene in enumerate(chromosone.getClassList()):
        print(f" {i + 1}:{gene.course},{gene.time},{gene.room}")


def tournamentSelection(population):
    k = 3


    tournament = random.sample(population, k)

    bestChromosone = max(tournament, key=lambda chrom: chrom.getFitness())

    # printChromosone(bestChromosone)

    return bestChromosone


def crossover(parent1, parent2):
    mask = None

    child1 = Chromosone()
    child2 = Chromosone()

    mask = ""
    for i in range(len(parent1.getClassList())):
        mask += str(random.choice([0, 1]))

    # print(mask)
    # print("Parent 1")
    # printChromosone(parent1)
    # print("\n")
    # print("Parent 2")
    # printChromosone(parent2)
    # print("\n")

    for i in range(len(mask)):
        if (mask[i] == '1'):
            child1.addGene(parent1.getClassList()[i])
            child2.addGene(parent2.getClassList()[i])
        else:
            child1.addGene(parent2.getClassList()[i])
            child2.addGene(parent1.getClassList()[i])

        child1.updateFitness()
        child2.updateFitness()
    return child1, child2


def genParents(chromPopulation):
    # Make new generation
    newParents = []
    parentNum = int(len(chromPopulation))


    for i in range(parentNum):
        tempWinner = tournamentSelection(chromPopulation)
        newParents.append(tempWinner)
        # print(str(tempWinner.getFitness()))

    # for i in range(len(newParents)):
    # print(newParents[i].getFitness())
    return newParents


def evolvePopulation(population, elitismRate, mutationRate, crossoveRate):
    # Sort population by fitness (descending)
    population.sort(key=lambda chrom: chrom.getFitness(), reverse=True)

    newPopulation = []

    elites=[]

    for i in range(int(elitismRate*len(population))):
        elites.append(population[i])

    # Generate new parents
    new_parents = genParents(population)




    # Perform crossover to generate children

    for i in range(0, len(new_parents) - 1, 2):

        if(random.random() < crossoveRate):
            child1, child2 = crossover(new_parents[i], new_parents[i+1])
        else:
            child1, child2 = new_parents[i], new_parents[i + 1]




        # Apply mutation with a certain probability
        if random.random() < mutationRate:
            child1.mutateClassL(Chromosone.rooms, Chromosone.times)

        if random.random() < mutationRate:
            child2.mutateClassL(Chromosone.rooms, Chromosone.times)

        newPopulation.append(child1)
        newPopulation.append(child2)

    newPopulation.sort(key=lambda chrom: chrom.getFitness(), reverse=False)
    for i in range(len(elites)):
        newPopulation.pop(0)
        newPopulation.append(elites[i])

    # Ensure the new population size matches the original
    while len(newPopulation) != len(population):
        print("bad pop")

    newPopulation = sorted(newPopulation, key=lambda chrom: chrom.getFitness(), reverse=True)

    return newPopulation


# crossOvrRate=float(input("Enter your Crossover Rate: "))
# elitismRate=float(input("Enter your Elitism Rate: "))


crossoverRate = 0.9
elitismRate = 0.01
mutationRate = 0.02
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

population = 250
# print(population)
Chromosone.classes = courses
Chromosone.rooms = rooms
Chromosone.times = timeslots
profs = [course['professor'] for course in courses]
students = [course['students'] for course in courses]
Chromosone.profs = profs
classesNum = len(Chromosone.classes)

chromPopulation = []

for i in range(population):
    tempChrom = generateChromosone(courses, timeslots, profs, rooms)
    chromPopulation.append(tempChrom)

chromPopulation = sorted(chromPopulation, key=lambda chrom: chrom.getFitness(), reverse=True)

# for i in range(population):
# print(str(chromPopulation[i].getFitness()))
# print("\n")



print("Calculating...")
gen = 0
maxfitness = 0.0
crossoverPop = 0




while (maxfitness != 1):





    chromPopulation= evolvePopulation(chromPopulation, elitismRate, mutationRate, crossoverRate)

    tempMax=chromPopulation[0].getFitness()

    if(maxfitness <tempMax):
        maxfitness=chromPopulation[0].getFitness()

    print("Gen" + str(gen) + ": " + str(maxfitness))

    gen += 1




