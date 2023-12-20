from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
import time
import pandas as pd
import re
# Path to your WebDriver. Make sure you have the appropriate WebDriver downloaded.
# Here, I'm using Chrome WebDriver. Update the path accordingly if you're using a different browser.
# driver_path = '/path/to/your/chromedriver'

# Initialize Chrome WebDriver
driver = webdriver.Chrome()


def company_urls():
    df = pd.read_csv("Equity.csv")
    df = df[["Security Code", "Security Id", "Security Name"]]
    c = 0
    print(len(df))
    urls = []
    for i in df.iterrows():
        code = i[1][0]
        id = i[1][1].lower()
        # print(code)
        # print(id)
        # if i[1][2].lower()[-1] == ".":
        name = re.sub(r"[^\w\s]", "", i[1][2].lower())
        name = name.replace(" ","-")
        # print(name)
        urls.append(f'https://www.bseindia.com/stock-share-price/{name}/{id}/{code}/corp-announcements/')
    return urls

def get_pdf_links():
    urls = company_urls()
    c = 0
    for url in urls:
        if c < 10:
            try:
                # Open the webpage
                driver.get(url)
                time.sleep(5)  # Adjust this time according to the page load speed

                elems = driver.find_elements(By.XPATH, "//*[contains(text(), 'Earnings Call Transcript')]")
                for elem in elems:
                    print(elem.get_attribute('innerText'))
                    welem = driver.find_element(locate_with(By.TAG_NAME, 'a').to_right_of(elem))
                    print(welem.get_attribute('href'))


            except Exception as e:
                print("An error occurred:", e)
                continue
        c += 1
    driver.quit()

if __name__== "__main__":
    get_pdf_links()
