import pandas as pd
from selenium_scrape import *

driver = webdriver.Chrome()

missing_rows = pd.read_csv("MissingRows.csv")

for index, row in missing_rows.iterrows():
    name = row['Name'] 
    year = row['Year_of_Release']
    publisher = row['Publisher']

    print(f'name = {name}, publishing year = {year}, publisher = {publisher}')
    
    if pd.isna(year) or pd.isna(publisher):
        info = find_info(name + " video game", driver)
        print(info)
        print()
        if 'Year_of_Release' in info and pd.isna(year):
            missing_rows.at[index, 'Year_of_Release'] = int(info['Year_of_Release'])
        if 'Publisher' in info and pd.isna(publisher):
            missing_rows.at[index, 'Publisher'] = str(info['Publisher'])

print(missing_rows)

missing_rows.to_csv('FilledRows.csv')

driver.quit()