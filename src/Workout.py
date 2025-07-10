
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
            rpe = 7
            weight = (prev_weight +2.5) if prev_weight is not None else round(one_RM * 0.65)
        elif self.load_cycle == 2:
            sets = 3  
            reps = 3  # I want more power focus
            rpe = 9 
            weight = (prev_weight+2.5) if prev_weight is not None else round(one_RM * 0.85)
        elif self.load_cycle == 3:
            sets = 3
            reps = 5 
            rpe = 8 
            weight = (prev_weight +2.5) if prev_weight is not None else round(one_RM * 0.7)
        elif self.load_cycle == 4:
            sets = 2 
            reps = 5 
            rpe = 5 
            weight = prev_weight if prev_weight is not None else round(one_RM * 0.6)
        
        # return a string with the recommended workout details
        recommendation = f"Recommendation for {self.name}:\n" \
                            f"Sets: {sets}, Reps: {reps}, RPE: {rpe}, Weight: {weight} lbs"
        return recommendation

    def get_1RM(self, wb):
        benchmarks = wb[wb.sheetnames[1]]
        for row in benchmarks.iter_rows(min_row=2):
            if row[0].value.strip() == self.name.strip(): 
                return row[3].value # this is the 1RM value in the benchmarks sheet
    
    # Retrieves the weight from the previous workout in the same load cycle.
    #  gets the weight from that workout the most recent time the load cycle value was equal to the current load cycle value
    def get_previous_weight(self, day=None):
        current_day = day if day is not None else self.day
        workout_cols = ['Workout 1', 'Workout 2', 'Workout 3']
        weight_cols = ['Weight W1', 'Weight W2', 'Weight W3']
        rpe_cols = ['RPE W1', 'RPE W2', 'RPE W3']
        
        filtered_prev_workouts = self.df[ # Create a filtered DataFrame with all previous workouts of the same type in the same load cycle
            (self.df['Load Cycle'] == self.load_cycle) &
            (self.df['Day'] < current_day) &
            (self.df[workout_cols].eq(self.name).any(axis=1))
        ].sort_values(by='Day', ascending=False)
        
        if filtered_prev_workouts.empty:
            return None
        
        most_recent_row = filtered_prev_workouts.iloc[0]
        for i, col in enumerate(workout_cols): # find the most recent workout
            if most_recent_row[col] == self.name:
                # If a workout was skipped, find the next most recent workout
                if most_recent_row[weight_cols[i]] == 0:
                    return self.get_previous_weight(day=most_recent_row['Day'])
                else:
                    if rpe_cols[i] >= 9:
                        return most_recent_row[weight_cols[i]] -2.5 # If the RPE is 9 or higher, reduce the weight by 2.5 lbs since its too heavy
                    else:
                        return most_recent_row[weight_cols[i]]
        return None

           
           
           
           
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