from abc import ABC, abstractmethod # abc = abstract base class
import matplotlib.pyplot as plt
import numpy as np

# Base class that contains common functionality for all graph types
# I've decided not to just use df.plot here so that I can have extra control over the graph features
class BaseGraph(ABC):
    def __init__(self, data, path, date):
        self.data = data
        self.date = date
        self.path = path
        self.fig, self.ax = plt.subplots()  
    
    # This will contain the specific plotting logic for each graph type
    @abstractmethod
    def plot_graph(self):
        pass

    def finalize_graph(self, title, xlabel, ylabel):
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.fig.savefig('/Users/cole/Desktop/ClimbingWorkoutAnalyzer/src/graphs/' + self.path)
        plt.close(self.fig)
    

class LoadTrendGraph(BaseGraph):
    # Goal: Track how over/underloaded I am 
        # This graph will plot the load vs expected load
            # load = sets * reps * %1RM 
            # expected load = load determined by the training plan
            # actual load = load calculated from the actual workout data
            # timeframe = all time
            # lines: (one for actual load, one for expected load) * 3 -> (one for each workout on that day) = 6
            # x axis = date (every three days)
                # Major ticks = every 3 days
                # Minor ticks = every day
            # y axis = load
            # legend = each workout actual & expected will have its own line, so the legend will contain the names of each workout
            # title = "Actual vs Expected Load" 

    # data needed: 
        # day (current and every 3 days)
        # (for all three workouts on that type):
            # load (actual)
            # expected load (from training plan)

class MaxProgressionGraph(BaseGraph):
    # Goal: Track how my 1RM is progressing for all 9 exercises
        # use the 1RM formula to calculate the 1RM for each exercise for each date
        # timeframe = all time
        # lines: 2 for each exercise, one for benchmark 1RM, one for calculated 1RM
            # x axis = date
                # major ticks = every day
            # y axis = 1RM
                # major ticks = every 5 lbs
        # in the legend, include date of 1RM benchmark
        # title = "1RM progression"

    #data needed:
        # days 
        # (for all nine exercises):
            # 1RM (calculated from the actual workout data) for each date
class RPEvsTargetGraph(BaseGraph):
    # Goal: Track how my actual RPE compares to my target RPE
        # timeframe = all time
        # dumbell dot plot, with lines connecting the actual RPE to the target RPE
            # x axis = day
            # y axis = RPE
                # major ticks = 1 RPe
                # minor ticks = 0.5 RPE
        # title = "Actual vs Target RPE"

    # data needed:
        # day (current and every 3 days)
        # (for all three exercises):
            # actual RPE (calculated from the actual workout data) for each date
            # target RPE (from the training plan) for each date
class WeeklyConsistencyGraph(BaseGraph):
    # Goal: Track how consistent I am with my workouts and stretching
        # this will be a bar graph that shows a green bar for completed workouts and a red bar for missed workouts for each week
        # timeframe = all time
        # bars: 2 for each week, one for completed workouts, one for missed workouts
            # x axis = week number
                # major ticks = every week
            # y axis = number of workouts (red for missed, green for completed)
        # title = "Weekly Consistency"
        # legend = "Completed Workouts" and "Missed Workouts"
    def plot_graph(self):
        self.ax.
    # data needed:
        # week numbers
        # (for each week):
            # number of completed workouts
            # number of missed workouts
class LoadCycleSummaryGraph(BaseGraph):
    # Goal: Track where I am in my training cycle
        # I would like to have a simple line graph contains the load cycle values, with a circle around the current load cycle value
        # timeframe = all time
        # lines: 1 for the load cycle values, one circle around the current load cycle value
            # x axis = date
            # y axis = load cycle value
    def plot_graph(self):
        self.ax.plot(self.data['Date'],self.data['Load Cycle'])

        self.finalize_graph('Load Cycle Summary', 'Date', 'Load Block')
    # data needed:
        # day (current and every 3 days)
        # load cycle values (from the training plan) for each date (every 3 days)
        # current load cycle value (from the training plan) for the current date
