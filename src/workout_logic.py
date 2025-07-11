from src.Training_day import Training_day
def give_workout_info(date, df, ws, wb, benchmark_df):
    # Gives info about where the user is in their training cycle gives a plan for 
        current_workout_day = Training_day(date, df, ws, wb, benchmark_df)
        current_workout_day.display_workout_info()