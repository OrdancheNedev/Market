from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
import time 

chrome_options = Options()
chrome_options.add_argument("--start-maximized")


service = Service(r"C:\Users\Lenovo\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.knuspr.de")

time.sleep(20)

driver.quit()

