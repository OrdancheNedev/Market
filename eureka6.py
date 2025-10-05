import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

# ---------------- Setup ----------------
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

service = Service(r"C:\Users\Lenovo\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.rewe.de/shop")
time.sleep(3)

# Click initial entry button
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "intentionButtonList"))
).click()

# ---------------- Zip codes list ----------------
zip_codes = ['01067', '01069', '01070', '01071', '01167','01168']

# Store results here
results = []

# ---------------- Loop through zip codes ----------------
for zc in zip_codes:
    try:
        print(f"\nProcessing zip code: {zc}")

        # Step 1: Enter zip code
        try:
            zip_input = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "gbmc-zipcode-input"))
            )
            zip_input.clear()
            zip_input.send_keys(zc + Keys.ENTER)
        except TimeoutException:
            print("Zip input not available, maybe we're already in checkout flow.")

        time.sleep(2)

        # Step 2: Check for available buttons
        try:
            element = WebDriverWait(driver, 5).until(
                EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME, "gbmc-back-button")),
                    EC.presence_of_element_located((By.CLASS_NAME, "gbmc-change-zipcode-link"))
                )
            )
            # ✅ If found → availability = Yes
            results.append({"zipcode": zc, "availability": "Yes"})

            # Re-find element to avoid stale reference
            element = driver.find_element(By.CLASS_NAME, element.get_attribute("class").split()[0])

            if "gbmc-back-button" in element.get_attribute("class"):
                print(f"Zip {zc} accepted -> back button present.")
                element.click()
            elif "gbmc-change-zipcode-link" in element.get_attribute("class"):
                print(f"Zip {zc} accepted -> change zip link present.")
                element.click()

        except TimeoutException:
            # ❌ If not found → availability = No
            print(f"Neither back nor change-zip buttons present for zip {zc}, marking as No...")
            results.append({"zipcode": zc, "availability": "No"})

            # Recovery flow
            try:
                headed_back = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "gbmc-headed-back-button"))
                )
                headed_back.click()
                time.sleep(1)

                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "intentionButtonList"))
                ).click()
                time.sleep(1)
                print(f"Recovered successfully for zip {zc}")

            except Exception:
                print(f"Recovery failed for zip {zc}")
                continue

    except Exception as e:
        print(f"Unexpected error with zip {zc}: {e}")
        results.append({"zipcode": zc, "availability": "No"})

time.sleep(5)
driver.quit()

# ---------------- Save results ----------------
df = pd.DataFrame(results)
df.to_csv("zip_availability.csv", index=False)
print("\n✅ Dataset saved as zip_availability.csv")
