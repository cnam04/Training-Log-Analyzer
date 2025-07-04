import matplotlib.pyplot as plt
import numpy as np

# Pipeline: Use dataframe -> create new dataframes with data needed for each graph -> create graphs with the new dataframes

def graph_maker(df, date):
    # Prepare data for graphs
    graph_data = prepare_graph_data(df, date)
    
    graph_paths = ['load_trend.png', '1RM_progression.png', 'actual_RPE_vs_target.png', 'weekly_consistency.png', 'load_cycle_summary.png']

    # Create graphs
    display_graphs(graph_data, graph_paths, date)
    
    #save graphs
    save_graphs(graph_paths,'/Users/cole/Desktop/ClimbingWorkoutAnalyzer/src/graphs')


# Save graphs to specified output path
def save_graphs(graph_paths, output_path):
    pass

# Instantiate graph objects and call their methods to plot and save graphs
def display_graphs(graph_data,graph_paths,date):
    graph_classes = [
        (LoadTrendGraph, 'load_trend'),
        (MaxProgressionGraph, '1RM_progression'),
        (RPEvsTargetGraph, 'actual_RPE_vs_target'),
        (WeeklyConsistencyGraph, 'weekly_consistency'),
        (LoadCycleSummaryGraph, 'load_cycle_summary')
    ]
    # Dynamically create graph objects
    graphs = [
        cls(graph_data[key], graph_paths[i], date) 
        for i, (cls, key) in enumerate(graph_classes) # iterates through graph_classes, keeps track of index using i, unpacks the graph_classes tuple
    ]

    for graph in graphs:
        graph.plot_graph()

# Transform base dataframe into data needed for each graph
def prepare_graph_data(df, date):
    #add logic to prepare data for each graph

    
    return {
        'load_trend': g1,
        '1RM_progression': g2,
        'actual_RPE_vs_target': g3,
        'weekly_consistency': g4,
        'load_cycle_summary': g5
    }
