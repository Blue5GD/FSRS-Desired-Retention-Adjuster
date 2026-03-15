import math
import itertools

"""
S : Stability
D : Difficulty, D ∈ [ 1 , 10 ]
R : Retrievability (probability of recall)
r : Request retention
t : Days since last review ("elapsed days")
I : Interval ("scheduled days"). Number of days before the card is due next

 G : Grade (card rating)
    1 : again
    2 : hard
    3 : good
    4 : easy
"""

# Default parameters FSRS-5 (CHANGEABLE)
w = {0:0.40255, 1:1.18385, 2:3.173, 3:15.69105, 4:7.1949, 5:0.5345, 6:1.4604, 7:0.0046, 8:1.54575, 9:0.1192, 
10:1.01925, 11:1.9395, 12:0.11, 13:0.29605, 14:2.2698, 15:0.2315, 16:2.9898, 17:0.51655, 18:0.6621}

# Forgetting curve constants (FSRS-4.5 and 5)
baseDecay = -0.5 # Base decay value
factor = 19/81
minDiffculty = 1
maxDifficulty = 10

# Algorithm configuration
# Context class so decay isn't recalculated after every interval
class FSRSContext:
    def __init__(self, E=0):
        self.decay = baseDecay * (100 / (100 + E)) # E=0 would be original FSRS-5

    def retrievability(self, t, S):
        return math.pow(1 + factor * t/S, self.decay)

    def calculateInterval(self, r, S):
        rawInterval = (S/factor) * (math.pow(r, 1/self.decay) - 1)
        if rawInterval < 1:
            return 1
        return round(rawInterval)

def initialDifficulty(grade):
    return min(max(w[4] - math.exp(w[5] * (grade - 1)) + 1, minDiffculty), maxDifficulty) 

def initialStability(grade):
    return w[grade-1]

def updateDifficulty(currentD, grade):
    deltaD = -w[6] * (grade - 3)
    dPrime = currentD + deltaD * ((10 - currentD)/9)
    dTarget = initialDifficulty(4)
    return w[7] * dTarget + (1 - w[7]) * dPrime

def stabilityIncrease(D, S, R, grade):
    w15 = w[15] if grade == 2 else 1
    w16 = w[16] if grade == 4 else 1
    return 1 + w15 * w16 * math.exp(w[8]) * (11 - D) * math.pow(S, -w[9]) * (math.exp(w[10] * (1-R)) - 1)

def updateStability(currentS, D, R, grade):
    if grade == 1:
        newS = w[11] * math.pow(D, -w[12]) * (math.pow(currentS + 1, w[13]) -1) * math.exp(w[14] *(1-R))
        return min(newS, currentS)
    else:
        sInc = stabilityIncrease(D, currentS, R, grade)
        return currentS * sInc

def updateSameDayStability(currentS, grade):
    return currentS * math.exp(w[17] * (grade - 3 + w[18]))


# Not a part of the algorithm, but combinations function for the secondary program
# Constants for string length (CHANGEABLE)
minLength = 1
maxLength = 15

def generateCombinations(minPercent3):
    if not (1 <= minPercent3 <= 100):
        raise ValueError ("Percentage must be between 1 and 100")
    validCombinations = []
    for length in range (minLength, maxLength + 1):
        for combo in itertools.product("13", repeat=length):
            string = "".join(combo)
            count3 = string.count("3")
            percent3 = (count3/length) * 100
            if percent3 >= minPercent3:
                validCombinations.append(string)
    return validCombinations


"""
NOTES: values aren't 100% precise 
https://open-spaced-repetition.github.io/anki_fsrs_visualizer/
is close enough though

https://www.reddit.com/r/Anki/comments/18jvyun/some_posts_and_articles_about_fsrs/ 
https://expertium.github.io/Algorithm.html  

https://github.com/ankitects/anki/issues/3094 
"""