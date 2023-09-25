import matplotlib.pyplot as plot
import re
import sys


countOfQNumbers = 0
fileWithData = open('lomatrixandpene.chk', 'r')

# Skip info strings in file
for i in range(5):
    fileWithData.readline()


qNumbers = []
points = []
energies = []
resultOfParsing = []

# Read file
for string in fileWithData:
    list = re.split('\s+', string)
    for i in range(2):
        list.pop(0)

    point = list.pop(0)
    j = list.pop(0)
    ch = list.pop(0)
    l = list.pop(0)
    energy = list.pop(0)
    penetrability = list.pop(0)
    currentLMatrix = list.pop(0)[1:-1].split(',')
    currentLMatrix = [float(currentLMatrix[0]),float(currentLMatrix[1])]

    if qNumbers.__contains__([j, ch, l]):
        resultOfParsing[qNumbers.index([j, ch, l])].get("Penetrobility").append(float(penetrability))
        resultOfParsing[qNumbers.index([j, ch, l])].get("lMatrix").append(currentLMatrix)
    else:
        qNumbers.append([j, ch, l])
        resultOfParsing.append({
            "qNumber": (j, ch, l),
            "Penetrobility": [float(penetrability)],
            "lMatrix": [currentLMatrix]
        })


    if qNumbers[0].__eq__([j, ch, l]):
        points.append(int(point))
        energies.append(float(energy))

energies2point = {
    "energies": energies,
    "points": points
}


if sys.argv[1].__eq__("p"):
    for i in range(len(resultOfParsing)):
        plot.plot(energies2point.get("points"), resultOfParsing[i].get("Penetrobility"))
else:
    i = int(sys.argv[1])
    plot.plot(energies2point.get("points"),resultOfParsing[i].get("lMatrix"))
plot.show()
