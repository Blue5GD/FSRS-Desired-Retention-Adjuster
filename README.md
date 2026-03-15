# FSRS-Desired-Retention-Adjustment
This was a Science Fair project I made back in 11th grade on Anki's FSRS-5 algorithm.


**IMPORTANT NOTE**: Many parts of this work is less useful now with FSRS-6 adding customizable forgetting curves, but the core problem persists.


Spaced repetition algorithms like FSRS in Anki can adjust its parameters to suit the individual's learning patterns, but there's no objective or mathematical way to determine what desired retention they should use.


This program tries to fix this issue by doing the following:
1. modifying the decay constant in FSRS-5 to decrease forgetting curve speed by E% 
IMAGE
    - E represents the "effectiveness" of the user's encoding/study techniques. Research indicates that utilizing higher-order learning techniques that emphasize understanding relationships between concepts rather than isolated lower-order learning, such as interleaving and mind mapping (Lafleur and Kanazawa; Batdi; Firth et al.), can improve retention and reduce the decay rate of the forgetting curve.

2. attempting to find which desired retention in the unmodified algorithm best matches with the desired retention in the modified algorithm
    - the program does this by calculating error margins (how much the intervals deviate) between the original and modified algorithms for specific grade sequences


## How I collected the data for my spreadsheet, graphs, etc
Data recorded on Google Sheet (LINK) for all combinations of these inputs:
- Desired retention from 75%-95% (steps of 5) 
- Various E-values from 0-200 (0, 5, 10, 15, 25, 50, 75, 100, 125, 150, 200, [10 total])
- 9 grade sequences to reflect a variety of possible Anki inputs (see image below)
IMAGE


## Project Screenshots and Results


