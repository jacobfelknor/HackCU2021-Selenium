from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument("-incognito")
# option.add_argument("--headless")
# option.add_argument("disable-gpu")

browser = webdriver.Chrome(executable_path=r"", options=option)

browser.get(
    "https://docs.google.com/forms/d/e/1FAIpQLSdMxDauEatgZGCVoAG3XGuDaCFs9emRPSx9hLUkgtTOf47pqg/viewform"
)
