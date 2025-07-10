import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Pipeline: Use dataframe -> create new dataframes with data needed for each graph -> create graphs with the new dataframes

def graph_maker(df, date, wb):
    # Prepare data for graphs
    graph_data = prepare_graph_data(df, date, wb)
    
    graph_paths = ['load_trend.png', '1RM_progression.png', 'actual_RPE_vs_target.png', 'weekly_consistency.png', 'load_cycle_summary.png']

    graphs = create_graphs(graph_data, graph_paths, date)
    
    plot_graphs(graphs)


    save_graphs(graph_paths,'/Users/cole/Desktop/ClimbingWorkoutAnalyzer/src/graphs')


# TODO: Save graphs to specified output path
def save_graphs(graph_paths, output_path):
    pass

# Instantiate graph objects and call their methods to plot and save graphs
def create_graphs(graph_data,graph_paths,date):
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

    return graphs

def plot_graphs(graphs):
    for graph in graphs:
        graph.plot_graph()

# TODO: Transform base dataframe into data needed for each graph
def prepare_graph_data(df, date, wb):
    #add logic to prepare data for each graph
    g1 = load_trend_data(df, date, wb)
    
    return {
        'load_trend': g1,
        '1RM_progression': g2,
        'actual_RPE_vs_target': g3,
        'weekly_consistency': g4,
        'load_cycle_summary': g5
    }

def load_trend_data(df, date, wb):
# Actual load: 
    # get 1RM data for exercises on that day
        # get the type
    current_type = df[df['Date'] == date]['Type'].iloc[0]
        # find 1Rm for each exercise of the type of that day
    current_1RMs = get_1RMs(current_type, wb)
    # add a column in g1_data that contains the %1RM for each exercise
        # add logic to cut down dataframe based on type
        #  (type column is for type of climbing, but the exercises correspond so this is the easiest way to do it)
    g1_data = df[df['Type'] == current_type]


    # add a new column with actual load for each exercise
    # actual load = sets * reps * %1RM
    g1_data['Workout 1 Actual Load'] = g1_data['Sets W1'] * g1_data['Reps W1'] * (current_1RMs['Workout 1 1RM'] / 100)
    g1_data['Workout 2 Actual Load'] = g1_data['Sets W2'] * g1_data['Reps W2'] * (current_1RMs['Workout 2 1RM'] / 100)
    g1_data['Workout 3 Actual Load'] = g1_data['Sets W3'] * g1_data['Reps W3'] * (current_1RMs['Workout 3 1RM'] / 100)

    
    
#Expected load:
    # give each load cycle block value a respective load value
    # assign expected load values to each workout based on the load cycle block
    load_cycle_values = {
        # sets * reps * %1RM
        1: 3 * 5 * 0.65, # buildup
        2: 3 * 3 * 0.85, # power
        3: 3 * 5 * .7, # strength
        4: 2 * 5 * .6 # deload
    }
    # this line takes the values from 'load_cycles' and uses them as keys to get the corresponding values from load_cycle_values
    #  it then assigns those values to the new column 'Expected Load'
    # yay dictionaries!!
    g1_data['Workout 1 Expected Load'] = g1_data['Load Cycle'].map(load_cycle_values)
    g1_data['Workout 2 Expected Load'] = g1_data['Load Cycle'].map(load_cycle_values)
    g1_data['Workout 3 Expected Load'] = g1_data['Load Cycle'].map(load_cycle_values)
    
    g1_data = g1_data[['Day', 'Workout 1 Actual Load', 'Workout 2 Actual Load', 'Workout 3 Actual Load', 'Workout 1 Expected Load', 'Workout 2 Expected Load', 'Workout 3 Expected Load']]

    return g1_data
    
    # return df including the day, actual load, expected load
    

def get_1RMs(type, wb):
    benchmarks = wb[wb.sheetnames[1]]
    rows = list(benchmarks.iter_rows(min_row=2))
    # iterate by threes since the benchmarks are grouped by type
    for i in range(0, len(rows), 3):
        if rows[i][8].value == type: 
            #if type matches, get the other two 
            return {
                'Workout 1 1RM': rows[i][3].value,
                'Workout 2 1RM': rows[i+1][3].value,
                'Workout 3 1RM': rows[i+2][3].value,
            }