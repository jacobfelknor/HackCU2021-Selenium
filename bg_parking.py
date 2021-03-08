from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from keys import chromedriver, email_pass, email_user, me, password, url, username, you


## EMAIL CONFIRMATION
def email_confirmation(msg: str = None, msg_prefix: str = "") -> None:
    # Import smtplib for the actual sending function
    import smtplib
    from datetime import datetime, timedelta

    # Import the email modules we'll need
    from email.mime.text import MIMEText

    if msg is None:
        now = datetime.now()
        then = now + timedelta(days=7)
        now = now.strftime("%A, %B %e %Y")
        then = then.strftime("%A, %B %e %Y")
        msg = MIMEText(f"{msg_prefix}Booking made at {now} for {then}.")
    else:
        msg = MIMEText(msg)

    msg["Subject"] = "Your Breckenridge Booking bot just ran"
    msg["From"] = me
    msg["To"] = you

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(email_user, email_pass)
    s.sendmail(me, [you], msg.as_string())
    s.quit()


option = webdriver.ChromeOptions()
option.add_argument("-incognito")
option.add_argument("--headless")
# option.add_argument("disable-gpu")


try:

    browser = webdriver.Chrome(executable_path=chromedriver, options=option)

    browser.get(url)

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

    # this is the day a week from today
    day = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                """/html/body/div/div[5]/div/div[2]/div[2]/div/div/div[4]/div[2]/div/div/div/table/tbody/tr[9]/td[4]/form/button""",
            )
        )
    )
    day.click()

    try:
        # assume no waitlist
        pick_car = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    """/html/body/div/div[5]/div/div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr[2]/td[6]/button""",
                )
            )
        )
        pick_car.click()
        confirm = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    """/html/body/div/div[5]/div/section[2]/div[2]/div/form/button""",
                )
            )
        )
        confirm.click()
        email_confirmation()
    except TimeoutException:
        # must be waitlist?
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
        email_confirmation(msg_prefix="Waitlist ")

except Exception as e:
    email_confirmation(f"ERROR: {e}")
