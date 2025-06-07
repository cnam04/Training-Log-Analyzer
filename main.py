import pandas as pd
from openpyxl import load_workbook # Using openpyxl to preserve the formatting and fomulas 

file_path = '/Users/cole/Documents/OneDrive - State University of New York at New Paltz/Climbing Training Log Summer.xlsx'
def main():
    df = pd.read_excel(file_path)
    wb = load_workbook(file_path)
    ws = wb["Plan"]

    current_date = ask_for_date(df)

#   give_workout_info(date, df)
   
    input_results(df, current_date, ws, wb)
    
#   generate_report(df)
    
    wb.save(file_path)
    wb.close()

def input_results(df, date, ws, wb):
    sets_reps_rpe = ['Sets W1', 'Reps W1', 'Weight W1','RPE W1', 'Sets W2', 'Reps W2', 'Weight W2', 'RPE W2', 'Sets W3', 'Reps W3', 'Weight W3', 'RPE W3', 'Stretch?', 'Warmup?']
    for stat in sets_reps_rpe:
        # Only allow y or n for Warmup and Stretch
        if stat in ('Warmup?','Stretch?'):
            result = input(f"Did you {stat} (y/n)? (press enter to skip):")
            while result not in ('y', 'n', ''):
                result = input(f"Did you {stat} (y/n)? (press enter to skip):")
        else:
            result = input(f"Please enter your {stat} for {date} (or press enter to skip): ")
        update_cell(ws,df, stat, date, result)
    
def update_cell(ws,df, stat, date, result):
    row_index = df.index[df['Date'] == date].tolist()[0] + 2 # +2 to account for header and 0-indexing
    col_index = df.columns.get_loc(stat) + 1  # +1 because openpyxl is 1-indexed
    ws.cell(row=row_index, column=col_index).value = result
    
def ask_for_date(df):
    date = input("Please enter today's date (MM-DD-YYYY): ")
    #check for invalid date format or if date is not in the log
    try:
        pd.to_datetime(date)
        date = pd.to_datetime(date) 
        
        matches = df.index[df['Date'] == date].tolist()
        if not matches:
            print(f"No entry found for {date}. Please make sure the date is in the log.")
            return ask_for_date(df)
        
        return date
    except ValueError:
        print("Invalid date format. Please use MM-DD-YYYY.")
        return ask_for_date(df)
        

if __name__ == "__main__":
    main()