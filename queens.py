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
start = 0

while page<=88:
    print(page)
    if start==0:
        url = 'https://pure.qub.ac.uk/en/persons/?format='
        start = 1
    else:
        url = 'https://pure.qub.ac.uk/en/persons/?format=&page='+str(page)


    driver.get(url)
    time.sleep(20)

    content_list = driver.find_elements_by_css_selector('.grid-result-item')
    for content in content_list:
        name = content.find_element_by_css_selector('.title a span').text
        prof_names.append(name)
        print(name)
        try:
            email = content.find_element_by_css_selector('.email a span').text
        except:
            email = ''
        prof_email.append(email)
        org = []
        try:
            org_links = content.find_elements_by_css_selector('.relations.organisations li a span')
            for o in org_links:
                org.append(o.text)
            dept = ", ".join(org)
        except:
            dept = ''
        prof_depts.append(dept)

    page+=1


df = pd.DataFrame({'Name': prof_names, 'Department': prof_depts, 'Email':prof_email})
df.to_excel('queens.xlsx',index=False)
