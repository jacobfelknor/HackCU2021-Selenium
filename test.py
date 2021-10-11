from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from keys import chromedriver, email_pass, email_user, me, password, url, username, you


option = webdriver.ChromeOptions()
option.add_argument("-incognito")
option.add_argument("--headless")


browser = webdriver.Chrome(executable_path=chromedriver, options=option)

browser.get(url)