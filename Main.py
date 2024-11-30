from Chromosone import Chromosone
import random
from Gene import Gene
import wandb
import json


def generateChromosone(courses, timeslots, rooms):
    classes = []
    unique_days = list(set(slot['day'] for slot in timeslots))
    courseNum = len(courses)

    for j in range(courseNum):
        course_index = j
        day_index = random.choice(unique_days)
        available_slots = [i for i, slot in enumerate(timeslots) if slot["day"] == day_index]
        time_index = random.choice(available_slots)
        suitable_rooms = [room for room in rooms if room["capacity"] >= courses[j]["students"]]

        if not suitable_rooms:
            raise ValueError(f"No suitable room found for course {courses[j]['name']} with {courses[j]['students']} students.")

        room_index = rooms.index(random.choice(suitable_rooms))
        newGene = Gene(j, time_index, day_index, room_index)
        classes.append(newGene)

    chromosone = Chromosone(classes)

    if courseNum != len(chromosone.getClassList()):
        print("Error: Mismatch in number of courses and genes in chromosome.")

    return chromosone

def printChromosone(chromosone, courses, timeslots, rooms):
    for i, gene in enumerate(chromosone.getClassList()):

        day = timeslots[gene.time]['day']
        hour = timeslots[gene.time]['hour']

        course_name = courses[gene.course]['name']
        room_name = rooms[gene.room]['name']
        duration = courses[gene.course]['dur']

        time = f"{day}: {hour}pm"


        print(f" {i + 1}: {course_name}, {duration}, {time}, {room_name}")

def tournamentSelection(population):
    k = 2


    tournament = random.sample(population, k)

    best = sorted(tournament, key=lambda chrom: chrom.getFitness(), reverse=True)

    # printChromosone(bestChromosone)

    return best[0],best[1]

def uniformCrossover(parent1, parent2):


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

def singlePointCrossover(parent1, parent2):
    child1 = Chromosone()
    child2 = Chromosone()

    crossover_point = random.randint(0, len(parent1.getClassList()) - 1)

    for i in range(len(parent1.getClassList())):
        if i < crossover_point:
            child1.addGene(parent1.getClassList()[i])
            child2.addGene(parent2.getClassList()[i])
        else:
            child1.addGene(parent2.getClassList()[i])
            child2.addGene(parent1.getClassList()[i])

    child1.updateFitness()
    child2.updateFitness()

    return child1, child2


def doublePointCrossover(parent1, parent2):
    child1 = Chromosone()
    child2 = Chromosone()

    point1 = random.randint(0, len(parent1.getClassList()) - 1)
    point2 = random.randint(0, len(parent1.getClassList()) - 1)

    # Ensures first pint is less than the sedodn
    if point1 > point2:
        point1, point2 = point2, point1

    for i in range(len(parent1.getClassList())):
        if point1 <= i < point2:
            child1.addGene(parent2.getClassList()[i])
            child2.addGene(parent1.getClassList()[i])
        else:
            child1.addGene(parent1.getClassList()[i])
            child2.addGene(parent2.getClassList()[i])

    child1.updateFitness()
    child2.updateFitness()

    return child1, child2

def genParents(chromPopulation):
    # Make new generation
    newParents = []
    parentNum = int(len(chromPopulation)/2)


    for i in range(parentNum):
        tempWinner = tournamentSelection(chromPopulation)
        tempWinner1=tempWinner[0]
        tempWinner2=tempWinner[1]
        newParents.append(tempWinner1)
        newParents.append(tempWinner2)
        # print(str(tempWinner.getFitness()))

    # for i in range(len(newParents)):
    # print(newParents[i].getFitness())
    return newParents

