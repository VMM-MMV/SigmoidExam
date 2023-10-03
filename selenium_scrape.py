from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np


# driver = webdriver.Chrome()

def find_info(game_name, driver):    
    info = {}
    try:
        # Open the search URL
        search_url = f"https://www.wikidata.org/w/index.php?go=Go&search={game_name}&ns0=1&ns120=1"
        driver.get(search_url)

        try:
            # Click on the first link in the search results under the "mw-search-results-container" div
            first_link = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.mw-search-results-container a"))
            )
            first_link.click()

            # Extract the publication date
            date_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#P577 .wikibase-snakview-variation-valuesnak"))
            )
            info['Year_of_Release'] = date_element.text.split(' ')[-1]  # Extracting the year from the date

            # Extract the publisher
            publisher_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#P123 .wikibase-snakview-variation-valuesnak a"))
            )
            info['Publisher'] = publisher_element.text


        except Exception as e:
            print(f"Could not retrieve information for {game_name}")
            print(f"Error: {e}")
            print("===================================")

    finally:
        pass

    return info


if __name__ == "__main__":
    games = [
        "Madden NFL 2004",
        "FIFA Soccer 2004",
        "LEGO Batman: The Videogame",
        "wwe Smackdown vs. Raw 2006",
        "Space Invaders",
        "Rock Band"
    ]

    for game in games:
        find_info(game)

    # driver.quit()