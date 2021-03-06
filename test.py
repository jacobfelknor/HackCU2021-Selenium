from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from keys import password, username

option = webdriver.ChromeOptions()
# option.add_argument("-incognito")
# option.add_argument("--headless")
# option.add_argument("disable-gpu")

browser = webdriver.Chrome(
    executable_path=r"/home/jacob/bin/chromedriver", options=option
)

browser.get("https://www.bgvgrandcentral.com/")

user = WebDriverWait(browser, 20).until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            """/html/body/div/div[2]/div[2]/div/div/div[1]/form/div[2]/fieldset/div/input[1]""",
        )
    )
)
user.send_keys(username)

passwd = WebDriverWait(browser, 20).until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            """/html/body/div/div[2]/div[2]/div/div/div[1]/form/div[2]/fieldset/div/input[2]""",
        )
    )
)


passwd.send_keys(password)

login = WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            """/html/body/div/div[2]/div[2]/div/div/div[1]/form/div[2]/fieldset/div/div/button""",
        )
    )
)


login.click()


parking = WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable(
        (By.XPATH, """/html/body/div/div[5]/div/div[2]/div/div[2]/div/div[2]/a""")
    )
)

parking.click()


day = WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            """/html/body/div/div[5]/div/div[2]/div[2]/div/div/div[4]/div[2]/div/div/div/table/tbody/tr[9]/td[4]/form/button""",
        )
    )
)
day.click()


confirm = WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            """/html/body/div/div[5]/div/div[2]/form/div[2]/div/button""",
        )
    )
)
confirm.click()


confirm_again = WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            """/html/body/div/div[5]/div/div[2]/form/button""",
        )
    )
)
confirm_again.click()