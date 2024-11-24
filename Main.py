from Chromosone import Chromosone
import random
from Gene import Gene


def generateChromosone(courses, timeslots, rooms):
    classes = []

    unique_days = list(set(slot['day'] for slot in timeslots))

    for j in range(len(courses)):
        course_index = j
        day_index = (random.choice(unique_days))

        available_slots = [i for i, slot in enumerate(timeslots) if slot["day"] == day_index]
        time_index = random.choice(available_slots)
        suitable_rooms = [room for room in rooms if room["capacity"] >= courses[j]["students"]]
        if not suitable_rooms:
            raise ValueError(f"No suitable room found for course {courses[j]['name']} with {courses[i]['students']} students.")

        room_index = rooms.index(random.choice(suitable_rooms))  # Select a random suitable room

        newGene = Gene(j, time_index, day_index, room_index)

        classes.append(newGene)


    chromosone = Chromosone(classes)

    # for i in range(len(classes)):
    ##print(str(i+1)+" "+str(classes[i].course)+", "+str(classes[i].time)+", "+str(classes[i].prof)+", "+str(classes[i].room)+"\n")

    # print(chromosone.getFitness())

    return chromosone

def printChromosone(chromosone, courses, timeslots, rooms):
    for i, gene in enumerate(chromosone.getClassList()):
        # Extract day and hour from timeslots using gene indices
        day = timeslots[gene.time]['day']
        hour = timeslots[gene.time]['hour']

        # Extract course name and room name
        course_name = courses[gene.course]['name']
        room_name = rooms[gene.room]['name']

        # Format the time string
        time = f"{day}: {hour}pm"

        # Print details
        print(f" {i + 1}: {course_name}, {time}, {room_name}")

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

def evolvePopulation(population, elitismRate, mutationRate, crossoveRate, gen):
    # Sort population by fitness (descending)
    population.sort(key=lambda chrom: chrom.getFitness(), reverse=True)

    if (gen > 1000):
        mutationRate = 0.25
        crossoveRate = 0.95

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
            child1.mutateClassL()

        if random.random() < mutationRate:
            child2.mutateClassL()

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
mutationRate = 0.05
population =500
courses = []








count=0
with open("t2/courses.txt", "r") as file:
    next(file)

    courses=[]
    for line in file:
        name, professor, students, duration = line.strip().split(",")

        # Creates a dict for each of the courses
        course_dict = {
            "name": name,
            "prof": professor,
            "students": int(students),
            "dur": int(duration)
        }

        # Add the dictionary to the courses list
        courses.append(course_dict)
        count+=1



rooms =[]

with open("t2/rooms.txt", "r") as file:
    next(file)

    for line in file:
        name, capacity = line.strip().split(",")

        # Add a dictionary for each room to the list
        rooms.append({
            "name": name,
            "capacity": int(capacity)
        })

timeslots = []

with open("t2/timeslots.txt", "r") as file:
    next(file)

    for line in file:
        day, hour = line.strip().split(",")
        timeslots.append({
            "day": day,
            "hour": int(hour)
        })



classesNum = len(courses)

Chromosone.courses = courses
Chromosone.rooms = rooms
Chromosone.timeslots = timeslots

chromPopulation = []

for i in range(population):
    tempChrom = generateChromosone(courses, timeslots, rooms)
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





    chromPopulation= evolvePopulation(chromPopulation, elitismRate, mutationRate, crossoverRate, gen)

    tempMax=chromPopulation[0].getFitness()

    if(maxfitness <tempMax):
        maxfitness=chromPopulation[0].getFitness()

    print("Gen" + str(gen) + ": " + str(maxfitness))

    gen += 1


printChromosone(chromPopulation[0], courses, timeslots, rooms)



