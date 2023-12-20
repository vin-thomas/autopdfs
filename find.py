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


def bse_urls():
    df = pd.read_csv("Equity.csv")
    df = df[["Security Code", "Security Id", "Security Name"]]
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


def screener_urls():
    df = pd.read_csv("Equity.csv")
    df = df["Security Id"]
    urls = []
    for i in df.tolist():
        urls.append(f'https://www.screener.in/company/{i}/')
    return urls


def order_urls(urls, ch):
    df = pd.read_csv('ind_nifty50list.csv')
    df = df['Symbol']
    df = df.sort_values(ascending=False)        
    for i in range(len(urls)):
        for sym in df.tolist():
            if ch == 1:
                if urls[i].split('/')[-4].upper() == sym:
                    urls.insert(0, urls.pop(i))
            elif ch == 2:
                if urls[i].split('/')[-2] == sym:
                    urls.insert(0, urls.pop(i))
    return urls


def from_bse(urls):
    id = []
    pdf_list = []
    c = 0
    for url in urls:
        if c < 50:
            try:
                # Open the webpage
                driver.get(url)
                time.sleep(2)  # Adjust this time according to the page load speed

                elems = driver.find_elements(By.XPATH, "//*[contains(text(), 'Earnings Call Transcript')]")
                href = []
                for elem in elems:
                    print(elem.get_attribute('innerText'))
                    welem = driver.find_element(locate_with(By.TAG_NAME, 'a').to_right_of(elem))
                    href.append(welem.get_attribute('href') )
                    print(href)
                id.append(url.split('/')[-4].upper())
                pdf_list.append(href)

            except Exception as e:
                print("An error occurred:", e)
                continue
        c += 1
    driver.quit()
    return id, pdf_list


def from_screener(urls):
    id = []
    pdf_list = []
    c = 0
    for url in urls:
        if c < 50:
            try:
                # Open the webpage
                driver.get(url)
                time.sleep(2)  # Adjust this time according to the page load speed

                elems = driver.find_elements(By.XPATH, "//a[contains(@class, 'concall-link') and contains(text(), 'Transcript')]")
                href = []
                for elem in elems:
                    print(elem.get_attribute('innerText'))
                    href.append(elem.get_attribute('href'))
                print(href)
                id.append(url.split('/')[-2].upper())
                pdf_list.append(href)

            except Exception as e:
                print("An error occurred:", e)
                continue
        c += 1
    driver.quit()
    return id, pdf_list


def get_pdf_links():
    # urlsb = order_urls(bse_urls(), 1)
    # id, pdf_list = from_bse(urlsb)

    # df = pd.DataFrame()
    # df['id'] = id
    # df["pdfs"] = pdf_list
    # df.to_csv("pdf_list.csv", index=False)


    urlss = order_urls(screener_urls(), 2)
    sid, spdf_list = from_screener(urlss)

    sdf = pd.DataFrame()
    sdf['id'] = sid
    sdf["pdfs"] = spdf_list
    sdf.to_csv("spdf_list.csv", index=False)

    

if __name__ == "__main__":
    get_pdf_links()
