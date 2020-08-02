#Name: Madeline McMahon, Carolyn Fish, Seva Galitskiy, Bri Ganzon
#Class: Bio 3770

import sys

#cyclin A1, B1, C1, D1 are tumor phenotypes (do not exit cycle into G0 at 20 hrs)
#cyclin A2, B2, C1, D1 are healthy cell phenotypes (exit cycle into G0 at 20 hrs)
def main(p53_opt, DNAdamage, rB_opt): #defined variables for various cyclin scenarios, each variable is a list consisting of values that graph a respective shape for each cyclin
    cyclinA1 = [0,0,0,0,0,0,0,0,0,0.25,0.75,2,3.5,5,6.5,8,9.5,11,12.5,14,14.75,15.25,15.5,15.5,15,13,10.5,7,0.25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.25,0.75,2,3.5,5,6.5,8,9.5,11,12.5,14,14.75,15.25,15.5,15.5,15,13,10.5,7,0.25,0,0,0,0,0,0,0,0,0,0,0]
    cyclinA2 = [0,0,0,0,0,0,0,0,0,0.25,0.75,2,3.5,5,6.5,8,9.5,11,12.5,14,14.75,15.25,15.5,15.5,15,13,10.5,7,0.25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    cyclinB1 = [0,0,0,0,0,0,0,0,0,0,0,0,0.3,0.75,1.25,1.9,2.5,3.25,4,5,6,7,8.5,10,11.3,13.5,15,15,13,7,0.25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.3,0.75,1.25,1.9,2.5,3.25,4,5,6,7,8.5,10,11.3,13.5,15,15,13,7,0.25,0,0,0,0,0,0,0,0,0]
    cyclinB2 = [0,0,0,0,0,0,0,0,0,0,0,0,0.3,0.75,1.25,1.9,2.5,3.25,4,5,6,7,8.5,10,11.3,13.5,15,15,13,7,0.25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    cyclinE1 = [0,0,0,0,0,0,0,0,0,2,5,9,13,14.5,15,14,11,4,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,5,9,13,14.5,15,14,11,4,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    cyclinE2 = [0,0,0,0,0,0,0,0,0,2,5,9,13,14.5,15,14,11,4,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    cyclinD1 = [0,0,4.5,6,7.5,8.5,9.5,10.25,11,11.5,12,12.5,12.75,13,13.15,13.25,13.4,13.5,13.5,13.5,13.5,13.5,13.5,13.5,13.4,13.25,13,12.75,12.5,12,11.5,11,10.25,9.5,8.5,7.5,6,4.5,0,0,0,0,4.5,6,7.5,8.5,9.5,10.25,11,11.5,12,12.5,12.75,13,13.15,13.25,13.4,13.5,13.5,13.5,13.5,13.5,13.5,13.5,13.4,13.25,13,12.75,12.5,12,11.5,11,10.25,9.5,8.5,7.5,6,4.5,0,0]
    cyclinD2 = [0,0,4.5,6,7.5,8.5,9.5,10.25,11,11.5,12,12.5,12.75,13,13.15,13.25,13.4,13.5,13.5,13.5,13.5,13.5,13.5,13.5,13.4,13.25,13,12.75,12.5,12,11.5,11,10.25,9.5,8.5,7.5,6,4.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    p53neg = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    p53pos = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,4.5,5,4.5,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,4.5,5,4.5,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
    cyclinA = []
    cyclinB = []
    cyclinE = []
    cyclinD = []
    p53 = []
    rB = []
    Rbpos=[11,11,11,11,11,11,11,11,10.9,10.75,10.3,8.75,6,3,0.25,0,0,0,0,0,0.25,3,6,8.75,10.3,10.75,10.9,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11]
    Rbneg=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

#x-axis consisting of a time scale (half hour increments)
    xaxis = [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15,15.5,16,16.5,17,17.5,18,18.5,19,19.5,20,20.5,21,21.5,22,22.5,23,23.5,24,24.5,25,25.5,26,26.5,27,28,28.5,29,29.5,30,30.5,31,31.5,32,32.5,33,33.5,34,34.5,35,35.5,36,36.5,37,37.5,38,38.5,39,39.5,40]

    #p53 = input("Do you want a p53 mutation? (Yes/No) : " ) #definition of prompts for a p53 mutatation

    #DNAdamage = input("Do you want DNA damage? (Yes/No) : ") #definition of prompts for DNA damage

    #rB = input("Do you want rb to be mutated? (Yes/No) : ") #definition of prompts for prescence of rB
    print (p53, DNAdamage, rB)
    if (p53_opt and not rB_opt): #checks for error state (active p53 and prescence of rB)
        sys.exit("Error state")
        #print ("Error")

    if not rB_opt: #if statements that evaluate rB input and designate levels of rB during cell cycle (assign list of y-values)
        rB = Rbneg
    elif rB_opt:
        rB = Rbpos

    #if statments that evaluate DNAdamage and p53 input, 4 possible scenarios
    #scenarios designate the amounts of cyclin and p53 during cell cycle (assign list of y-values)
    if p53_opt and DNAdamage:

        cyclinA = cyclinA2
        cyclinB = cyclinB2
        cyclinE = cyclinE2
        cyclinD = cyclinD2
        p53 = p53pos
    elif p53_opt and not DNAdamage:
        cyclinA = cyclinA2
        cyclinB = cyclinB2
        cyclinE = cyclinE2
        cyclinD = cyclinD2
        p53 = p53pos
    elif not p53_opt and DNAdamage:
        cyclinA = cyclinA1
        cyclinB = cyclinB1
        cyclinE = cyclinE1
        cyclinD = cyclinD1
        p53 = p53neg
    elif not p53_opt and not DNAdamage:
        cyclinA = cyclinA1
        cyclinB = cyclinB1
        cyclinE = cyclinE1
        cyclinD = cyclinD1
        p53 = p53neg

    return xaxis,cyclinA,cyclinB,cyclinE,cyclinD,p53,rB
