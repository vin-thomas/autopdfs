from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
import time

# Path to your WebDriver. Make sure you have the appropriate WebDriver downloaded.
# Here, I'm using Chrome WebDriver. Update the path accordingly if you're using a different browser.
driver_path = '/path/to/your/chromedriver'

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

# URL to navigate
url = 'https://www.bseindia.com/stock-share-price/ltimindtree-ltd/ltim/540005/corp-announcements/'

try:
    # Open the webpage
    driver.get(url)
    time.sleep(5)  # Adjust this time according to the page load speed

    # Perform Ctrl + F and search for the phrase
    # search_phrase = "Earnings Call Transcript"
    # body = driver.find_element(By.TAG_NAME, "body")
    # body.send_keys(Keys.CONTROL + 'f')  # Opens the browser's find box
    

    elem = driver.find_element(By.XPATH, "//*[contains(text(), 'Earnings Call Transcript')]")
    print(elem.get_attribute('innerText'))

    welem = driver.find_element(locate_with(By.TAG_NAME, 'a').to_right_of(elem))
    print(welem.get_attribute('href'))

    # Type the search phrase in the find box
    # time.sleep(1)  # Adding a delay for the find box to open
    # body.send_keys(search_phrase)
    # time.sleep(2)  # Adjust this time according to the search speed

    # Close the browser
    driver.quit()

except Exception as e:
    print("An error occurred:", e)
    driver.quit()
