import pandas as pd

# Function to ask for a valid date from the user and check if it exists in the log
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
 