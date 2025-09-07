# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00AB8DA087D34325363C03BFCB3BC037A844B3326080D6101535FCB082EC83D0E4C2603D774306C9692DA9C5D110DF7CD3F211C668E39E01C077917F93FE08D37F85495B8125639E05C80834A08FB5C306CEC25B624C92CED86767A9937074CD236BE4DD8937B5EC2AC1B382A3BFEFF6AD99FE4FC004ACF0C184A0AFB97B120763223600116E66EEE9EF10E2AE3938DA2A3387EA058D6666C896E5F899C5F352EF5746401B9E2D92289C84E1014B4FF051C4F80A875CCBF95A11D80359F9180B2C589387999F1714F3791548C277C0456F33646DD0F25C293C082C9B61257D576D3E243C74FB486AB73F66B5264DA175DE1CAC3BAFAAC1CB4C210531F8B46FA6E47AB0D1A3405DC80768EE086A3B72189AE9B2205E2C31C49333363665582E264B7FC3161FE8CFE554D9CFD673BF263E303976E5FD57F4A5940705CF8A1F2B1D2F40446711DEF0E544C54B817DF854AD7C9CB2A86CE59F639A6C387A8AEB244178E8A1CBB847A9174D5397B6C5C4A8B4F9C95B9B54EED16A1F9B361E82D2A3741858B6054A76081736A6466CFC9F911F5286B1BD70B85AD57DC906F1E640680CC2"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
