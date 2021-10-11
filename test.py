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
    msg = f"{msg_prefix}Booking made at {now} for {then}."

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


try:
    option = webdriver.ChromeOptions()
    option.add_argument("-incognito")
    option.add_argument("--headless")
    # option.add_argument("disable-gpu")


    browser = webdriver.Chrome(executable_path=chromedriver, options=option)

    browser.get(url)



    email_confirmation()
except:
    pass
finally:
    print("here")
    browser.close()
    browser.quit()