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

    elems = driver.find_elements(By.XPATH, "//*[contains(text(), 'Earnings Call Transcript')]")
    for elem in elems:
        print(elem.get_attribute('innerText'))
        welem = driver.find_element(locate_with(By.TAG_NAME, 'a').to_right_of(elem))
        print(welem.get_attribute('href'))

    driver.quit()

except Exception as e:
    print("An error occurred:", e)
    driver.quit()
