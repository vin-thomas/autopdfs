from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with


def getBSE100(url):
    driver = webdriver.Chrome()
    driver.get(url)
    code = []
    name = []
    market_cap = []
    # for i in range(2):
    # tbody = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_gvData"]/tbody')
    all_trs = driver.find_elements(By.XPATH, '//*[@id="ContentPlaceHolder1_gvData"]/tbody/tr')
    # print(tbody)
    # print(all_trs)
    # print(len(all_trs))
    for j in all_trs:
        # print(j.get_attribute('innerHTML'))
        print(j.get_attribute('outerHTML'))
        # code.append(j.find_element(By.XPATH, "//td[1]").text())
        name.append(j.find_element(By.XPATH, "//td[2]/a").get_attribute('innerHTML'))
        market_cap.append(j.find_element(By.XPATH, "//td[4]").get_attribute('innerHTML'))
    # driver.find_element(By.XPATH, "/html/body/form/div[4]/div/div/div[3]/div/div/table/tbody/tr[3]/td/table[2]/tbody/tr/td/div/img[3]").click()
# print(code[0], code[1])
# print(name[0], name[1])
# print(market_cap[0], market_cap[1])
    return [code, name, market_cap]
if __name__ == "__main__":
    getBSE100("https://www.bseindia.com/markets/equity/EQReports/TopMarketCapitalization.aspx")