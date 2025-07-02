from abc import ABC, abstractmethod # abc = abstract base class
import matplotlib.pyplot as plt
import numpy as np

# Base class that contains common functionality for all graph types
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
        self.fig.savefig(self.path)
        plt.close(self.fig)

class WeeklyLoadTrendGraph(BaseGraph):
    
class MaxProgressionGraph(BaseGraph):

class RPEvsTargetGraph(BaseGraph):

class WeeklyConsistencyGraph(BaseGraph):

class LoadCycleSummaryGraph(BaseGraph):
