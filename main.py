from algorithm import FSRSContext, updateStability, updateDifficulty, initialDifficulty, initialStability, generateCombinations

def simulateSequence(grades, context, targetRetention):
    D = initialDifficulty(int(grades[0]))
    S = initialStability(int(grades[0]))
    intervals = []

    for i in range(1, len(grades)):
        t = context.calculateInterval(targetRetention, S)
        R = context.retrievability(t, S)
        intervals.append(t)

        grade = int(grades[i])
        D = updateDifficulty(D, grade)
        S = updateStability(S, D, R, grade)

    if len(grades) > 1:
        t = context.calculateInterval(targetRetention, S)
        intervals.append(t)
    
    return intervals

def checkTimeframe(intervals, timeframeLimit):
    if not intervals or timeframeLimit is None:
        return True
    
    # Sum of all intervals should be at least timeframeLimit
    total_sum = sum(intervals)
    if total_sum < timeframeLimit:
        return False
    
    # If sum without last interval exceeds timeframeLimit, exclude
    sum_without_last = sum(intervals[:-1])
    if sum_without_last > timeframeLimit:
        return False
    
    return True

def calculatePercentDeviation(intervals1, intervals2):
    if (not intervals1) or (not intervals2) or (len(intervals1) != len(intervals2)):
        return float("inf")
    deviations = []
    for i1, i2 in zip(intervals1, intervals2):
        deviation = abs(i1 - i2) / i1 * 100
        deviations.append(deviation)
    return sum(deviations) / len(deviations)

def findMatchingRetention(sequence, targetRetention, E, maxTimeframe=None):
    modifiedContext = FSRSContext(E)
    originalContext = FSRSContext(0)
    print(f"\nANALYZING SEQUENCE {sequence}")
    modifiedIntervals = simulateSequence(sequence, modifiedContext, targetRetention)

    if maxTimeframe and not checkTimeframe(modifiedIntervals, maxTimeframe):
        print("Sequence invalid due to timeframe constraint")
        return 0, float('inf')
    
    print(f"Modified intervals (E={E}): {[f'{x:.2f}' for x in modifiedIntervals]}")
    minDeviation = float('inf')
    bestRetention = targetRetention

    # Start from target retention and go down
    for retention in range(int(targetRetention * 100), 69, -1):
        testRetention = retention / 100
        originalIntervals = simulateSequence(sequence, originalContext, testRetention)
        deviation = calculatePercentDeviation(modifiedIntervals, originalIntervals)
        if deviation < minDeviation:
            minDeviation = deviation
            bestRetention = testRetention
            print(f"\nNew best match found!")
            print(f"Retention: {bestRetention:.4f}")
            print(f"Unmodified intervals: {[f'{x:.2f}' for x in originalIntervals]}")
            print(f"Average deviation: {deviation:.2f}%")

    return bestRetention, minDeviation

fixedList = ["3313", "4313", "3314", "4314", "3333", "4333"]
# Inputs and validation
while True:
    try:
        retentionInput = float(input("Enter desired retention (70-95): "))
        if 70 <= retentionInput <= 95:
            targetRetention = retentionInput / 100
            break
        else:
            print("Value must be between 70 and 95.")
    except ValueError:
        print("Number not valid.")

while True:
    try:
        eValue = float(input("Enter E value (0-200): "))
        if 0 <= eValue <= 200:
            break
        else:
            print("Please enter a non-negative value between 0 and 200.")
    except ValueError:
        print("Please enter a valid number.")

timeframeInput = input("Enter timeframe limit (days) or press Enter to skip: ")
timeframeLimit = None
if timeframeInput.strip():
    try:
        timeframeLimit = int(timeframeInput)
        if timeframeLimit <= 0:
            print("Invalid timeframe. Proceeding without timeframe limit.")
            timeframeLimit = None
    except ValueError:
        print("Invalid input. Proceeding without timeframe limit.")

# List choice input and simulation
while True:
    listChoice = input("Choose list (1 for fixed, 2 for generated): ")
    if listChoice in ['1', '2']:
        break
    print("Please enter either 1 or 2.")

if listChoice == "1":
    sequences = fixedList
else:
    minPercent3 = targetRetention * 100
    sequences = generateCombinations(minPercent3)

totalRetention = 0
totalError = 0
validSequences = 0

print("\nAnalyzing sequences...")
for sequence in sequences:
    matchedRetention, error = findMatchingRetention(sequence, targetRetention, eValue, timeframeLimit)
    if error != float('inf'):
        totalRetention += matchedRetention
        totalError += error
        validSequences += 1

if validSequences == 0:
    print("No valid sequences found with given parameters.")
else:
    averageMatchedRetention = totalRetention / validSequences
    averageError = totalError / validSequences
    relativeDecrease = (targetRetention - averageMatchedRetention) / targetRetention * 100

    print(f"\nResults:")
    print(f"Average Matched Retention: {averageMatchedRetention * 100:.2f}%")
    print(f"Average Error Margin: {averageError:.2f}%")
    print(f"Relative Decrease (Risk Factor): {relativeDecrease:.2f}%")
    print(f"Number of valid sequences analyzed: {validSequences}")