from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

service = Service(r"C:\Users\Lenovo\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.rewe.de/shop")
time.sleep(3)

# Click the entry button
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "intentionButtonList"))
)
button.click()

# List of zip codes
zip_codes = ["01067","10115","01030", "20095", "01050","50667"]

for zc in zip_codes:
    try:
        # Try to find zipcode input
        try:
            zip_code = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "gbmc-zipcode-input"))
            )
            zip_code.clear()
            zip_code.send_keys(zc + Keys.ENTER)
        except TimeoutException:
            print("Zip input not available, maybe we're already inside checkout flow.")

        time.sleep(2)

        # Wait for either back button or change-zip link
        try:
            element = WebDriverWait(driver, 5).until(
                EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME, "gbmc-back-button")),
                    EC.presence_of_element_located((By.CLASS_NAME, "gbmc-change-zipcode-link"))
                )
            )

            if "gbmc-back-button" in element.get_attribute("class"):
                print(f"Zip {zc} accepted -> back button present.")
                element.click()  # go back to try next
            elif "gbmc-change-zipcode-link" in element.get_attribute("class"):
                print(f"Zip {zc} accepted -> change zip link present.")
                element.click()  # optionally click to enter another zip

        except TimeoutException:
            print(f"Neither button present for zip {zc}, clicking 'gbmc-headed-back-button' and retrying intentionButtonList.")
            try:
                # Click gbmc-headed-back-button first
                headed_back = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "gbmc-headed-back-button"))
                )
                headed_back.click()
                time.sleep(1)

                # Retry clicking intentionButtonList
                intention_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "intentionButtonList"))
                )
                intention_btn.click()
                time.sleep(1)

            except Exception as e:
                print(f"Failed to recover for zip {zc}")
                continue

    except Exception as e:
        print(f"Error with zip {zc}: {e}")

time.sleep(5)
driver.quit()
