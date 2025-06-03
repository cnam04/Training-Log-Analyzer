import pandas as pd

def main():
    file_path = '/Users/cole/Downloads/Climbing Training Log Summer.csv'
    df = pd.read_csv(file_path)
    print(df.head())
    print("done")
if __name__ == "__main__":
    main()