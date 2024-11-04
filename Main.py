

courses= []
rooms=[]
timeslots=[]

with open("t1/courses.txt","r") as file:
    next(file)

    for line in file:
        name, professor, students, duration = line.strip().split(",")
        courses.append({
            "name": name,
            "professor": professor,
            "students": int(students),  # Convert to integer
            "duration": int(duration)  # Convert to integer
        })

with open("t1/rooms.txt","r") as file:
    next(file)

    for line in file:
        name, capacity = line.strip().split(",")
        rooms.append({
            "name": name,
            "capacity": int(capacity)  # Convert to integer
        })

with open("t1/timeslots.txt","r") as file:
    next(file)

    for line in file:
        day, hour = line.strip().split(",")
        timeslots.append({
            "day": day,
            "hour": int(hour)  # Convert to integer
        })

