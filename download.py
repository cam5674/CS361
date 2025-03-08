

import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


# downloads csv file from nasdaq

download_dir = "C:\\Users\\camer\\Desktop\\test_1"


options = Options()
options.add_experimental_option('prefs',  {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
    }
)


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://www.nasdaq.com/market-activity/etf/aapl/historical?page=1&rows_per_page=10&timeline=m1')
download_csv = WebDriverWait(driver, 10).until(
    expected_conditions.presence_of_element_located((By.CLASS_NAME, "historical-download"))
)

# Click the element
download_csv.click()
time.sleep(5)
driver.close()