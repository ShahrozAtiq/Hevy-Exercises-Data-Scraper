from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

EMAIL="ENTER_EMAIL"
PASS="ENTER_PASS"

class text_to_change(object):
    def __init__(self, locator, old_text):
        self.locator = locator
        self.old_text = old_text

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        new_text = element.text
        return new_text != self.old_text

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://hevy.com/exercise/")
driver.maximize_window()



inputTags = driver.find_elements("xpath", '//input[@label]')
for inputTag in inputTags:
    if "email" in inputTag.get_attribute("label").lower() or "username" in inputTag.get_attribute("label").lower():
        inputTag.send_keys(EMAIL)
    elif "password" in inputTag.get_attribute("label").lower():
        inputTag.send_keys(PASS)

buttons_elements = driver.find_elements("xpath", '//button')
for button in buttons_elements:
    if button.get_attribute("innerText").lower() == "login":
        button.click()

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "sc-5cc7d96-0")]')))
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "sc-5cc7d96-0")]')))
exercises = driver.find_elements("xpath", '//div[contains(@class, "sc-5cc7d96-0")]')
allData=[]
for index , ex in enumerate(exercises):
    exData={
            "name" : "None",
            "equipment" : "None",
            "primary_muscle" : "None",
            "secondary_muscle" : "None",
            "source" : "None",
            "sourceType" : "None",
            "thumbnail":"None"
            }
    
    ex.click()
    if index==0:
        time.sleep(5)
    else:
        WebDriverWait(div, 10).until(text_to_change((By.XPATH, './/h1'),allData[len(allData)-1]["name"]))

    div = driver.find_element("xpath", '//div[contains(@class, "sc-d526da1-0")]')
    
    exData["name"] = div.find_element("xpath", './/h1').get_attribute("innerText")

    p_elements = div.find_elements("xpath", './/p')

    exData["equipment"]=p_elements[1].get_attribute("innerText")
    exData["primary_muscle"]=p_elements[3].get_attribute("innerText")

    if len(p_elements)>4:
        exData["secondary_muscle"]=p_elements[5].get_attribute("innerText")

    try:
        exData["source"] = div.find_element("xpath", './/img').get_attribute("src")
        exData["sourceType"] = "image"
    except:
        try:
            exData["source"] = div.find_element("xpath", './/source').get_attribute("src")
            exData["sourceType"] = "video"
        except:
            print("nofile")
    try:
        exData["thumbnail"] = ex.find_element("xpath", './/img').get_attribute("src")
    except:
        pass

    allData.append(exData)
    print(exData)

csv_file_path = "D:\Coding\Python Projects\Hevy\exercises_data.csv"

fieldnames = ["name", "equipment", "primary_muscle", "secondary_muscle", "source", "sourceType"]

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    writer.writeheader()
    
    for exData in allData:
        writer.writerow(exData)

driver.quit()

print("Data has been successfully saved to:", csv_file_path)