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
        # timeframe = current vs benchmark date
        # dumbbell dot plot connecting index of 1 to improvement index
            # x-axis: workout names (9)
            # y- axis: improvmeent indices
        # it would be nice to show original and new weights inside the plots
        # in the legend, include date of 1RM benchmark and explanation of the index
        # title = "1RM progression"
    def plot_graph(self):
        workouts = self.data['Workout'].tolist()
        self.ax.set_xticklabels(workouts)
        self.ax.set_ybound(.8, 1.4)
        self.ax.set_yticklabels(np.arange(.8,1.4,.05))
        
        # for each workout, plot the base point and improvement index and connect them
        for workout in workouts:
            # plot base point and new improvement index
            self.ax.scatter(self.data['Workout'], 1)
            self.ax.scatter(self.data['Workout'], self.data['Improvement Index'])
            
            # connect the points with a line between them
            self.ax.plot((self.data['Workout'], self.data['Workout']),(1, self.data['Improvement Index']))

            # put the base weight in the first point, and the new weight in the second point
            self.ax.text(self.data['Workout'], 1, str(self.data['Previous 1RM']))
            self.ax.text(self.data['Workout'], 1, str(self.data['Current 1RM']))

        
        self.finalize_graph('1RM progression', 'Workouts', 'Improvement Index')
    #data needed:
        # (for all nine exercises):
            # 1RM (calculated from the actual workout data) for each date
            # prev 1RM
class RPEvsTargetGraph(BaseGraph):
    # Goal: Track how my actual RPE compares to my target RPE
        # timeframe = all time
        # 3 figures, 1 for each workout. Each has a line for expected rpe and actual, area will be shaded in blue if actual RPE is higher, and yellow if expected RPE is higher
            # x axis = day
            # y axis = RPE
                # major ticks = 1 RPe
                # minor ticks = 0.5 RPE
        # title = "Actual vs Target RPE"
    def plot_graph(self):
        # Override original declaration since there's 3 subplots
        self.fig, self.ax = plt.subplots(3, sharex=True) 
        for i in range(3):
            expected = self.data[f'Expected RPE W{i+1}']
            actual = self.data[f'Actual RPE W1{i+1}']
            days = self.data['Day']
            self.ax[i].plot(days, expected, color='Blue')
            self.ax[i].plot(days, actual, color='Orange')
            # shade area to highlight deviance from expected
            self.ax[i].fill_between(days, expected, actual,
                                    where=(expected > actual),color='Blue')
            self.ax[i].fill_between(days, expected, actual,
                                    where=(expected < actual), color='Orange')
            self.ax[i].set_title(f'Workout {i+1}')
        
        # Make title less generic
        possible_titles = {
            'Weighted Pull Up' : 'Pulling Accesory Workouts',
            'Incline Bench' : 'Pushing Accessory Workouts',
            'Barbell Squat' : 'Leg Accessory Workouts'
        }
        workout_type = possible_titles[self.data['Workout 1'].iloc[0]]
        self.finalize_graph('Actual vs Target RPE for ' + workout_type, 'Day', 'RPE')

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
        bar_width, x_locations = .4, np.arange(self.data['Week'])
        self.ax.bar(x_locations - bar_width/2, self.data['completed_workouts'], width=bar_width/3,color='Green',label='Completed')
        self.ax.bar(x_locations - bar_width/6, self.data['partially_completed_workouts'], width=bar_width/3,color='Yellow',label='Partially Completed')
        self.ax.bar(x_locations + bar_width/6, self.data['missed_workouts'], width=bar_width/3,color='Red',label='Missed')
        self.ax.legend()
        
        self.finalize_graph('Weekly Consistency', 'Week', 'Number of Workouts')
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