def evolvePopulation(population, elitismRate, mutationRate, crossoverRate, gen, crossover_type):
    newPopulation = []
    elitismNum = int(elitismRate * len(population))
    elites = population[:elitismNum]

    new_parents = genParents(population)
    random.shuffle(new_parents)

    for i in range(0, len(new_parents), 2):
        if i + 1 < len(new_parents):
            if random.random() < crossoverRate:
                if crossover_type == 'single':
                    child1, child2 = singlePointCrossover(new_parents[i], new_parents[i + 1])
                elif crossover_type == 'double':
                    child1, child2 = doublePointCrossover(new_parents[i], new_parents[i + 1])
                else:
                    child1, child2 = uniformCrossover(new_parents[i], new_parents[i + 1])
            else:
                child1, child2 = new_parents[i], new_parents[i + 1]

            child1.mutateClassL(mutationRate)
            child2.mutateClassL(mutationRate)

            newPopulation.append(child1)
            newPopulation.append(child2)

    newPopulation.extend(elites)
    newPopulation = sorted(newPopulation, key=lambda chrom: chrom.getFitness(), reverse=True)

    # Ensures the new population size matches the original
    newPopulation = newPopulation[:len(population)]

    return newPopulation


def geneticAlgorithm(crossoverRate, elitismRate, mutationRate, population, fileLoc, isTest,crossoverType):
    # crossOvrRate=float(input("Enter your Crossover Rate: "))
    # elitismRate=float(input("Enter your Elitism Rate: "))


    maxGen=1200


    print(str(population))
    #int(input("Enter your Population Size: "))
    courses = []


    maxFitnesList=[]
    avgFitnesList=[]

    courseFile=fileLoc+"/courses.txt"
    roomFile=fileLoc+"/rooms.txt"
    timeslotsFile = fileLoc + "/timeslots.txt"





    count=0
    with open(courseFile, "r") as file:
        next(file)

        courses=[]
        for line in file:
            name, professor, students, duration = line.strip().split(",")


            course_dict = {
                "name": name,
                "prof": professor,
                "students": int(students),
                "dur": int(duration)
            }


            courses.append(course_dict)
            count+=1



    rooms =[]

    with open(roomFile, "r") as file:
        next(file)

        for line in file:
            name, capacity = line.strip().split(",")


            rooms.append({
                "name": name,
                "capacity": int(capacity)
            })

    timeslots = []



    with open(timeslotsFile, "r") as file:
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



    print("Calulating...")
    gen = 0
    maxfitness = 0.0
    crossoverPop = 0

    results = []
    fitnessData=[]

    while (maxfitness != 1 ):





        chromPopulation= evolvePopulation(chromPopulation, elitismRate, mutationRate, crossoverRate, gen,crossover_type)

        tempMax=chromPopulation[0].getFitness()

        avg=0
        for i in range(len(chromPopulation)):
            avg+=chromPopulation[i].getFitness()

        avg/=len(chromPopulation)


        if(maxfitness <tempMax):
            maxfitness=chromPopulation[0].getFitness()



        maxFitnesList.append(tempMax)
        avgFitnesList.append(avg)

        if isTest:
            wandb.log({"generation": gen, "max_fitness": maxfitness, "avg_fitness": avg})
            fitnessData.append({"generation": gen, "max_fitness": maxfitness, "avg_fitness": avg})

        print("Gen: "+str(gen)+" Max: "+str(maxfitness)+" Avg: "+str(avg))

        if (gen == maxGen):
            break

        gen += 1



    printChromosone(chromPopulation[0], courses, timeslots, rooms)

    return maxFitnesList, avgFitnesList


#crossoverRate = 0.95
#elitismRate = 0.01
#mutationRate = 0.2
#population =250


#geneticAlgorithm(crossoverRate, elitismRate, mutationRate, population,"t1/courses.txt","t1/rooms.txt", "t1/timeslots.txt",1200, False)

