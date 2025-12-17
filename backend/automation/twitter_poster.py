import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class TwitterPoster:
    def __init__(self, username, password, email=None):
        self.username = username
        self.password = password
        self.email = email
        
        # Setup Chrome options
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless") # Comment out to see the browser
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 20)

    def login(self):
        try:
            self.driver.get("https://twitter.com/i/flow/login")
            
            # Enter Username
            username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "text")))
            username_input.send_keys(self.username)
            username_input.send_keys(Keys.RETURN)
            
            # Check for unusual activity (sometimes asks for email/phone)
            try:
                # Wait briefly to see if it asks for password or email
                time.sleep(2)
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                for input_field in inputs:
                    if "text" in input_field.get_attribute("type") and "password" not in input_field.get_attribute("name"):
                        # Likely asking for email/phone verification
                        if self.email:
                            input_field.send_keys(self.email)
                            input_field.send_keys(Keys.RETURN)
                            time.sleep(1)
                        break
            except:
                pass

            # Enter Password
            password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_input.send_keys(self.password)
            password_input.send_keys(Keys.RETURN)
            
            # Wait for home page
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='SideNav_NewTweet_Button']")))
            print("Login successful")
            
        except Exception as e:
            print(f"Login failed: {e}")
            self.driver.quit()
            raise e

    def post(self, text, media_path=None):
        try:
            self.driver.get("https://twitter.com/compose/tweet")
            
            # Wait for text area
            text_area = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']")))
            
            # Type text
            # We use JS to set value sometimes if send_keys is flaky, but send_keys usually works for X
            text_area.send_keys(text)
            
            # Upload Media
            if media_path:
                file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                file_input.send_keys(media_path)
                
                # Wait for upload to complete (simplified check)
                time.sleep(5) 
            
            # Click Tweet
            tweet_button = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='tweetButton']")
            tweet_button.click()
            
            # Wait for success toast or just wait a bit
            time.sleep(5)
            print("Posted successfully")
            
        except Exception as e:
            print(f"Posting failed: {e}")
            raise e
        finally:
            self.driver.quit()
