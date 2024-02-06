# import required modules
import os
import pickle
from io import BytesIO
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

import requests


class GetStatus():
    def __init__(self) -> None:
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--window-size=900,600')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("start-maximized")
        self.options.add_argument("disable-infobars")
        self.options.add_argument("--disable-browser-side-navigation")

        self.cookies_file = "whatsapp_cookies.pkl"

        if os.path.exists(self.cookies_file):
            with open(self.cookies_file, "rb") as f:
                self.cookies = pickle.load(f)
            for cookie in self.cookies:
                self.options.add_argument(f"--cookie={cookie['name']}={cookie['value']}")

        self.driver = webdriver.Chrome(options=self.options)
        #self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
        self.driver.get("https://web.whatsapp.com/")

    def save_cookies(self):
        cookies = self.driver.get_cookies()
        with open(self.cookies_file, "wb") as f:
            pickle.dump(cookies, f)

    def seturl(self):
        self.url = f"https://web.whatsapp.com/send/?phone={self.id}&text&type=phone_number&app_absent=0"


    def test(self):
            self.count = 4
            self.time = self.count *2
            try:
                self.a = WebDriverWait(self.driver, self.time).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'))).get_attribute("title")
                #/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]
            except TimeoutException: 
                try:
                    self.a = WebDriverWait(self.driver, self.time).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/span[2]/div/span/div/div/div/div/div/div[1]'))).get_attribute("innerHTML")
                except TimeoutException:                
                    if(self.count > 1):
                        self.count -= 1
                        self.test()
                except:
                    self.result = "Error." or "Erro"
                else:
                    if(self.a == self.checkerTextInvalid):
                        self.result = "Numero Invalido"
                    else:
                        self.result = "Error." or "Erro"
            except:
                self.result = "Error." or "Erro"
            else:
                if(self.a == self.checkerTextValid):
                    self.result = "Numero valido."
                else:
                    self.result = "Sucesso."
            finally:
                print(self.result)
                self.count = 3


    def run(self, id):
        
        self.options.add_argument('headless');
        self.waitText = "Starting chat"
        self.checkerTextInvalid = "Phone number shared via url is invalid."
        self.checkerTextValid = "Type a message"
        self.id = id

        self.seturl()
        self.driver.get(self.url)

        self.test()

        return self.result
        
    def login(self):
        self.driver.get("https://web.whatsapp.com")


    def github(self):
        self.driver.get("https://github.com/soaresgabe/whatsapp-status")


    def check_login_status(driver):
        try:
            chat_list = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._3j8Pd")))
            return True
        except:
            return False
        else:
            self.driver.close()
            self.chrome_options.add_argument('--headless')
            driver.execute_script("window.open('https://web.whatsapp.com');")
