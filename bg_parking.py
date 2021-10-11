from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from keys import chromedriver, email_pass, email_user, me, password, url, username, you, sns_arn

## EMAIL CONFIRMATION
def email_confirmation(msg: str = None, msg_prefix: str = "") -> None:
    import boto3
    from datetime import datetime, timedelta

    now = datetime.now()
    then = now + timedelta(days=7)
    now = now.strftime("%A, %B %e %Y")
    then = then.strftime("%A, %B %e %Y")
    msg = f"{msg_prefix}Booking made on {now} for {then}."

    subject = "Your Breckenridge Booking bot just ran"

    # Send the message via SNS topic
    client = boto3.client('sns')
    client.publish(
        TopicArn=sns_arn,
        # TargetArn='string',
        # PhoneNumber='string',
        Message=msg,
        Subject=subject,
        # MessageStructure='string',
        # MessageAttributes={
        #     'string': {
        #         'DataType': 'string',
        #         'StringValue': 'string',
        #         'BinaryValue': b'bytes'
        #     }
        # },
        # MessageDeduplicationId='string', # only for fifo
        # MessageGroupId='string' # only for fifo
    )


option = webdriver.ChromeOptions()
option.add_argument("-incognito")
option.add_argument("--headless")
# option.add_argument("disable-gpu")


try:

    browser = webdriver.Chrome(executable_path=chromedriver, options=option)

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

    login.click()

    try:
        # pop up may be here bugging me
        popup = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    """/html/body/div[2]/div/div/div[2]/button[3]""",
                )
            )
        )
        popup.click()
    except TimeoutException:
        # assuming popup isn't there
        pass

    parking = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, """/html/body/div/div[4]/div/div[2]/div/div[2]/div/div[2]/a""")
        )
    )

    parking.click()

    # this is the day a week from today
    day = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                """/html/body/div/div[4]/div/div[2]/div[2]/div/div/div[4]/div[2]/div/div/div/table/tbody/tr[8]/td[4]/form/button""",
            )
        )
    )
    day.click()

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
        pick_car.click()
        confirm = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    """/html/body/div/div[4]/div/section[2]/div[2]/div/form/button""",
                )
            )
        )
        confirm.click()
        email_confirmation()
    except TimeoutException:
        # THIS WILL BE BROKEN - NO WAY TO TEST YET
        # must be waitlist?
        confirm = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    """/html/body/div/div[5]/div/div[2]/form/div[2]/div/button""",
                )
            )
        )
        confirm.click()

        confirm_again = WebDriverWait(browser, 10).until(
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
    print("uh oh")
    email_confirmation(f"{e.__class__.__name__}: {e}")
finally:
    # close and quit browser to avoid zombies
    browser.close()
    browser.quit()
