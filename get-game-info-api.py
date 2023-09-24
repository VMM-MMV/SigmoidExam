import requests
import json
from datetime import datetime
import pandas as pd

with open('config.json', 'r') as f:
    config = json.load(f)

client_id = config.get('IGDB_CLIENT_ID')
access_token = config.get('IGDB_ACCESS_TOKEN')
headers = {
    "Client-ID": client_id,
    "Authorization": f"Bearer {access_token}"
}


def get_game_info(game_name):
    url = "https://api.igdb.com/v4/games"
    body = f"""
    fields first_release_date, involved_companies;
    where name ~ "{game_name}"*;
    limit 1;
    """
    response = requests.post(url, headers=headers, data=body)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve information for {game_name}. Status Code:", response.status_code)
        print("Response Text:", response.text)
        return None


def get_involved_companies_info(involved_companies_ids):
    url = "https://api.igdb.com/v4/involved_companies"
    body = f"""
    fields company,developer,publisher;
    where id = ({','.join(map(str, involved_companies_ids))});
    """
    response = requests.post(url, headers=headers, data=body)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve information for involved companies. Status Code:", response.status_code)
        print("Response Text:", response.text)
        return None


def get_companies_info(company_ids):
    url = "https://api.igdb.com/v4/companies"
    body = f"""
    fields name,slug,description;
    where id = ({','.join(map(str, company_ids))});
    """
    response = requests.post(url, headers=headers, data=body)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve information for companies. Status Code:", response.status_code)
        print("Response Text:", response.text)
        return None


# Get game information
game_name = "Madden NFL 2004"
def get_info(game_name):
    info = {}
    game_info = get_game_info(game_name)
    print(game_info)
    if game_info:
        release_date = game_info[0].get('first_release_date', [])
        print(release_date)
        if release_date:
            year_of_release = datetime.utcfromtimestamp(release_date).strftime('%Y')
            info["Year_of_Release"] = int(year_of_release)

        involved_companies_ids = game_info[0].get('involved_companies', [])
        involved_companies_info = get_involved_companies_info(involved_companies_ids)
        if involved_companies_info:
            for i in involved_companies_info:
                print(i)
            publisher_or_developer = [company_info['publisher'] for company_info in involved_companies_info]
            company_ids = [company_info['company'] for company_info in involved_companies_info]
            
            company_info = get_companies_info(company_ids)
            print(publisher_or_developer)
            print()
            # print(company_info)
            for i in company_info:
                print(i["id"], i["name"])
            print()
            for i in company_info:
                    index = company_ids.index(i["id"])
            
                    if publisher_or_developer[index] == True:
                        info["Publisher"] = i["name"]
                    if publisher_or_developer[index] == False:
                        info["Developer"] = i["name"]
    return info
            
        
# print(get_info(game_name))


missing_rows = pd.read_csv("MissingRows.csv")

for index, row in missing_rows.iterrows():
    print()
    print(index/len(missing_rows)*100, "%")
    name = row['Name'] 
    year = row['Year_of_Release']
    publisher = row['Publisher']

    print(f'name = {name}, publishing year = {year}, publisher = {publisher}')
    
    if pd.isna(year) or pd.isna(publisher):
        info = get_info(name)
        print(info)
        print()
        if 'Year_of_Release' in info and pd.isna(year):
            missing_rows.at[index, 'Year_of_Release'] = int(info['Year_of_Release'])
        if 'Publisher' in info and pd.isna(publisher):
            missing_rows.at[index, 'Publisher'] = str(info['Publisher'])

print(missing_rows)

missing_rows.to_csv('FilledRows.csv')