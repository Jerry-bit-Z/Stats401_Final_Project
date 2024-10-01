import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Set up Safari WebDriver
driver = webdriver.Safari()

# Navigate to the desired webpage
i = '泡沫'
url_1 = f"https://y.qq.com/n/ryqq/search?w={i}&t=song&remoteplace=txt.yqq.center"
driver.get(url_1)  # Replace with your target URL

# Wait for the page to load
time.sleep(5)

# Open Developer Tools
driver.execute_script("window.open()")
driver.switch_to.window(driver.window_handles[-1])
driver.get("javascript:void(document.querySelector('#-webkit-web-inspector').contentWindow.UI.inspectorView._tabbedPane.selectTab('network'))")

# Wait for the Network tab to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".network-log-grid")))

# Find FCG file requests
fcg_requests = driver.find_elements(By.XPATH, "//div[contains(@class, 'network-log-grid')]//div[contains(text(), '.fcg')]")

for request in fcg_requests:
    request.click()
    # Wait for the request details to load
    time.sleep(2)
    
    # Switch to the Response tab
    response_tab = driver.find_element(By.XPATH, "//div[text()='Response']")
    response_tab.click()
    
    # Get the FCG file contents
    fcg_content = driver.find_element(By.CSS_SELECTOR, ".request-view-body pre").text
    print(f"FCG File Contents:\n{fcg_content}")

# Close the browser
driver.quit()