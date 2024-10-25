from webdriver_manager.chrome import ChromeDriverManager
from email.mime.multipart import MIMEMultipart
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from keys import (
    email_link_url,
    email_pass,
    email_user,
    me,
    password,
    url,
    username,
    you,
)


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
        msg = MIMEMultipart("alternative")
        plain = MIMEText(
            f"{msg_prefix}Parking reserved at Grand Lodge Peak 7 for {then}.", "plain"
        )
        html_contents = f"""
        <html>
            <head></head>
            <body>
                <p>
                    {msg_prefix}Parking reserved at Grand Lodge Peak 7 for <b>{then}</b>.
                    <br><br>
                    Click <a href="{email_link_url}">here</a> to view.
                    <br><br>
                    Your Breck Bot
                </p>
            </body>
        </html>
        """
        html = MIMEText(html_contents, "html")
        msg.attach(plain)
        msg.attach(html)
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
option.add_argument("--headless=new")
# option.add_argument("disable-gpu")

def js_click(browser, clickable):
    browser.execute_script("arguments[0].click();", clickable)

# def get_element(browser, selector):
#     return browser.find_element(*selector)

try:
    driver_manager = ChromeDriverManager().install()

    browser = webdriver.Chrome(service=ChromeService(driver_manager), options=option)

    browser.get(url)

    user = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                """/html/body/div/div[2]/div[2]/div/div/div[1]/form/div[2]/fieldset/div/input[1]""",
            )
        )
    )
    user.send_keys(username)

    passwd = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                """/html/body/div/div[2]/div[2]/div/div/div[1]/form/div[2]/fieldset/div/input[2]""",
            )
        )
    )

    passwd.send_keys(password)

    login = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                """/html/body/div/div[2]/div[2]/div/div/div[1]/form/div[2]/fieldset/div/div/button""",
            )
        )
    )

    js_click(browser, login)

    parking = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, """/html/body/div/div[4]/div/div[2]/div/div[2]/div/div[2]/a""")
        )
    )

    js_click(browser, parking)

    # this is the day a week from today
    day = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                """/html/body/div/div[4]/div/div[2]/div[2]/div/div/div[4]/div[2]/div/div/div/table/tbody/tr[9]/td[4]/form/button""",
            )
        )
    )
    js_click(browser, day)

    try:
        # assume no waitlist
        pick_car = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    """/html/body/div/div[4]/div/div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr[2]/td[6]/button""",
                )
            )
        )
        js_click(browser, pick_car)
        confirm = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    """/html/body/div/div[4]/div/section[2]/div[2]/div/form/button""",
                )
            )
        )
        js_click(browser, confirm)
        email_confirmation()
    except TimeoutException:
        # must be waitlist?
        confirm = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    """/html/body/div/div[4]/div/div[2]/form/div[2]/div/button""",
                )
            )
        )
        js_click(browser, confirm)

        confirm_again = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    """/html/body/div/div[4]/div/div[2]/form/button""",
                )
            )
        )
        js_click(browser, confirm_again)
        email_confirmation(msg_prefix="Waitlist ")

except Exception as e:
    email_confirmation(f"{e.__class__.__name__}: {e}")
finally:
    # close and quit browser to avoid zombies
    browser.close()
    browser.quit()
