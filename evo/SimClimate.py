'''
file: SimClimate.py
Author: Richard Charczenko
See: Seattle University Biology Department
'''

import random

class Simulate_Climate():
    '''simulates climate for a given number of years and if desired change'''

    def __init__(self, change, yrs):
        self.climate = change
        self.years = yrs

    def generate_climate(self):
        count = 0
        weekStart = random.choice([21, 22, 23, 24, 25, 26, 27, 28])
        week = weekStart
        outPut = {}

        if self.climate == "change":
                while count < self.years: #generates climate change, plunging week of snow thaw
                    count += 1
                    b = random.choice(range(100))
                    o = weekStart - week
                    p = weekStart + 1
                    if o > 13:
                        week = week + 2
                        outPut[count] = week
                    elif week == weekStart:
                        y = random.choice(range(100))
                        if y < 51:
                            week = week - 2
                            outPut[count] = week
                        else:
                            outPut[count] = week
                    elif week >= p:
                        week = week - 2
                        outPut[count] = week
                    else:
                        if b <= 10:
                            c = random.choice(range(100))
                            if c < 40 or c == 40:
                                week = week - 2
                            else:
                                week = week - 1
                            outPut[count] = week
                        elif b in [11, 12, 13, 14]:
                            d = random.choice(range(100))
                            if d < 10 or d == 10:
                                week = week + 2
                            else:
                                week = week + 1
                            outPut[count] = week
                        else:
                            outPut[count] = week
        else:
            for i in range(self.years):
                outPut[i+1] = week - random.choice([-1,0,1])
        return outPut
