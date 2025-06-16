from src.input_module import find_cell
from src.Workout import Workout
class Training_day:
    def __init__(self, date, df, ws, wb):
        self.ws = ws
        self.wb = wb
        self.date = date
        self.df = df
        self.load_cycle_block = find_cell(self.ws, self.df, 'Load Cycle', self.date).value
        self.day = find_cell(self.ws, self.df, 'Day', self.date).value
        self.initialize_workouts()

    #initialize each workout object 
    def initialize_workouts(self):
        workout_columns = ['Workout 1', 'Sets W1', 'Reps W1', 'Weight W1','RPE W1',
                           'Workout 2', 'Sets W2', 'Reps W2', 'Weight W2', 'RPE W2',
                           'Workout 3', 'Sets W3', 'Reps W3', 'Weight W3', 'RPE W3']
        self.workouts = [Workout() for _ in range(3)]
        # instantiate each workout object with the corresponding data from the Excel sheet
        for i in range(0, len(workout_columns), 5):
            name = find_cell(self.ws, self.df, workout_columns[i], self.date).value
            sets = find_cell(self.ws, self.df, workout_columns[i+1], self.date).value
            reps = find_cell(self.ws, self.df, workout_columns[i+2], self.date).value
            weight = find_cell(self.ws, self.df, workout_columns[i+3], self.date).value
            RPE = find_cell(self.ws, self.df, workout_columns[i+4], self.date).value
            self.workouts[i//5] = Workout(self.day, name, sets, reps, weight, RPE, self.load_cycle_block, self.wb, self.df)

    def load_cycle_info(self):
        block_descriptions = {
            1: "buildup block of your current load cycle. Focus will be on reloading with moderate to high weight and moderate reps.",
            2: "power block of your current load cycle. Focus will be on building power with lower reps and higher weights.",
            3: "strength block of your current load cycle. Focus will be on building strength with moderate reps and weights.",
            4: "deload block of your current load cycle. Focus will be on recovery with reduced intensity and volume."
        }
        return f"You're in the {block_descriptions[int(self.load_cycle_block)]}"
       
       
        

    #TODO: add graphical representations        
    def display_workout_info(self):
        self.display_climbing_type()

        # Give info about the current point in the load cycle
        print(self.load_cycle_info())
        
        # Display each workout's recommendation
        for workout in self.workouts:
            print(workout.recommend_next_workout())

    def display_climbing_type(self):
        climbing_workout_type = str(find_cell(self.ws, self.df, 'Type', self.date).value).lower()
        if climbing_workout_type == 'Rest':
            print(f"Today is a rest day. Only leg workouts.")
        else:
            print(f"Today is a {climbing_workout_type} climbing day.")
        