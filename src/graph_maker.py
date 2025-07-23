import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from src.graph_classes import LoadTrendGraph, MaxProgressionGraph, RPEvsTargetGraph, WeeklyConsistencyGraph, LoadCycleSummaryGraph

# Pipeline: Use dataframe -> create new dataframes with data needed for each graph -> create graphs with the new dataframes

def graph_maker(df, date, wb, benchmark_df):
    # Prepare data for graphs
    graph_data = prepare_graph_data(df, date, wb, benchmark_df)
    
    graph_paths = ['load_trend.png', '1RM_progression.png', 'actual_RPE_vs_target.png', 'weekly_consistency.png', 'load_cycle_summary.png']

    graphs = create_graphs(graph_data, graph_paths, date)
    
    plot_graphs(graphs)

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
    g3 = actual_RPE_vs_target_data(df, date, wb)
    g4 = get_weekly_consistency_data(df, date)
    g5 = get_load_cycle_summary_data(df, date)
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
    current_type = get_current_type(df, date)
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
    # find previous benchmark 1RMs for each exercise
    g2_data = benchmark_df[['Workout','Estimated 1RM']]
    g2_data = g2_data.rename(columns={'Estimated 1RM': 'Previous 1RM'})
    current_day = df[df['Date'] == date]['Day'].iloc[0]
    current_1RMs = {}

    # make sure we are deriving 1rms from completed workouts
    completed_df = df[df['Day'] <= current_day].sort_values('Day', ascending=False)
    mask = (
        ((completed_df['Sets W1'] > 0) & (completed_df['Reps W1'] > 0) & (completed_df['Weight W1'] > 0)) &
        ((completed_df['Sets W2'] > 0) & (completed_df['Reps W2'] > 0) & (completed_df['Weight W2'] > 0)) &
        ((completed_df['Sets W3'] > 0) & (completed_df['Reps W3'] > 0) & (completed_df['Weight W3'] > 0))
    )
    completed_df = completed_df[mask]
    # 
    for day in completed_df['Day'].head(3):   
        # get the workout name, weight, and reps for each exercise
        row= completed_df[completed_df['Day'] == day].iloc[0]
        for i in range(1,4):    
            workout_name = row[f'Workout {i}']
            weight = row[f'Weighjt {i}']
            reps = row[f'Reps {i}']
            current_1RM = weight / (1.0278 - (0.0278 * reps)) # apply formula
            # add to dict
            current_1RMs[workout_name] = current_1RM
    # add a new column to g2_data with the current 1RMs
    g2_data['Current 1RM'] = g2_data['Workout'].map(current_1RMs)

    return g2_data

def actual_RPE_vs_target_data(df, date, wb):
    # sort actual vs target RPE for each workout
    current_type = get_current_type(df, date)
    g3_data = df[df['Type'] == current_type][['Day', 'Workout 1', 'Workout 2', 'Workout 3','RPE W1', 'RPE W2', 'RPE W3', 'Load Cycle']]
    g3_data = g3_data.rename(columns={
        'RPE W1': 'Actual RPE W1',
        'RPE W2': 'Actual RPE W2',
        'RPE W3': 'Actual RPE W3',
        # this just renames the columns to the actual names of the workouts on those days
        #  this will be used in the legend
        'Workout 1': g3_data[g3_data['Day'] == date]['Workout 1'].iloc[0],
        'Workout 2': g3_data[g3_data['Day'] == date]['Workout 2'].iloc[0],
        'Workout 3': g3_data[g3_data['Day'] == date]['Workout 3'].iloc[0]
    })
    load_cycle_RPE_expected = {
        1: 7,
        2: 9,
        3: 8,
        4: 6
    }
    g3_data['Expected RPE W1']= g3_data['Load Cycle'].map(load_cycle_RPE_expected)
    g3_data['Expected RPE W2']= g3_data['Load Cycle'].map(load_cycle_RPE_expected)
    g3_data['Expected RPE W3']= g3_data['Load Cycle'].map(load_cycle_RPE_expected)

    return g3_data

# count up weekly number of partially, missed, completed per week
def get_weekly_consistency_data(df, date):
    counted_columns = ['Sets W1', 'Reps W1', 'Weight W1',
                       'Sets W2', 'Reps W2', 'Weight W2',
                       'Sets W3', 'Reps W3', 'Weight W3']
    # clean up the data a bit
    g4_data = df[counted_columns + ['Week', 'Date']].copy()
    g4_data = g4_data[g4_data['Date'] <= date]
    g4_data[counted_columns] = g4_data[counted_columns].fillna(0)  # replace NaN with 0 for easier counting
   
    # create columns for missed, partially completed, and completed workouts
    #  evaluate for each row
    g4_data['missed_workouts'] = g4_data[counted_columns].eq(0).all(axis=1)
    g4_data['partially_completed_workouts'] = g4_data[counted_columns].eq(0).any(axis=1)
    g4_data['completed_workouts'] = g4_data[counted_columns].ne(0).all(axis=1)
    
    # then just group by week and sum the columns
    g4_data = g4_data[['Week', 'missed_workouts', 'partially_completed_workouts', 'completed_workouts']].groupby('Week').sum().reset_index()

    return g4_data
    
def get_load_cycle_summary_data(df, date):
    # I will get the specific day to show on the graph inside the graph class, i just need the two columns
    load_cycle_data = df[['Date', 'Load_Cycle']]
    return load_cycle_data

def get_current_type(df, date):
    return df[df['Date'] == date]['Type'].iloc[0]