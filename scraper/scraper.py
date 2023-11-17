import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By


def initialize_webdriver():
    """
    Initializes and returns a Chrome WebDriver for modularity.
    """
    options = uc.ChromeOptions()
    options.headless = False
    chrome_driver = uc.Chrome(use_subprocess=True, options=options)
    return chrome_driver
