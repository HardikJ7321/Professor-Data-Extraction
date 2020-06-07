import time
# import requests
# from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

chrome_driver_path = './chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument("--headless")

prof_names = []
prof_depts = []
prof_email = []


for p in range(13,42):
    print(p)
    driver = webdriver.Chrome(chrome_driver_path, options=chrome_options)
    driver.get('https://med.stanford.edu/profiles/browse?p=' + str(p) + '&affiliations=capFaculty&ps=100')
    time.sleep(150)
    content_list = driver.find_elements_by_css_selector('.unstyled.list-items li')
    for content in content_list:
        link = content.find_element_by_css_selector('.media-body a').get_attribute('href')
        print(link)
        name = content.find_element_by_css_selector('.media-body a h4').text
        prof_names.append(name)
        print(name)
        dept = content.find_element_by_css_selector('.media-body a h5').text
        prof_depts.append(dept)
        new_driver = webdriver.Chrome(chrome_driver_path, options=chrome_options)
        new_driver.get(link)
        time.sleep(15)
        try:
            email_div = new_driver.find_element_by_css_selector('.contact-info.primary')
            email = email_div.find_element_by_css_selector('.email').text
        except:
            email = ''
        prof_email.append(email)
        new_driver.close()
    driver.close()
    df = pd.DataFrame({'Name': prof_names, 'Department': prof_depts, 'Email':prof_email})
    df.to_excel('harvard'+str(p)+'.xlsx',index=False)
