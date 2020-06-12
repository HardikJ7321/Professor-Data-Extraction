import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

chrome_driver_path = 'chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument("--headless")

prof_names = []
prof_depts = []
prof_email = []

driver = webdriver.Chrome(chrome_driver_path, options=chrome_options)

page = 1

while page<=29872:
    print(page)
    
    url = 'https://search2.ucl.ac.uk/s/search.html?query=&collection=website-meta&profile=_directory&tab=directory&start_rank='+str(page)

    driver.get(url)
    time.sleep(15)

    content_list = driver.find_elements_by_css_selector('.result__item.result__item--person.result__item--person--secure')
    for content in content_list:
        try:
            email = content.find_element_by_css_selector('.email a').text
        except:
            continue
        prof_email.append(email)
        print('XXXXXXX'+email)
        name = content.find_element_by_css_selector('.profile-details .fn').text
        prof_names.append(name)
        print('XXXXXXXX'+name)
        org = []
        try:
            org_links = content.find_elements_by_css_selector('.org p')
            for o in org_links:
                org.append(o.text)
            dept = ", ".join(org)
        except:
            dept = ''
        prof_depts.append(dept)
        print('XXXXXXXXXXXX'+dept)
    page+=10

driver.close()
df = pd.DataFrame({'Name': prof_names, 'Department': prof_depts, 'Email':prof_email})
df.to_excel('ucl.xlsx',index=False)
