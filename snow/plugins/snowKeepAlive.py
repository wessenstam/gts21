from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time

for i in range (001,151):
    acctEmail = "gts" + "{0:03d}".format(i) + "@nutanix.com"

    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options, executable_path=r'C:\Windows\System32\chromedriver.exe')
    driver.implicitly_wait(10)
    driver.get("https://signon.service-now.com/ssologin.do?RelayState=%252Fapp%252Ftemplate_saml_2_0%252Fk317zlfESMUHAFZFXMVB%252Fsso%252Fsaml%253FRelayState%253Dhttps%25253A%25252F%25252Fdeveloper.servicenow.com%25252Fdev.do&redirectUri=&email=")
    driver.find_element_by_id("username").send_keys(acctEmail)
    driver.find_element_by_id("username").send_keys(Keys.ENTER)
    driver.find_element_by_id("password").send_keys("XXXXXXXXXXX")
    driver.find_element_by_id("password").send_keys(Keys.ENTER)
    time.sleep(15)
    print('Logged in as ' + acctEmail)
    driver.quit()
