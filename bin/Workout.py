#TODO: Fix problem in get_previous_weight 
#TODO: Add graphical representations
class Workout:   
    def __init__(self, day=None, name=None, sets=None, reps=None, weight=None, RPE=None, load_cycle=None, wb=None, df=None):
        self.day = day
        self.name = name
        self.sets = sets
        self.reps = reps
        self.weight = weight
        self.RPE = RPE 
        self.load_cycle = load_cycle
        self.wb = wb  
        self.df = df 
    
    def recommend_next_workout(self):
        one_RM = self.get_1RM(self.wb)
        prev_weight = self.get_previous_weight()
        if self.load_cycle == 1:
            sets = 3
            reps = 5  
            rpe = 6.5
            weight = prev_weight if prev_weight is not None else one_RM * 0.7
        elif self.load_cycle == 2:
            sets = 3  
            reps = 3  # I want more power focus
            rpe = 8.5 
            weight = prev_weight if prev_weight is not None else one_RM * 0.7
        elif self.load_cycle == 3:
            sets = 3
            reps = 5 
            rpe = 7.5 
            weight = prev_weight if prev_weight is not None else one_RM * 0.7
        elif self.load_cycle == 4:
            sets = 2 
            reps = 5 
            rpe = 5 
            weight = prev_weight if prev_weight is not None else one_RM * 0.7
        
        # return a string with the recommended workout details
        recommendation = f"Recommendation for {self.name}:\n" \
                            f"Sets: {sets}, Reps: {reps}, RPE: {rpe}, Weight: {weight} lbs"
        return recommendation

    def get_1RM(self, wb):
        benchmarks = wb[wb.sheetnames[1]]
        for row in benchmarks.iter_rows(min_row=2):
            if row[0].value == self.name: 
                return row[3].value # this is the 1RM value in the benchmarks sheet
    
    # Retrieves the weight from the previous workout in the same load cycle.
    #  gets the weight from that workout the most recent time the load cycle value was equal to the current load cycle value
    def get_previous_weight(self):
        current_day = self.day
        #TODO: Fix this to work with the excel sheet. Doesn't account for 3 workout columns.
        filtered_prev_workouts = self.df[ #create a new dataframe containing rows where: load cycle is equal to the current load cycle, day is less than the current day, workount name is equal to the current workout name
            (self.df['Load Cycle'] == self.load_cycle) &
            (self.df['Day'] < current_day) &
            (self.df['Workout 1'] or self.df['Workout 2'] or self.df['Workout 3']  == self.name)
        ]
        filtered_prev_workouts = filtered_prev_workouts.sort_values(by='Day', ascending=False)  # Sort by day in descending order so you can pop the most recent one off the top
        weight_column_index = filtered_prev_workouts.columns.get_loc(self.name) + 3 # this is bc each rows contains weights for each workout. prob should've structured my data differently...
        prev_weight = filtered_prev_workouts.iloc[0, weight_column_index] if not filtered_prev_workouts.empty else None

        return prev_weight
        #  weight column is 3 columns to the right of the workout name column
        
           
           
           
           
# 4 Week Training Block algorithm:
    # week 1,
        # sets: 3, 
        # reps 5-6, 
        # rpe 6-7
        # weight -> previous week 1 + 2.5 lbs, if no previous week 1, then 70-75% of 1RM
    # week 2
        # sets: 3, 
        # reps 3-5, 
        # rpe 8-9
        # weight -> previous week 2 + 2.5 lbs, if no previous week 2, then 80-90% of 1RM
    # week 3, 
        # sets: 3, 
        # reps 4-6, 
        # rpe 7-8
        # weight -> previous week31 + 2.5 lbs, if no previous week 3, then 70-80% of 1RM
    # week 4 (deload week)
        # sets: 1-2 
        # reps 5-6, 
        # rpe 5-6
        # weight -> 65% of 1RM