import requests
import json
from pprint import pprint
from enum import IntEnum

#url = 'https://api.devhub.virginia.edu/v1/courses'
#data = requests.get(url).json()

#data = json.dumps(data, indent=2)
#print(data)

#data = json.load(open("out.txt"))
#data = json.dumps(data["class_schedules"], indent=2)
#data = json.loads(data)

#print data columns
#pprint(data["columns"])

#display classes by index
'''fieldCount = len(data["columns"])
tabCount = [4, 3, 3, 3, 3, 2, 3, 2, 3, 2, 2, 4, 3]

while (True):
    index = int(input("> "))

    for i in range(fieldCount):
        name = data["columns"][i]
        value = data["records"][index][i]
        print(name + ("\t" * tabCount[i]) + str(value))
    print("")'''

#display all class subjects
'''classCount = len(data["records"])
classSubjects = []

for i in range(classCount):
    subject = data["records"][i][0]
    if not subject in classSubjects:
        classSubjects.append(subject)

pprint(classSubjects)'''

#display all class years
'''classCount = len(data["records"])
classYears = []

for i in range(classCount):
    year = data["records"][i][12]
    if not year in classYears:
        classYears.append(year)

pprint(classYears)'''

class ClassData(IntEnum):
    subject = 0
    catalogNumber = 1
    classSection = 2
    classNumber = 3
    classTitle = 4
    classTopicFormalDesc = 5
    instructor = 6
    enrollmentCapacity = 7
    meetingDays = 8
    meetingTimeStart = 9
    meetingTimeEnd = 10
    term = 11
    year = 12

#save fall classes to json
'''data = json.load(open("out.txt"))
data = json.dumps(data["class_schedules"], indent=2)
data = json.loads(data)

fallClasses = []

for i in range(len(data["records"])):
    if (data["records"][i][ClassData.year] == '2021 Fall'):
        fallClasses.append(data["records"][i])

fallClassesJson = json.dumps(fallClasses)
obj = open('fallClasses.txt', 'w')
obj.write(fallClassesJson)
obj.close()'''

fallClasses = json.load(open("fallClasses.txt"))

fallClassCount = len(fallClasses)
classYears = []

for i in range(fallClassCount):
    if (fallClasses[i][ClassData.subject] == 'ENTP'):
        year = fallClasses[i][ClassData.instructor]
        if not year in classYears:
            classYears.append(year)

pprint(classYears)