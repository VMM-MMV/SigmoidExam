from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

game_name = "Madden NFL 2004"

driver = webdriver.Chrome()
search_url = f"https://www.wikidata.org/w/index.php?go=Go&search={game_name}&ns0=1&ns120=1"
driver.get(search_url)

try:
    # Click on the first link in the search results
    first_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, game_name))
    )
    first_link.click()

    # Extract the publisher
    publisher_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#P123 .wikibase-snakview-value a"))
    )
    publisher = publisher_element.text

    # Extract the publication date
    date_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#P577 .wikibase-snakview-value"))
    )
    date = date_element.text

    print(f"Game: {game_name}")
    print(f"Publisher: {publisher}")
    print(f"Publication Date: {date}")

finally:
    driver.quit()
