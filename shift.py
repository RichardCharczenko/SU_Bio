
class cleanLog(object):

    def __init__(self, changeLog):
        self.log = changeLog
    
    def nullDel(self, key):
        for newKey in self.log:
            if self.log[newKey][0] == self.log[key][0] and newKey < key:
                self.log[newKey].append("silent")


    def nullPoint(self, key):
        for newKey in self.log:
            if self.log[key][0] == self.log[newKey][0] and newKey < key:
                self.log[newKey].append("silent")
        
    def setNull(self):
        for key in self.log:
            if self.log[key][2] == "Del":
                self.nullDel(key)
            if self.log[key][2] == "Point":
                if self.log[key][3].istitle():
                    self.nullPoint(key)

    def shiftLog(self):
        for key in self.log:
            if self.log[key][2] == "In":
                for x in self.log:
                    if self.log[x][0] > self.log[key][0]:
                        self.log[x][0] += 1
            if self.log[key][2] == "Del":
                for x in self.log:
                    if self.log[x][0] > self.log[key][0]:
                        self.log[x][0] -= 1
        
                    
## Test Code ##
'''
dic0 = {0: [33, 'A', 'Point', 't'], 1: [12, 'C', 'Point', 'a'],
        2: [7, 'M', 'Point', 'l'], 3: [16, 'Y', 'In'],
        4: [36, 'D', 'Point', 't'], 5: [2, 'R', 'Point', 'l'],
        6: [12, 'M', 'Point', 'C'], 7: [20, 'Q', 'Point', 'n'],
        8: [10, 'T', 'Point', 'v'], 9: [1, 'K', 'Point', 'a'],
        10: [6, 'R', 'Point', 'l']}

dic1 = {0: [22, 'L', 'Point', 'n'], 1: [23, 'M', 'Point', 'v'],
        2: [25, 'T', 'Point', 'v'], 3: [23, 'C', 'Point', 'M'],
        4: [26, 'T', 'Point', 'n'], 5: [15, 'Y', 'Point', 'm'],
        6: [21, 'L', 'Point', 'v'], 7: [2, 'l', 'Del'],
        8: [9, 'T', 'Point', 'v'], 9: [24, 'S', 'Point', 'T'],
        10: [15, 'L', 'Point', 'm']}

s = cleanLog(dic1)
s.shiftLog()
s.setNull()

for key in s.log:
    print key, s.log[key]
'''

