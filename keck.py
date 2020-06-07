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


elements = 'pqrstvwx'
for ele in elements:
    print(ele)
    driver = webdriver.Chrome(chrome_driver_path, options=chrome_options)
    driver.get('https://keck.usc.edu/faculty-search/')
    time.sleep(15)
    tab_link = '#'+ele+'.tab-link'
    req_class_name = '.preson.' + ele.upper()
    tab_link_ele = driver.find_element_by_css_selector(tab_link)
    tab_link_ele.click()
    time.sleep(10)
    content_list = driver.find_elements_by_css_selector(req_class_name)
    for content in content_list:
        link = content.find_element_by_css_selector('a').get_attribute('href')
        new_driver = webdriver.Chrome(chrome_driver_path, options=chrome_options)
        new_driver.get(link)
        new_driver.get(link)
        #response = requests.get(link)
        #soup = BeautifulSoup(response.content, "html.parser")
        #print('XXXXXXXXXXX',soup.prettify())
        time.sleep(20)
        name = new_driver.find_element_by_css_selector('.fm-person-preferred-name').text
        #name = soup.find('div',{'class':'fm-person-preferred-name'}).text
        if ',' in name:
            name = name.split(',')[0]
        prof_names.append(name)
        print('XXXXXXXXXXX'+name)
        try:
            dept_name = new_driver.find_element_by_css_selector('.fm-title.fm-department').text
            #dept_class = soup.find('div',{'class':'fm-department'})
            #dept_name = dept_class.find('span').text
        except:
            dept_name = ''
        prof_depts.append(dept_name)
        try:
            email = new_driver.find_element_by_css_selector('.fm-title.fm-email span a').text
            #email_class = soup.find('div',{'class':'fm-email'})
            #email = email_class.find('span').find('a').text
        except:
            email = ''
        prof_email.append(email)
        new_driver.close()

    driver.close()
    df = pd.DataFrame({'Name': prof_names, 'Department': prof_depts, 'Email': prof_email})
    df.to_excel('keck'+ele+'.xlsx', index=False)

