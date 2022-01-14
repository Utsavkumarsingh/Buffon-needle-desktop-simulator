import math
import numpy as np
from numpy import random
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

UPDATE_FREQ = 1000
BOUND = 10
BORDER = 0.05 * BOUND
NEEDLES = 10000
NEEDLE_LENGTH = 1
FLOORBOARD_WIDTH = 2
FLOORBOARD_COLOR = 'black'
NEEDLE_INTERSECTING_COLOR = 'red'
NEEDLE_NON_INTERSECTING_COLOR = 'green'

class Needle :
    def __init__(self, x=None, y=None, theta=None, length=NEEDLE_LENGTH) :
        if x is None :
            x = random.uniform(0, BOUND)
        if y is None :
            y = random.uniform(0, BOUND)
        if theta is None :
            theta = random.uniform(0, math.pi)
        self.center = np.array([x, y])
        self.comp = np.array([length/2 * math.cos(theta), length/2 * math.sin(theta)])
        self.endPoints = np.array([np.add(self.center, -1 * np.array(self.comp)), np.add(self.center, self.comp)])
    def intersectsY(self, y):
        return self.endPoints[0][1] < y and self.endPoints[1][1] > y
class Buffon_Sim :
    def __init__(self) :
        self.floorboards = []
        self.boards = int ((BOUND / FLOORBOARD_WIDTH) + 1)
        self.needles = []
        self.intersections = 0
        window = "Buffon"
        title = "Simulation of Buffon's Needle Problem\nas a Monte Carlo method for approximating Pi"
        desc = (str(NEEDLES) + " needles of length " + str(NEEDLE_LENGTH) +
                " uniformly distributed over a " + str(BOUND) + " by " + str(BOUND) + " area" +
                " with floorboards of width " + str(FLOORBOARD_WIDTH))
        fig = plt.figure(figsize=(8, 8))
        fig.canvas.set_window_title(window)
        fig.suptitle(title, size=16, ha='center')
        self.buffon = plt.subplot()
        self.buffon.set_title(desc, style='italic', size=9, pad=5)
        self.results_text = fig.text(0, 0, self.updateResults(), size=10)
        self.buffon.set_xlim(0 - BORDER, BOUND + BORDER)
        self.buffon.set_ylim(0 - BORDER, BOUND + BORDER)
        plt.gca().set_aspect('equal')
    def plotFloorboards(self) :
        for j in range(self.boards) :
            self.floorboards.append(0 + j * FLOORBOARD_WIDTH)
            self.buffon.hlines(y=self.floorboards[j], xmin=0, xmax=BOUND, color=FLOORBOARD_COLOR, linestyle='--', linewidth=2.0)
    def tossNeedle(self) :
        needle = Needle()
        self.needles.append(needle)
        p1 = [needle.endPoints[0][0], needle.endPoints[1][0]]
        p2 = [needle.endPoints[0][1], needle.endPoints[1][1]]
        for k in range (self.boards) :
            if needle.intersectsY(self.floorboards[k]) :
                self.intersections += 1
                self.buffon.plot(p1, p2, color=NEEDLE_INTERSECTING_COLOR, linewidth=0.5)
                return
        self.buffon.plot(p1, p2, color=NEEDLE_NON_INTERSECTING_COLOR, linewidth=0.5)
    def plotNeedles(self) : 
        for i in range(NEEDLES) :
            self.tossNeedle()
            self.results_text.set_text(self.updateResults(i+1))
            if (i+1) % UPDATE_FREQ == 0 :
                plt.pause(1/UPDATE_FREQ)
    def updateResults(self, needlesTossed=0) :
        if self.intersections == 0 :
            sim_pi = 0
        else :
            sim_pi = (2 * NEEDLE_LENGTH * needlesTossed) / (FLOORBOARD_WIDTH * self.intersections)
        error = abs(((math.pi - sim_pi) / math.pi) * 100)
        return ("Intersections: " + str(self.intersections) +
                "\nTotal Needles: " + str(needlesTossed) +
                "\nApproximation of pi: " + str(sim_pi) +
                "\nError: " + str(error) + "%")
    def plot(self) :
        legend_lines = [mlines.Line2D([], [], color=FLOORBOARD_COLOR, linestyle='--', lw=2),
                        mlines.Line2D([], [], color=NEEDLE_INTERSECTING_COLOR, lw=1),
                        mlines.Line2D([], [], color=NEEDLE_NON_INTERSECTING_COLOR, lw=1)]
        self.buffon.legend(legend_lines, ['floorboard', 'intersecting needle', 'non-intersecting needle'], loc=1, framealpha=0.9)
        self.plotFloorboards()
        self.plotNeedles()
        plt.show()

def main() :
    bsim = Buffon_Sim()
    bsim.plot() 

main()