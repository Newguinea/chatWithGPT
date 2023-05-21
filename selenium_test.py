import os
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait  # Correct import for WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from app import app, db, login_manager
from app.models import User, Chat, Message
from flask_login import login_user, logout_user, login_required, current_user
from app.DND import GameSession
from app.longtext import *



class LoginTestCase(unittest.TestCase):
    def setUp(self):
        chromedriver_path = os.getenv('CHROMEDRIVER_PATH')
        self.driver = webdriver.Chrome(executable_path=chromedriver_path)  # Use the specified ChromeDriver executable path
        self.driver.get('http://127.0.0.1:5000/login')

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        # Find the username and password input fields
        username_input = self.driver.find_element_by_id('username')
        password_input = self.driver.find_element_by_id('password')

        # Enter the username and password
        username_input.send_keys('dddd')
        password_input.send_keys('dddd')

        # Submit the login form
        password_input.send_keys(Keys.RETURN)
        #checks if at the home page
        home_page_url = 'http://127.0.0.1:5000/index'  # Replace with the URL of the home page
        self.assertEqual(self.driver.current_url, home_page_url)
class ChatSeleniumTestCase(unittest.TestCase):
    def setUp(self):
        chromedriver_path = os.getenv('CHROMEDRIVER_PATH')
        self.driver = webdriver.Chrome(executable_path=chromedriver_path)  # WebDriver for browser
        self.driver.get('http://127.0.0.1:5000/login')

    def tearDown(self):
        self.driver.quit()

    def test_chat_functionality(self):
        # Find the username and password input fields
        username_input = self.driver.find_element_by_id('username')
        password_input = self.driver.find_element_by_id('password')

        # Enter the username and password
        username_input.send_keys('dddd')
        password_input.send_keys('dddd')

        # Submit the login form
        password_input.send_keys(Keys.RETURN)

        # Wait for the page to load after logging in
        self.driver.implicitly_wait(5)

        # Assert that the login is successful and the user is redirected to the home page
        home_page_url = 'http://127.0.0.1:5000/index'  # Replace with the URL of the home page
        self.assertEqual(self.driver.current_url, home_page_url)

        # Navigate to the chat page
        self.driver.get('http://127.0.0.1:5000/chat')  # Replace with the URL of the chat page
        # Test create chat
        create_chat_button = self.driver.find_element_by_id('newChatButton')
        create_chat_button.click()

        # Wait for the chat to be created
        self.driver.implicitly_wait(2)

        # Test send and get messages
        message_input = self.driver.find_element_by_class_name('chat-input')
        message_input.send_keys('Hello, world!')
        send_button = self.driver.find_element_by_id('send-btn')
        send_button.click()

        # Wait for the message to be sent and received
        self.driver.implicitly_wait(6)

class DNDTestCase(unittest.TestCase):
    def setUp(self):
        chromedriver_path = os.getenv('CHROMEDRIVER_PATH')
        self.driver = webdriver.Chrome(executable_path=chromedriver_path)  # WebDriver for browser
        self.driver.get('http://127.0.0.1:5000/login')

    def tearDown(self):
        self.driver.quit()

    def test_chat_functionality(self):
        # Find the username and password input fields
        username_input = self.driver.find_element_by_id('username')
        password_input = self.driver.find_element_by_id('password')

        # Enter the username and password
        username_input.send_keys('dddd')
        password_input.send_keys('dddd')


        # Submit the login form
        password_input.send_keys(Keys.RETURN)
        self.driver.implicitly_wait(1)

        # Assert that the login is successful and the user is redirected to the home page
        home_page_url = 'http://127.0.0.1:5000/index'  # Replace with the URL of the home page
        self.assertEqual(self.driver.current_url, home_page_url)
        self.driver.get('http://127.0.0.1:5000/dnd')

        # Click start play button
        start_play_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "start-play-btn")))
        start_play_button.click()

        # Find the chat input element and send a message
        chat_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "chat-input")))
        chat_input.send_keys("Hello, how are you?")
        send_button = self.driver.find_element_by_id("send-btn")
        send_button.click()

        # Wait for the new chat message to appear in the chat history
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Hello, how are you?')]")))

        # Find the chat history element
        chat_history = self.driver.find_element_by_id("chat-history")

        # Check if the message appears in the chat history
        self.assertIn("Hello, how are you?", chat_history.text)

class longTextTestCase(unittest.TestCase):
    def setUp(self):
        chromedriver_path = os.getenv('CHROMEDRIVER_PATH')
        self.driver = webdriver.Chrome(executable_path=chromedriver_path)  # WebDriver for browser
        self.driver.get('http://127.0.0.1:5000/login')

    def tearDown(self):
        self.driver.quit()

    def test_chat_functionality(self):
        # get current directory
        current_dir = os.getcwd()
        # create absolute file path
        file_path = os.path.join(current_dir, 'app', 'tester.txt')

        # Find the username and password input fields
        username_input = self.driver.find_element_by_id('username')
        password_input = self.driver.find_element_by_id('password')

        # Enter the username and password
        username_input.send_keys('dddd')
        password_input.send_keys('dddd')

        # Submit the login form
        password_input.send_keys(Keys.RETURN)
        self.driver.implicitly_wait(1)

        # Assert that the login is successful and the user is redirected to the home page
        home_page_url = 'http://127.0.0.1:5000/index'  # Replace with the URL of the home page
        self.assertEqual(self.driver.current_url, home_page_url)
        self.driver.get('http://127.0.0.1:5000/process')

        # Locate and interact with the file input element
        file_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "file")))
        file_input.send_keys(file_path)  # Provide the path to the test file

        # Locate and interact with the 'final_prompt' input element
        final_prompt_input = self.driver.find_element_by_name("compress_prompt")
        final_prompt_input.send_keys("What is this story about?")

        # Locate and interact with the 'compress_prompt' input element
        compress_prompt_input = self.driver.find_element_by_name("final_prompt")
        compress_prompt_input.send_keys("Summarize the key points of this story.")

        # Locate and click the 'Start Process' button
        submit_button = self.driver.find_element_by_xpath('//input[@type="submit"]')
        submit_button.click()

        # Check the result
        WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, "//h2[text()='Result']")))

        # Here,result will be displayed in a 'p' tag with a class 'border border-primary p-2'
        result_text = self.driver.find_element_by_xpath("//p[@class='border border-primary p-2']").text
        self.assertIsNotNone(result_text)

if __name__ == '__main__':
    unittest.main()


