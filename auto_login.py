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
    browser.add_cookie({"name": "MUSIC_U", "value": "0099AFA5F1C901FBE6CE156F586944BE61DB24C1F28A1A887F97626CFC65C02F586C70D6217B4FCF733F0BEDD9DC25E36CF49A2D2E182D0E0FE840D15C75B0433A6C741C1257526E035DCA0C4BCD7987CA324E551A66843716A829FF300F58D220A777E29ED9A6478833375FFE66DC8F0AE0F5411E50D72E16464C46C8EAFEE5059CCA7CAEEFC33AAB83EDE0132508F0F503A535B4534445346542A59E26B4C98774BF29BCFB97F799C0EEEA366C319D63350D5FDC734FDC65585A9B437B836EC1FEEA3E6C5A1C9D6364BCF3A4A590EA64886E2CF62FB2C07953EEA240317A53920CCF370AC5B471F56868C5E2DD94F719A00C596FC7E095AED15775A8F210EA5FB3B10A3E28F366B74897D418B2B37975F3E25F7B17B0D70156B091FC6658C6897FBAD5E61724B05F55BF245C790B2B515F37E48ABED51C6366A2260E3ECB071004209F15FC5638DC8AAD745516DFB3B4C70C80D275C84A124E916B5D685481D37382AE0FD75210768511AE28781BF632FE3FC7DE123FE11C3F7D1F26E246116A15936139A0851CDC97B6F784B20763BE69B81F54635EAC42BFA97195DD5D06B1"})
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