# Defines the parameter combinations for the testing stuff
parameter_combinations = [
    {"name": "T1 - Full Crossover, No Mutation", "crossover_rate": 1.0, "mutation_rate": 0.0, "elitism_rate": 0.01, "file_loc": "t1"},
    {"name": "T1 - Full Crossover, 10% Mutation", "crossover_rate": 1.0, "mutation_rate": 0.1, "elitism_rate": 0.01, "file_loc": "t1"},
    {"name": "T1 - 90% Crossover, No Mutation", "crossover_rate": 0.9, "mutation_rate": 0.0, "elitism_rate": 0.01, "file_loc": "t1"},
    {"name": "T1 - 90% Crossover, 10% Mutation", "crossover_rate": 0.9, "mutation_rate": 0.1, "elitism_rate": 0.01, "file_loc": "t1"},
    {"name": "T1 - Optimized Settings", "crossover_rate": 0.95, "mutation_rate": 0.05, "elitism_rate": 0.01, "file_loc": "t1"},

    {"name": "T2 - Full Crossover, No Mutation", "crossover_rate": 1.0, "mutation_rate": 0.0, "elitism_rate": 0.01, "file_loc": "t2"},
    {"name": "T2 - Full Crossover, 10% Mutation", "crossover_rate": 1.0, "mutation_rate": 0.1, "elitism_rate": 0.01, "file_loc": "t2"},
    {"name": "T2 - 90% Crossover, No Mutation", "crossover_rate": 0.9, "mutation_rate": 0.0, "elitism_rate": 0.01, "file_loc": "t2"},
    {"name": "T2 - 90% Crossover, 10% Mutation", "crossover_rate": 0.9, "mutation_rate": 0.1, "elitism_rate":0.01, "file_loc": "t2"},
    {"name": "T2 - Optimized Settings", "crossover_rate": 0.95, "mutation_rate": 0.05, "elitism_rate": 0.01, "file_loc": "t2"}
]



# Function to run the GA and logs results to website thing
def run_experiment(groupName,crossover_rate, mutation_rate, elitism_rate, fileLoc):
    # Initialize W&B run for tracking
    wandb.init(project="course-scheduling",name=groupName, config={
        "crossover_rate": crossover_rate,
        "mutation_rate": mutation_rate,
        "elitism_rate": elitism_rate,
        "population_size": 250

    })

    # Run the GA
    fitness_data = []
    population=250


    # Simulate the evolution process
    geneticAlgorithm(crossover_rate, elitism_rate, mutation_rate, population, fileLoc,True)




    # Save the fitness data as an artifact
    with open("fitness_data.json", "w") as f:
        json.dump(fitness_data, f)

    # Create a W&B artifact to upload the data
    artifact = wandb.Artifact(f'fitness_data_{crossover_rate}_{mutation_rate}', type='dataset')
    artifact.add_file('fitness_data.json')
    wandb.log_artifact(artifact)

    # Save the final solution (if applicable)
    wandb.save("final_solution.onnx")

    # Close the W&B run
    wandb.finish()

crossover_type_input = input("Select crossover type: \n1. Single-Point \n2. Double-Point \n3. Uniform\nEnter 1, 2, or 3: ")

if crossover_type_input == '1':
        print("You selected Single-Point Crossover")

        crossover_type = 'single'
elif crossover_type_input == '2':
        print("You selected Double-Point Crossover")

        crossover_type = 'double'
elif crossover_type_input == '3':
        print("You selected Uniform Crossover")

        crossover_type = 'uniform'
else:
        print("Invalid input. Defaulting to Uniform Crossover.")
        crossover_type = "uniform"


geneticAlgorithm(0.9,.01,0.01,250,"t1",False,crossover_type)

'''
#for i, params in enumerate(parameter_combinations):
    group_name = params["name"]  # Use the test criteria name as the group name
    for run in range(5):  # Repeat 5 times
        print(f"Running experiment {i + 1}, repetition {run + 1}, group: {group_name}")
        run_experiment(
            groupName=group_name,  # Pass group name for grouping
            crossover_rate=params["crossover_rate"],
            mutation_rate=params["mutation_rate"],
            elitism_rate=params["elitism_rate"],
            fileLoc=params["file_loc"]
        )
'''
