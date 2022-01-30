import os
import sys
import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

SHOW_BROWSER = True

class TestUI(unittest.TestCase):
    host = 'http://localhost'
    port = '3000'
    live_server_url = host + port

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        driver_path = "drivers/chromedriver"
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1200,800")
        cls.browser = webdriver.Chrome(
            executable_path=driver_path, options=chrome_options
        )
        cls.browser.delete_all_cookies()


    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls.browser.quit()


    def wait_until_element_found(self, xpath):
        WebDriverWait(self.browser, timeout=10).until(
            lambda x: self.browser.find_element_by_xpath(xpath)
        )


    def wait_seconds(self, seconds=2):
        if SHOW_BROWSER:
            time.sleep(seconds)


    def test_page_load(self):
        self.browser.get("http://localhost:3000")
        try:
            self.browser.find_element(by="id", value="app-title")
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            self.fail("App Title could not be loaded")

    def test_download_events(self):
        self.browser.get("http://127.0.0.1:3000")
        self.wait_seconds(5)
        try:
            self.browser.find_element(by="id", value="events-card").click()
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            self.fail("Events card could not be loaded")

        try:
            self.browser.find_element(by="id", value="download0")
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            self.fail("No Download Clip button found")

if __name__ == '__main__':
    unittest.main()