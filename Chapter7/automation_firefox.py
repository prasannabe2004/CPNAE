from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.keys  import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

driver.get("https://www.python.org/")

search_bar = driver.find_element(By.NAME, "q")
search_bar.clear()
search_bar.send_keys("Python Documentation")
search_bar.send_keys(Keys.RETURN)

try:
    search_result = driver.find_element(By.PARTIAL_LINK_TEXT,"Documentation by Version")
    search_result.click()
except Exception as e:
    print("Coud not find the specific link")

try:
    search_result = driver.find_element(By.PARTIAL_LINK_TEXT,"3.11.9")
    search_result.click()
except Exception as e:
    print("Coud not find the specific link")

input("Press Enter to close the browser...")

driver.quit()

