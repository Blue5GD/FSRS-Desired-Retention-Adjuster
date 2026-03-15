# FSRS-Desired-Retention-Adjustment
This was a Science Fair project I made back in 11th grade on Anki's FSRS-5 algorithm. It got 1st place in the mathematics & systems software category at regionals, but it didn't place at state probably because of my bad presentation skills at the time.


**IMPORTANT NOTE**: Many parts of this work is less useful now with FSRS-6 adding customizable forgetting curves, but the core problem persists.


Spaced repetition algorithms like FSRS in Anki can adjust its parameters to suit the user's learning patterns, but there's no objective or mathematical way to determine what desired retention they should use.


This program tries to fix this issue by doing the following:

1. modifying the decay constant in FSRS-5 to decrease forgetting curve speed by E% 
IMAGE
    - E represents the "effectiveness" of the user's encoding/study techniques. Research indicates that utilizing higher-order learning techniques that emphasize understanding relationships between concepts rather than isolated lower-order learning, such as interleaving and mind mapping (Lafleur and Kanazawa; Batdi; Firth et al.), can improve retention and reduce the decay rate of the forgetting curve.
IMAGE of Bloom's taxonomy and caption

2. attempting to find which desired retention in the unmodified algorithm best matches with the desired retention in the modified algorithm
    - the program does this by calculating error margins (how much the intervals deviate) between the original and modified algorithms for specific grade sequences

There is also a secondary visualizer program that outputs exact review intervals, calculates the % time the E-value saved, and graphs the forgetting curves of both algorithms.



## How I collected the data for my spreadsheet, graphs, etc
Data recorded on Google Sheet (LINK) for all combinations of these inputs:
- Desired retention from 75%-95% (steps of 5) 
- Various E-values from 0-200 (0, 5, 10, 15, 25, 50, 75, 100, 125, 150, 200, [10 total])
- 9 grade sequences to reflect a variety of possible Anki inputs (see image below)

so in total 450 combinations

IMAGE



## Project Screenshots
IMAGE
IMAGE



## Results
(Copy and pasted from my Science Fair board)
1. The % time E-values saved varied depending on the grade sequence, but were generally slightly higher or lower than E%. As desired retention lowered, this % progressively increased (see figure 11).
2. The matched FSRS-5 and modified FSRS-5 algorithms tended to deviate more as E increased, and more as desired retention decreased (see figures 13 and 14).
3. There were a total of 43 sequences (out of 450 total) where high E-values, in 75% and 80% retention, matched a desired retention below 70%. In Anki, you cannot set desired retention below 70% (see figure 12).
4. Error margins and matched retention were mostly consistent no matter what sequence was used to match the algorithms (see figure 15).
5. Rough estimates of E-value to desired retention decrease on figure 16.
IMAGE


**Why was there more deviation as desired retention decreased, and as E increased?**

In FSRS-5, the formula for the next scheduled interval is
IMAGE

Because 1/decay is a negative exponent, the function becomes more sensitive to change when r is smaller. 

Example: When E=0, for r = 0.9, r^-2 ~ 1.23; for r = 0.8, r^–2 ~ 1.56. 
But when E=100, for r = 0.9, r^-4 ~ 1.52; for r = 0.8, r^-4 ~ 2.44. 
r is approximately 2.79 times more sensitive when E=100.

This relationship also explains why E saved more time for lower desired retentions and less for higher desired retentions. 



## Conclusion (and future implications with FSRS-6)
- Because there was minimal deviation between the modified FSRS-5 algorithm and the matched unmodified FSRS-5 algorithm under optimal conditions, this suggests that this is an **accurate approach** to account for higher-order learning in FSRS-5 without modifying the core algorithm.
    - The low standard deviation between matched retention and error margins suggests there is a clear way to convert the modified FSRS-5 with E to the unmodified FSRS-5 with lower retention.
    - This conversion is not completely perfect, since lowering desired retention would make certain long intervals much longer when trying to match the modified algorithm with its best unmodified equivalent.
    - E-value matching is best suited when E causes a low relative decrease and when the user desires a higher retention, from 85% to 95%.
    - Intervals within the modified algorithm were reasonable, saved time, and had low relative decreases for most E-values, indicating that this would be helpful for a student utilizing higher-order learning techniques to save time.
- Because FSRS-6 now optimizes the user's forgetting curve, this is **no longer an effective approach**. **However, the issue of deciding what desired retention a user should use persists.**

In the future, I hope to create a new program that can mathematically determine the best desired retention a user should use. 

But for now... PEACE
