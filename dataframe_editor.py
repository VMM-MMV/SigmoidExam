import pandas as pd

missing_rows = pd.read_csv("MissingRows.csv")

for index, row in missing_rows.iterrows():
    name = row['Name'] 
    year = row['Year_of_Release']
    publisher = row['Publisher']

    print(f'name = {name}, publishing year = {year}, publisher = {publisher}')