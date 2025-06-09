
# Allows user to input results for a given date and updates the corresponding Excel sheet.
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

# This function updates the specified cell in the Excel worksheet with the user's input.
def update_cell(ws,df, stat, date, result):
    row_index = df.index[df['Date'] == date].tolist()[0] + 2 # +2 to account for header and 0-indexing
    col_index = df.columns.get_loc(stat) + 1  # +1 because openpyxl is 1-indexed
    ws.cell(row=row_index, column=col_index).value = result
    