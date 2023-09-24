import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import quote

def find_info(name):
    url = f"https://www.gamesdatabase.org/list.aspx?in=1&searchtext={quote(name)}&searchtype=1"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    tr_tags = soup.find_all('tr', align='left')
    if tr_tags:
        tr_tags = tr_tags[1]
        info = {}
        td_tags = tr_tags.find_all('td')
            
        needed_info = []
        for i in td_tags:
            if i.get_text(strip=True):
                needed_info.append(i.get_text(strip=True))

        if len(needed_info) == 6:
            info["Publisher"] = needed_info[2]
            info["Developer"] = needed_info[3]
            info["Year_of_Release"] = needed_info[5]
        else:
            return {}
    else:
        return {}
    
    return info


missing_rows = pd.read_csv("MissingRows.csv")

for index, row in missing_rows.iterrows():
    name = row['Name'] 
    year = row['Year_of_Release']
    publisher = row['Publisher']

    print(f'name = {name}, publishing year = {year}, publisher = {publisher}')
    
    if pd.isna(year) or pd.isna(publisher):
        info = find_info(name)
        print(info)
        print()
        if 'Year_of_Release' in info and pd.isna(year):
            missing_rows.at[index, 'Year_of_Release'] = int(info['Year_of_Release'])
        if 'Publisher' in info and pd.isna(publisher):
            missing_rows.at[index, 'Publisher'] = str(info['Publisher'])
        if 'Developer' in info and pd.isna(row['Developer']):  # Assuming you have a Developer column in your DataFrame
            missing_rows.at[index, 'Developer'] = str(info['Developer'])

missing_rows.to_csv('SomeRepairedRows.csv', index=False)