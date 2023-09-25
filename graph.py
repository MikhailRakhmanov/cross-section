import sys
import plotly.graph_objects as go
import re
import math
import numpy as np


class Particle:
    def __init__(self, mass, spin):
        self.mass = float(mass)
        self.spin = float(spin)

    def getInfo(self):
        print("mass: ", self.mass, "\nspin: ", self.spin)


def getParticles():
    particleInfoFile = open("checks/compoundnucleus.chk", 'r')
    particleData = particleInfoFile.readlines()
    numbers = []
    for dataLine in particleData:
        numbers.append(re.findall('\d+\.?\d*', dataLine))
    particle1 = Particle(numbers[8][0], numbers[5][0])
    particle2 = Particle(numbers[13][0], numbers[10][0])
    return [particle1, particle2]


def waveNumber(energy, particles):
    return math.sqrt(
        2 * particles[0].mass * particles[1].mass * energy / (particles[0].mass + particles[1].mass) / 41.8015876)


def drawMyCrossSection():
    fig.add_trace(
        go.Scatter(x=energies, y=crossSection, mode="lines", name="My cross section",
                   line=dict(color='red', width=1)))


def drawAzureCrossSection():
    fig.add_trace(
        go.Scatter(x=energies, y=azureCrossSection, mode="lines", name="Azure cross section",
                   line=dict(color='blue', width=2)))


def drawPhase():
    fig.add_trace(
        go.Scatter(x=energies, y=phases, mode="lines", name="Phase",
                   line=dict(color='green', width=1)))


particles = getParticles()
for particle in particles:
    particle.getInfo()
j = float(sys.argv[1])
s = 0

fileWithData = open('output/AZUREOut_aa=1_R=1.extrap', 'r')

energies = []
phases = []
crossSection = []
azureCrossSection = []

is_azure_cs = False
# Read file
for string in fileWithData:
    dataInLine = re.split('\s+', string)[1:6]
    if not len(dataInLine) == 5:
        is_azure_cs = True
        continue
    energy = float(dataInLine.pop(0))
    if is_azure_cs:
        azureCrossSection.append(float(dataInLine.pop(2)))
    else:
        phase = np.deg2rad(float(dataInLine.pop(2)))
        energies.append(energy)
        phases.append(phase)
        k = waveNumber(energy, particles)
        crossSectionI = (4 * math.pi / ((2 * s + 1) * (k ** 2))) * (2 * j + 1) * math.sin(phase) ** 2 / 100
        crossSection.append(crossSectionI)

fig = go.Figure()

# Add cross-section Line
drawAzureCrossSection()
drawMyCrossSection()
drawPhase()

# fig.update_yaxes(type="log")

fig.update_layout(title={'x': 0.5,
                         'text': "Cross section J = "+str(j)+", S = "+str(s)},
                  xaxis_title='CoM Energy',
                  yaxis_title='Cross section, [b]',
                  plot_bgcolor='white',
                  )

fig.show()
