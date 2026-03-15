import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithm import FSRSContext, updateStability, updateDifficulty, initialDifficulty, initialStability

class FSRSVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("FSRS-5 Visualizer")
        self.root.geometry("1200x800")
        
        # Frames and grid weights
        self.controlFrame = ttk.Frame(root, padding="10")
        self.controlFrame.grid(row=0, column=0, sticky="nsew")
        self.graphFrame = ttk.Frame(root, padding="10")
        self.graphFrame.grid(row=0, column=1, sticky="nsew")
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)

        self.setupControls()
        self.setupGraphs()

    def setupControls(self):
        # Input fields
        inputFrame = ttk.LabelFrame(self.controlFrame, text="Simulation Settings", padding="5")
        inputFrame.grid(row=0, column=0, pady=10, sticky="ew")

        ttk.Label(inputFrame, text="Desired Retention (70-95%):").grid(row=0, column=0, padx=5)
        self.retentionVar = tk.StringVar(value="90")
        self.retentionEntry = ttk.Entry(inputFrame, textvariable=self.retentionVar, width=10)
        self.retentionEntry.grid(row=0, column=1)

        ttk.Label(inputFrame, text="Effectiveness (0-200):").grid(row=1, column=0, padx=5)
        self.effectivenessVar = tk.StringVar(value="0")
        self.effectivenessEntry = ttk.Entry(inputFrame, textvariable=self.effectivenessVar, width=10)
        self.effectivenessEntry.grid(row=1, column=1)

        ttk.Label(inputFrame, text="Visualization Period (months):").grid(row=2, column=0, padx=5)
        self.monthsVar = tk.StringVar(value="12")
        self.monthsEntry = ttk.Entry(inputFrame, textvariable=self.monthsVar, width=10)
        self.monthsEntry.grid(row=2, column=1)

        # Sequence Input
        self.sequenceFrame = ttk.LabelFrame(self.controlFrame, text="Grade Sequence", padding="5")
        self.sequenceFrame.grid(row=1, column=0, pady=10, sticky="ew")
        ttk.Label(self.sequenceFrame, text="Enter grades (1=again, 2=hard, 3=good, 4=easy):").grid(row=0, column=0)
        self.sequenceVar = tk.StringVar()
        self.sequenceEntry = ttk.Entry(self.sequenceFrame, textvariable=self.sequenceVar)
        self.sequenceEntry.grid(row=1, column=0, sticky="ew")

        # Simulate button
        buttonFrame = ttk.Frame(self.controlFrame)
        buttonFrame.grid(row=2, column=0, pady=10)
        self.simulateButton = ttk.Button(buttonFrame, text="Run Simulation", command=self.runSimulation)
        self.simulateButton.grid(row=0, column=0, padx=5)

    def validateInputs(self):
        try: 
            retention = float(self.retentionVar.get())
            if not (70 <= retention <= 95):
                raise ValueError("Retention must be between 70 and 95%")
            effectiveness = float(self.effectivenessVar.get())
            if not (0 <= effectiveness <= 200):
                raise ValueError("Effectiveness must be between 0 and 200")
            months = int(self.monthsVar.get())
            if months < 1:
                raise ValueError("Simulation period must be at least 1 month")
            
            sequence = self.sequenceVar.get().strip()
            if not sequence:
                raise ValueError("Grade sequence not entered")
            if not all(g in "1234" for g in sequence):
                raise ValueError("Invalid grade sequence. Use only 1, 2, 3, or 4 no spaces")
            return True

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return False

    def setupGraphs(self):
        self.figure, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 8))
        self.figure.subplots_adjust(hspace=0.3)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graphFrame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.ax1.set_title("Standard FSRS-5")
        self.ax1.set_xlabel("Days")
        self.ax1.set_ylabel("Retention")
        self.ax2.set_title("Modified FSRS-5 (with E value)")
        self.ax2.set_xlabel("Days")
        self.ax2.set_ylabel("Retention")


    def simulateSingleReviewSequence(self, gradeSequence, E=0):
        context = FSRSContext(E=E)
        daysSinceStart = 0
        currentDifficulty = initialDifficulty(int(gradeSequence[0]))
        currentStability = initialStability(int(gradeSequence[0]))
        intervals = []
        retentions = []
        simulationStats = []

        # First review
        interval = context.calculateInterval(float(self.retentionVar.get())/100, currentStability)
        simulationStats.append((interval, currentDifficulty, currentStability))
        print(f"Review #1: Interval: {interval:.1f} days, Difficulty: {currentDifficulty:.2f}, Stability: {currentStability:.2f}")

        # Retention curve points for first interval
        tPoints = np.linspace(0, interval, 100)
        rPoints = [context.retrievability(t, currentStability) for t in tPoints]
        intervals.append(tPoints)
        retentions.append(rPoints)

        daysSinceStart += interval

        # Any subsequent review
        reviewCount = 2
        for grade in gradeSequence[1:]:
            grade = int(grade)

            R = context.retrievability(interval, currentStability)
            currentDifficulty = updateDifficulty(currentDifficulty, grade)
            currentStability = updateStability(currentStability, currentDifficulty, R, grade)
            interval = context.calculateInterval(float(self.retentionVar.get())/100, currentStability)

            simulationStats.append((interval, currentDifficulty, currentStability))
            print(f"Review #{reviewCount}: Interval: {interval:.1f} days, Difficulty: {currentDifficulty:.2f}, Stability: {currentStability:.2f}")

            tPoints = np.linspace(daysSinceStart, daysSinceStart + interval, 100)
            rPoints = [context.retrievability(t - daysSinceStart, currentStability) for t in tPoints]
            intervals.append(tPoints)
            retentions.append(rPoints)

            daysSinceStart += interval
            reviewCount += 1
            if daysSinceStart > int(self.monthsVar.get()) * 30:
                break

        return intervals, retentions, daysSinceStart, simulationStats


    def runSimulation(self):
        if not self.validateInputs():
            return
        self.ax1.clear()
        self.ax2.clear()

        sequence = self.sequenceVar.get().strip()
        
        print("\n=== Standard FSRS-5 ===")
        intervals1, retentions1, days1, stats1 = self.simulateSingleReviewSequence(sequence, E=0)
        print("\n=== Modified FSRS-5 ===")
        E = float(self.effectivenessVar.get())
        intervals2, retentions2, days2, stats2 = self.simulateSingleReviewSequence(sequence, E=E)

        # Calculate time savings MAYBE get rid of efficiency ratio
        if days1 > 0:
            timeSavedPercent = ((days1 - days2) / days1) * 100
            print(f"\nTime Savings Analysis:")
            print(f"Standard FSRS total days: {days1:.1f}")
            print(f"Modified FSRS total days: {days2:.1f}")
            print(f"Time saved with E={E}: {timeSavedPercent:.3f}%")
            if E > 0:
                efficiency_ratio = timeSavedPercent / E
                print(f"Efficiency ratio (time saved % / E value): {efficiency_ratio:.3f}")

        # Plot results
        self.plotForgettingCurves(intervals1, retentions1, self.ax1, "Standard FSRS-5")
        self.plotForgettingCurves(intervals2, retentions2, self.ax2, f"Modified FSRS-5 (E={E})")
        self.canvas.draw()

    def plotForgettingCurves(self, intervals, retentions, ax, title):
        for t, r in zip(intervals, retentions):
            ax.plot(t, r)
        ax.set_title(title)
        ax.set_xlabel("Days")
        ax.grid(True)
        ax.set_ylim(0, 1)

        # set x-axis based on visualization period
        maxDays = int(self.monthsVar.get()) * 30
        ax.set_xlim(0, maxDays)


root = tk.Tk()
app = FSRSVisualizer(root)
root.mainloop()