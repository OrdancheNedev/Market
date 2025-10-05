from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
import time 

chrome_options = Options()
chrome_options.add_argument("--start-maximized")


service = Service(r"C:\Users\Lenovo\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.knuspr.de")

time.sleep(3)

button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME,"sc-bd7fdcd9-0"))
)

button.click()

time.sleep(5)

zip_code = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME,"sc-99196136-6"))
)

zip_code.send_keys("Berlin"+ Keys.ENTER)



button2 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME,"sc-db4ed576-0"))
)
button2.click()

time.sleep(10)



driver.quit()

