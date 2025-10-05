from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
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
zip_codes = ['01067', '01069', '01070', '01071', '01072', '01073', '01074', '01075', '01076', '01077', '01078', '01079', '01080', '01081', '01082', '01083', '01084', '01085', '01086', '01087', '01088', '01089', '01090', '01091', '01092', '01093', '01094', '01095', '01096', '01097', '01098', '01099', '01100', '01101', '01102', '01103', '01104', '01105', '01106', '01107', '01108', '01109', '01110', '01111', '01112', '01113', '01114', '01115', '01116', '01117', '01118', '01119', '01120', '01121', '01122', '01123', '01124', '01125', '01126', '01127', '01128', '01129', '01130', '01131', '01132', '01133', '01134', '01135', '01136', '01137', '01138', '01139', '01140', '01141', '01142', '01143', '01144', '01145', '01146', '01147', '01148', '01149', '01150', '01151', '01152', '01153', '01154', '01155', '01156', '01157', '01158', '01159', '01160', '01161', '01162', '01163', '01164', '01165', '01166', '01167','01168']


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
            # Re-find element to avoid stale reference
            element = driver.find_element(By.CLASS_NAME, element.get_attribute("class").split()[0])

            if "gbmc-back-button" in element.get_attribute("class"):
                print(f"Zip {zc} accepted -> back button present.")
                element.click()
            elif "gbmc-change-zipcode-link" in element.get_attribute("class"):
                print(f"Zip {zc} accepted -> change zip link present.")
                element.click()

        except TimeoutException:
            print(f"Neither back nor change-zip buttons present for zip {zc}, attempting recovery...")

            # Step 3: Recovery flow
            try:
                # Click headed-back button
                headed_back = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "gbmc-headed-back-button"))
                )
                headed_back.click()
                time.sleep(1)

                # Retry clicking initial intentionButtonList
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "intentionButtonList"))
                ).click()
                time.sleep(1)
                print(f"Recovered successfully for zip {zc}")

            except Exception as e:
                print(f"Recovery failed for zip {zc}")
                continue

    except Exception as e:
        print(f"Unexpected error with zip {zc}: {e}")

time.sleep(5)
driver.quit()
