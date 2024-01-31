from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
import os, time
import pandas as pd
import re
import threading
import google.generativeai as genai
# Path to your WebDriver. Make sure you have the appropriate WebDriver downloaded.
# Here, I'm using Chrome WebDriver. Update the path accordingly if you're using a different browser.
# driver_path = '/path/to/your/chromedriver'




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
    df = pd.read_csv('ind_nifty100list.csv')
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


def from_bse(urls, id = [], pdf_list = []):
    driver = webdriver.Chrome()
    print("bse here")
    c = 0
    for url in urls:
        if c < 3:
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
    df = pd.DataFrame()
    df['id'] = id
    df["pdfs"] = pdf_list
    df.to_csv("pdf_list.csv", index=False)
    # return id, pdf_list


def from_screener(urls, id = [], pdf_list = []):
    driver = webdriver.Chrome()
    print("screener here")
    c = 0
    for url in urls:
        if c < 3:
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
    df = pd.DataFrame()
    df['id'] = id
    df["pdfs"] = pdf_list
    df.to_csv("spdf_list.csv", index=False)
    # return id, pdf_list


def get_pdf_links():
    urlsb = order_urls(bse_urls(), 1)
    urlss = order_urls(screener_urls(), 2)
    
    print(type(urlsb))
    
    # id, pdf_list = []
    bse_thread = threading.Thread(target=from_bse, args=([urlsb]))
    # sid, spdf_list = []
    screener_thread = threading.Thread(target=from_screener, args=([urlss]))

    bse_thread.start()
    screener_thread.start()


    bse_thread.join()
    print("completed bse")
    # df = pd.DataFrame()
    # df['id'] = id
    # df["pdfs"] = pdf_list
    # df.to_csv("pdf_list.csv", index=False)

    screener_thread.join()
    print("completed screener")
    # sdf = pd.DataFrame()
    # sdf['id'] = sid
    # sdf["pdfs"] = spdf_list
    # sdf.to_csv("spdf_list.csv", index=False)


def combine_check():
    df = pd.read_csv('pdf_list.csv')
    sdf = pd.read_csv('spdf_list.csv')
    fdf = pd.DataFrame()
    id = []
    pdfs = []
    for i in range(len(df)):
        for j in range(len(sdf)):
            if df['id'][i] == sdf['id'][j]:
                id.append(df["id"][i])
                ls1 = eval(df['pdfs'][i])
                ls2 = eval(sdf['pdfs'][j])
                if ls1 == [] or ls2 == []:
                    if ls1 != [] and ls2 == []:
                        pdfs.append(ls1)
                    elif ls2 != [] and ls1 == []:
                        pdfs.append(ls2)
                    else:
                        pdfs.append([])
                else:
                    tmp = []
                    indices = []
                    for x, k in enumerate(ls1):
                        for y, m in enumerate(ls2):
                            srch = re.findall(r"Pname=([\w.-]*)", m)[0] if re.findall(r"Pname=([\w.-]*)", m) != [] else ''
                            if k.split('/')[-1] == srch:
                                tmp.append(k)
                                indices.append(y)
                    for i in indices:
                        for l,j in enumerate(ls2):
                            if i == l:
                              continue
                            else:
                              tmp.append(j)
                    pdfs.append(tmp)
    fdf["id"] = id
    fdf["pdfs"] = pdfs
    fdf.to_csv('final_pdfs.csv')

import requests
import re
import pdftotext

def text_extraction(path):
  with open(path, "rb") as f:
      pdf = pdftotext.PDF(f)
  text = []
  # All pages
  for txt in pdf:
    text.append(txt)
  return text

def filemk(furl):
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
  res = requests.get(furl, headers=headers)
  with open("transcript.pdf", "wb+") as pdf:
    pdf.write(res.content)
    pdf.close()
  texts = text_extraction("transcript.pdf")
  infostr = ''.join(texts[0:2])
  return infostr


'''
def add_yq():
    genai.configure(api_key=GOOGLE_API_KEY)

    df = pd.read_csv('final_pdfs.csv')
    pdfs = []
    for i in range(len(df)):
        pdfs.append(eval(df['pdfs'][i]))
    df['pdfs'] = pdfs

'''
            
if __name__ == "__main__":
    get_pdf_links()
    combine_check()
    # add_yq()