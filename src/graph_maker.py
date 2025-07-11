import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Pipeline: Use dataframe -> create new dataframes with data needed for each graph -> create graphs with the new dataframes

def graph_maker(df, date, wb, benchmark_df):
    # Prepare data for graphs
    graph_data = prepare_graph_data(df, date, wb, benchmark_df)
    
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
def prepare_graph_data(df, date, wb, benchmark_df):
    #add logic to prepare data for each graph
    g1 = load_trend_data(df, date, wb)
    g2 = max_progression_data(df, date, wb, benchmark_df)
    
    return {
        'load_trend': g1,
        '1RM_progression': g2,
        'actual_RPE_vs_target': g3,
        'weekly_consistency': g4,
        'load_cycle_summary': g5
    }

def load_trend_data(df, date, wb, benchmark_df):
# Actual load: 
    # get 1RM data for exercises on that day
        # get the type
    current_type = df[df['Date'] == date]['Type'].iloc[0]
    # add a column in g1_data that contains the %1RM for each exercise
        # add logic to cut down dataframe based on type
        #  (type column is for type of climbing, but the exercises correspond so this is the easiest way to do it)
    g1_data = df[df['Type'] == current_type]
    

    # add a new column with actual load for each exercise
    # actual load = sets * reps * %1RM
    #%1RM = Weight / 1RM * 100
    g1_data['Workout 1 Actual Load'] = g1_data['Sets W1'] * g1_data['Reps W1'] * (g1_data['Weight W1'] / benchmark_df[benchmark_df['Type'] == current_type].iloc[0][3] * 100)
    g1_data['Workout 2 Actual Load'] = g1_data['Sets W2'] * g1_data['Reps W2'] * (g1_data['Weight W2'] / benchmark_df[benchmark_df['Type'] == current_type].iloc[1][3] * 100)
    g1_data['Workout 3 Actual Load'] = g1_data['Sets W3'] * g1_data['Reps W3'] * (g1_data['Weight W3'] / benchmark_df[benchmark_df['Type'] == current_type].iloc[2][3] * 100)

    
    
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

def max_progression_data(df, date, wb, benchmark_df):
    # TODO: find a way to get all 9
    # find previous benchmark 1RMs for each exercise
    g2_data = benchmark_df[['Workout','Estimated 1RM']]
    g2_data = g2_data.rename(columns={'Estimated 1RM': 'Previous 1RM'})
    # find current 1RMs for each exercise using estimated 1RM formula
    current_day = df[df['Date'] == date]['Day'].iloc[0]
    # 1RM = Weight / (1.0278 - (0.0278 * Repetitions))
    current_1RMs = {}
    for i in range(0, 3): #iterate through current -> prev 2 days
        # collect the data in an array of touples
        for j in range (1, 4):
            try:
                # get the workout name, weight, and reps for each exercise
                workout_name = df[df['Day'] == current_day - i]['Workout ' + str(j)].iloc[0]
                weight = df[df['Day'] == current_day - i]['Weight ' + str(j)].iloc[0]
                reps = df[df['Day'] == current_day - i]['Reps ' + str(j)].iloc[0]
            except (IndexError, KeyError):# Handle the case where the day or workout does not exist
                print(f"Data for Day {current_day - i} or Workout {j} is missing.")
                continue
            # apply formula to each exercise for most recent workout
            current_1RM = weight / (1.0278 - (0.0278 * reps))
            # add to dict
            current_1RMs[workout_name] = current_1RM
    # add a new column to g2_data with the current 1RMs
    g2_data['Current 1RM'] = g2_data['Workout'].map(current_1RMs)

    return g2_data

    

